import React, {Component, createRef} from 'react';
import PropTypes from 'prop-types';
import {ColorNames} from 'molstar/lib/mol-util/color/names';
import { Camera } from 'molstar/lib/mol-canvas3d/camera';
import { Mat4 } from 'molstar/lib/mol-math/linear-algebra';

/**
 * The Molstar viewer component for dash
 */
export default class MolstarViewer extends Component {
    constructor(props) {
        super(props);
        const defaultLayout = {
            showImportControls: false,
            showSessionControls: true,
            showStructureSourceControls: true,
            showMeasurementsControls: true,
            showStrucmotifSubmitControls: true,
            showSuperpositionControls: true,
            showQuickStylesControls: true,
            showStructureComponentControls: true,
            showVolumeStreamingControls: false,
            showAssemblySymmetryControls: false,
            showValidationReportControls: false,
            showPredictedAlignedErrorPlot: true,
            showMembraneOrientationPreset: false,
            showNakbColorTheme: false,
            detachedFromSierra: false,
            layoutIsExpanded: false,
            layoutShowControls: false,
            layoutControlsDisplay: 'reactive',
            layoutShowSequence: true,
            layoutShowLog: false,
            viewportShowExpand: true,
            viewportShowSelectionMode: true,
            backgroundColor: ColorNames.white,
            manualReset: false,
            pickingAlphaThreshold: 0.5,
            showWelcomeToast: false,
        };
        const defaultStyle = {
            'zIndex': 10,
            'position': 'relative'
        };
        this.state = {
            data: props.data,
            layout: defaultLayout,
            style: defaultStyle,
            className: props.className,
            selection: props.selection,
            hover: props.hover,
            focus: props.focus,
            frame: props.frame,
            measurement: props.measurement,
            camera: props.camera,
            cameradebounce: props.cameradebounce,
            cameraresponddrag: props.cameraresponddrag,
            screenshot: props.screenshot,
            updatefocusonframechange: props.updatefocusonframechange,
            updateselectiononframechange: props.updateselectiononframechange,
        };
        this.loadedShapes = {};
        this.loadedStructures = {};
        this.prevCameraSnapshot = null;
        this.cameraDebounceTimer = null;
        this.isInternalCameraUpdate = false;
        this.viewerRef = createRef();
        const updatedLayout = Object.assign({}, this.state.layout, props.layout);
        this.state.layout = updatedLayout;
        const updatedStyle = Object.assign({}, this.state.style, props.style);
        this.state.style = updatedStyle;
    }
    areCameraSnapshotsEqual(a, b) {
        if (!a || !b) return false;
        const EPSILON = 1e-6;
        const vec3Equal = (v1, v2) => {
            if (!v1 || !v2) return false;
            return Math.abs(v1[0] - v2[0]) < EPSILON &&
                   Math.abs(v1[1] - v2[1]) < EPSILON &&
                   Math.abs(v1[2] - v2[2]) < EPSILON;
        };
        return a.mode === b.mode &&
               Math.abs(a.fov - b.fov) < EPSILON &&
               Math.abs(a.radius - b.radius) < EPSILON &&
               Math.abs(a.radiusMax - b.radiusMax) < EPSILON &&
               Math.abs(a.fog - b.fog) < EPSILON &&
               a.clipFar === b.clipFar &&
               Math.abs(a.minNear - b.minNear) < EPSILON &&
               Math.abs(a.minFar - b.minFar) < EPSILON &&
               vec3Equal(a.position, b.position) &&
               vec3Equal(a.up, b.up) &&
               vec3Equal(a.target, b.target);
    }
    async handleDataChange(data) {
        // if new molecule was loaded into the viewer, clear the stage before loading
        if (Array.isArray(data)) {
            for (let d of data) {
                if (d.type === 'mol' || d.type === 'url') {
                    this.viewer.clear();
                    this.loadedShapes = {};
                    this.loadedStructures = {};
                    break;
                }
            }
        } else if (typeof data === "object" && (data.type === "mol" || data.type === "url")) {
            this.viewer.clear();
            this.loadedShapes = {};
            this.loadedStructures = {};
        }

        // loading data
        if (data) {
            const molecules = [];
            const shapes = [];

            if (Array.isArray(data)) {
                for (const obj of data) {
                    if (obj.type === 'shape') {
                        shapes.push(obj);
                    } else {
                        molecules.push(obj);
                    }
                }
            } else if (typeof data === "object") {
                if (data.type === 'shape') {
                    shapes.push(data);
                } else {
                    molecules.push(data);
                }
            }

            for (const mol of molecules) {
                await this.loadData(mol);
            }
            for (const shape of shapes) {
                await this.loadShape(shape);
            }
        }
        this.setState({data: data});
    }
    async handleComponentChange(component) {
        if (component) {
            if (Array.isArray(component)) {
                for (const obj of component) {
                    await this.addComponent(obj);
                }
            } else if (typeof component === "object") {
                await this.addComponent(component);
            }
        }
    }
    handleSelectionChange(selection) {
        if (selection) {
            const model_index = this.viewer._plugin.managers.structure.hierarchy.current.structures.length - 1;
            if (model_index >= 0) {
                const id = this.viewer._plugin.managers.structure.hierarchy.current.structures[model_index].cell.obj.data.units[0].model.id;
                let targets = [];
                if (selection.targets && selection.targets[0] !== null) {
                    // convert data from python to molstar data structure
                    targets = this.parseTargetsFromPython(selection.targets, id);
                }
                this.viewer.select(targets, 'select', selection.modifier);
            }
            this.setState({selection: this.parseTargetsForPython(this.viewer.getCurrentSelection())});
        }
    }
    handleHoverChange(hover) {
        if (hover) {
            const model_index = this.viewer._plugin.managers.structure.hierarchy.current.structures.length - 1;
            if (model_index >= 0) {
                const id = this.viewer._plugin.managers.structure.hierarchy.current.structures[model_index].cell.obj.data.units[0].model.id;
                let targets = [];
                if (hover.targets && hover.targets[0] !== null) {
                    // convert data from python to molstar data structure
                    targets = this.parseTargetsFromPython(hover.targets, id);
                }
                this.viewer.select(targets, 'hover', hover.modifier);
            }
            this.setState({selection: this.parseTargetsForPython(this.viewer.getCurrentSelection())});
        }
    }
    handleFocusChange(focus) {
        if (focus) {
            const model_index = this.viewer._plugin.managers.structure.hierarchy.current.structures.length - 1;
            if (model_index >= 0) {
                const id = this.viewer._plugin.managers.structure.hierarchy.current.structures[model_index].cell.obj.data.units[0].model.id;
                let targets = [];
                if (focus.targets && focus.targets[0] !== null) {
                    // convert data from python to molstar data structure
                    targets = this.parseTargetsFromPython(focus.targets, id);
                }
                this.viewer.setFocus(targets, focus.analyse);
            }
            this.setState({focus: this.parseTargetsForPython(this.viewer.getCurrentFocus())});
        }
    }
    handleFrameChange(frame_index) {
        if (Object.keys(this.loadedStructures).length != 0) {
            if (typeof frame_index === 'number') {
                this.viewer.setFrame(frame_index);
            }
            this.setState({frame: frame_index});
        }
    }
    async handleMeasurementChange(measurements) {
        if (measurements) {
            if (Array.isArray(measurements)) {
                if (measurements[0].mode === 'set') this.viewer.clearMeasurement();
                for (const obj of measurements) {
                    await this.addMeasurement(obj);
                }
            } else if (typeof measurements === "object") {
                if (measurements.mode === 'set') this.viewer.clearMeasurement();
                this.addMeasurement(measurements);
            }
        }
        this.setState({measurement: measurements});
    }
    handleCameraChange(camera) {
        if (camera) {
            if (Array.isArray(camera)) {
                // Minimum delay to ensure canvas renders each frame
                const MIN_FRAME_DELAY = 20;
                let delay = MIN_FRAME_DELAY;
                for (const cam of camera) {
                    const duration = cam.duration ?? 0;
                    setTimeout(() => {
                        this.viewer.setCamera(cam.camera, duration);
                    }, delay);
                    // Use at least MIN_FRAME_DELAY to ensure each frame is visible
                    delay += Math.max(duration, MIN_FRAME_DELAY);
                }
            } else if (typeof camera === "object") {
                this.viewer.setCamera(camera.camera, camera.duration??0);
            }
            this.setState({camera: camera});
        }
    }
    isCompleteCameraSnapshot(snapshot) {
        const requiredKeys = Object.keys(Camera.createDefaultSnapshot());
        return snapshot && requiredKeys.every(key => snapshot[key] !== undefined);
    }
    updateCameraParameters(snapshot) {
        if (this.viewer._plugin.disposed) {
            return;
        }
        const snap = snapshot ?? this.viewer._plugin.canvas3d.camera.getSnapshot();

        if (!this.isCompleteCameraSnapshot(snap)) return;

        // Only trigger if camera actually changed
        if (!this.areCameraSnapshotsEqual(this.prevCameraSnapshot, snap)) {
            this.prevCameraSnapshot = snap;

            // Apply debounce for setProps callback
            const debounceMs = this.props.cameraDebounce ?? 100;
            if (debounceMs > 0) {
                if (this.cameraDebounceTimer) {
                    clearTimeout(this.cameraDebounceTimer);
                }
                this.cameraDebounceTimer = setTimeout(() => {
                    this.isInternalCameraUpdate = true;
                    this.setState({camera: snap});
                    if (this.props.setProps) {
                        this.props.setProps({camera: snap});
                    }
                }, debounceMs);
            } else {
                this.isInternalCameraUpdate = true;
                this.setState({camera: snap});
                if (this.props.setProps) {
                    this.props.setProps({camera: snap});
                }
            }
        }
    }
    handleScreenshotChange(screenshot) {
        if (screenshot) {
            this.viewer.downloadScreenshot(screenshot.filename, screenshot.params, screenshot.crop);
        }
    }
    bindingComponentToMolecule(data, model_index) {
        // binding structure ID to component
        if (Array.isArray(data.component)) {
            data.component.forEach((component) => {
                component.modelId = this.loadedStructures[model_index];
            });
        } else if (typeof data.component === "object") {
            data.component.modelId = this.loadedStructures[model_index];
        }
    }
    parseTargetsForPython(targets) {
        const chainsMap = new Map();

        for (const t of targets) {
            const chainKey = t.labelAsymId ?? '';
            if (!chainsMap.has(chainKey)) {
                chainsMap.set(chainKey, {
                    name: t.labelAsymId,
                    auth_name: t.authAsymId,
                    residues: []
                });
            }
            const chainObj = chainsMap.get(chainKey);

            let residueObj = chainObj.residues.find((r) =>
                r.index === t.labelSeqId &&
                r.ins_code === t.pdbxInsCode &&
                r.number === t.authSeqId &&
                r.name === t.labelCompId
            );
            if (!residueObj) {
                residueObj = {
                    name: t.labelCompId,
                    index: t.labelSeqId,
                    number: t.authSeqId,
                    ins_code: t.pdbxInsCode,
                    atoms: []
                };
                chainObj.residues.push(residueObj);
            }
            residueObj.atoms.push({
                name: t.labelAtomId,
                index: t.atomIndex,
                x: t.x,
                y: t.y,
                z: t.z
            });
        }
        return {chains: Array.from(chainsMap.values())};
    }
    parseTargetsFromPython(targets, modelId) {
        const parsedTargets = [];

        for (let target of targets) {
            const chains = target.chains;
            const auth = ('auth' in target) ? target.auth : false;
            for (const chain of chains) {
                const residues = chain.residues;
                // when residues are empty, push chain level object
                // if no residues are provided, we assume the user wants to select the whole chain
                if (!residues || residues.length === 0) {
                    parsedTargets.push({
                        auth: auth,
                        modelId: modelId,
                        labelAsymId: chain.name,
                        authAsymId: chain.auth_name
                    });
                    continue;
                }
                for (const residue of residues) {
                    const atoms = residue.atoms;
                    // when atoms are empty, push residue level object
                    // if no atoms are provided, we assume the user wants to select the whole residue
                    if (!atoms || atoms.length === 0) {
                        parsedTargets.push({
                            auth: auth,
                            modelId: modelId,
                            labelAsymId: chain.name,
                            authAsymId: chain.auth_name,
                            labelSeqId: residue.index,
                            authSeqId: residue.number,
                            pdbxInsCode: residue.ins_code,
                        });
                        continue;
                    }
                    for (const atom of atoms) {
                        parsedTargets.push({
                            auth: auth,
                            modelId: modelId,
                            labelAsymId: chain.name,
                            authAsymId: chain.auth_name,
                            labelSeqId: residue.index,
                            authSeqId: residue.number,
                            pdbxInsCode: residue.ins_code,
                            atomIndex: atom.index,
                        });
                    }
                }
            }
        }
        return parsedTargets;
    }
    parseTargetsForMoleculePresets(preset) {
        if (preset && preset.hasOwnProperty('target'))
            preset.target = this.parseTargetsFromPython(preset.target, null)[0];
        if (preset && preset.hasOwnProperty('focus'))
            preset.focus = this.parseTargetsFromPython(preset.focus, null)[0];
        if (preset && preset.hasOwnProperty('targets'))
            preset.targets = this.parseTargetsFromPython(preset.targets, null);
        if (preset && preset.hasOwnProperty('glycosylation'))
            preset.glycosylation = this.parseTargetsFromPython(preset.glycosylation, null);
        if (preset && preset.hasOwnProperty('colors'))
            for (let color of preset.colors)
                color.targets = this.parseTargetsFromPython(color.targets, null);
    }
    async loadData(data) {
        if (typeof data === "object") {
            const model_index = Object.keys(this.loadedStructures).length + 1;
            if (data.type === "mol") { // loading a structure
                // handle the target key in preset
                this.parseTargetsForMoleculePresets(data.preset);
                const matrix = data.matrix ? Mat4.fromArray(Mat4.zero(), data.matrix, 0) : undefined;
                const result = await this.viewer.loadStructureFromData(data.data, data.format, false, {props: data.preset, matrix: matrix});
                // add the structure ID to this.loadedStructures
                this.loadedStructures[model_index] = result.structure.cell.obj.data.units[0].model.id;
                // if user specified component(s), add them to the structure
                if (data.hasOwnProperty('component')) {
                    this.bindingComponentToMolecule(data, model_index);
                    await this.handleComponentChange(data.component);
                }
            } else if (data.type === 'url') { // loading a URL
                // load url for molecules
                if (data.urlfor === 'mol') { // loading a structure from URL
                    // handle the target key in preset
                    this.parseTargetsForMoleculePresets(data.preset);
                    const matrix = data.matrix ? Mat4.fromArray(Mat4.zero(), data.matrix, 0) : undefined;
                    const result = await this.viewer.loadStructureFromUrl(data.data, data.format, false, {props: data.preset, matrix: matrix});
                    // add the structure ID to this.loadedStructures
                    this.loadedStructures[model_index] = result.structure.cell.obj.data.units[0].model.id;
                    // if user specified component(s), add them to the structure
                    if (data.hasOwnProperty('component')) {
                        this.bindingComponentToMolecule(data, model_index);
                        await this.handleComponentChange(data.component);
                    }
                } else if (data.urlfor === 'snapshot') { // load url for molstar snapshot file
                    await this.viewer.loadSnapshotFromUrl(data.data, data.format);
                }
            } else if (data.type === 'traj') {
                const { topo, coords } = data;
                // handle the target key in preset
                this.parseTargetsForMoleculePresets(topo.preset);
                const matrix = topo.matrix ? Mat4.fromArray(Mat4.zero(), topo.matrix, 0) : undefined;
                const result = await this.viewer.loadTrajectory(topo, coords, {props: topo.preset, matrix: matrix});
                // add the structure ID to this.loadedStructures
                this.loadedStructures[model_index] = result.structure.cell.obj.data.units[0].model.id;
                // if user specified component(s), add them to the structure
                if (topo.hasOwnProperty('component')) {
                    this.bindingComponentToMolecule(topo, model_index);
                    await this.handleComponentChange(topo.component);
                }
            }
        }
    }
    async loadShape(data) {
        // if the provided data label existed, remove it first before creating a new one
        if (data.label && this.loadedShapes[data.label]) {
            this.viewer.removeRef(this.loadedShapes[data.label]);
            delete this.loadedShapes[data.label];
        }
        // creating new shapes
        let ref;
        if (data.shape === 'box') {
            ref = await this.viewer.createBoundingBox(data.label, data.min, data.max, data.radius, data.color, data.alpha);
        } else if (data.shape === 'sphere') {
            ref = await this.viewer.createSphere(data.label, data.center, data.radius, data.color, data.alpha, data.detail);
        } else if (data.shape === 'cylinder') {
            ref = await this.viewer.createCylinder(data.label, data.start, data.end, data.color, data.alpha, data.props, data.dashed, data.dash_segments);
        } else if (data.shape === 'plane') {
            ref = await this.viewer.createPlane(data.label, data.center, data.dirMajor, data.dirMinor, data.scaleX, data.scaleY, data.color, data.alpha, data.doubleSided);
        } else if (data.shape === 'axes') {
            ref = await this.viewer.createAxes(data.label, data.origin, data.dirA, data.dirB, data.dirC, data.color, data.alpha, data.radiusScale);
        } else if (data.shape === 'ellipsoid') {
            ref = await this.viewer.createEllipsoid(data.label, data.center, data.dirMajor, data.dirMinor, data.radiusScale, data.color, data.alpha, data.detail);
        } else if (data.shape === 'ribbon') {
            ref = await this.viewer.createRibbon(data.label, data.controlPoints, data.normalVectors, data.binormalVectors, data.widthValues, data.color, data.alpha, data.linearSegments, data.arrowHeight);
        } else if (data.shape === 'sheet') {
            ref = await this.viewer.createSheet(data.label, data.controlPoints, data.normalVectors, data.binormalVectors, data.widthValues, data.heightValues, data.color, data.alpha, data.linearSegments, data.arrowHeight, data.startCap, data.endCap);
        } else if (data.shape === 'tube') {
            ref = await this.viewer.createTube(data.label, data.controlPoints, data.normalVectors, data.binormalVectors, data.widthValues, data.heightValues, data.color, data.alpha, data.linearSegments, data.radialSegments, data.startCap, data.endCap, data.crossSection, data.roundCap);
        }
        if (ref) {
            this.loadedShapes[data.label] = ref;
        }
    }
    async addComponent(component) {
        // construct molstar target object from python helper data
        let targets = [];
        if (component.targets && component.targets[0] !== null) {
            // convert data from python to molstar data structure
            targets = this.parseTargetsFromPython(component.targets, component.modelId)
        }
        await this.viewer.createComponent(component.label, targets, component.representation);
    }
    async addMeasurement(measurement) {
        const model_index = this.viewer._plugin.managers.structure.hierarchy.current.structures.length - 1;
        if (model_index >= 0) {
            const id = this.viewer._plugin.managers.structure.hierarchy.current.structures[model_index].cell.obj.data.units[0].model.id;
            const targets = measurement.targets
            let parsed_targets = [];
            if (targets && targets[0] !== null) {
                targets.forEach((target) => {
                    parsed_targets.push(this.parseTargetsFromPython([target], id));
                })
            }
            await this.viewer.addMeasurement(parsed_targets, measurement.type);
        }
    }
    componentDidMount() {
        if (this.viewerRef.current) {
            this.viewer = new rcsbMolstar.Viewer(this.viewerRef.current, this.state.layout);

            // Wait for plugin to be fully initialized before loading data
            this.viewer._plugin.canvas3dInitialized.then(() => {
                // subscribe to focus change
                this.focusSubscription = this.viewer._plugin.managers.structure.focus.behaviors.current.subscribe(() => {
                    if (this.viewer._plugin.disposed) {
                        return;
                    }
                    if (this.viewer._plugin.managers.structure.focus.history.length > 0) {
                        const focusData = this.parseTargetsForPython(this.viewer.getCurrentFocus());
                        this.setState({focus: focusData});
                        if (this.props.setProps) {
                            this.props.setProps({focus: focusData});
                        }
                    }
                });

                // subscribe to selection change
                this.selectionSubscription = this.viewer._plugin.managers.structure.selection.events.changed.subscribe(() => {
                    if (this.viewer._plugin.disposed) {
                        return;
                    }
                    const selectionData = this.parseTargetsForPython(this.viewer.getCurrentSelection());
                    this.setState({selection: selectionData});
                    if (this.props.setProps) {
                        this.props.setProps({selection: selectionData});
                    }
                });

                // subscribe to frame change
                this.frameSubscription = this.viewer._plugin.state.data.events.changed.subscribe(({ state }) => {
                    if (this.viewer._plugin.disposed) {
                        return;
                    }
                    const frameData = this.viewer.getCurrentFrame(state);
                    this.setState({frame: frameData});
                    if (this.props.setProps) {
                        this.props.setProps({frame: frameData});
                    }
                    if (this.state.updatefocusonframechange) {
                        const focusData = this.parseTargetsForPython(this.viewer.getCurrentFocus());
                        this.setState({focus: focusData});
                    }
                    if (this.state.updateselectiononframechange) {
                        const selectionData = this.parseTargetsForPython(this.viewer.getCurrentSelection());
                        this.setState({selection: selectionData});
                    }
                });

                // subscribe to camera change
                if (this.state.cameraresponddrag) {
                    this.cameraSubscription = this.viewer._plugin.canvas3d.didDraw.subscribe(() => this.updateCameraParameters());
                } else {
                    this.cameraSubscription = this.viewer._plugin.canvas3d.camera.stateChanged.subscribe((state) => this.updateCameraParameters(state));
                }
                // Load initial data if provided
                if (this.state.data) {
                    this.handleDataChange(this.state.data);
                }
                if (this.state.selection) {
                    this.handleSelectionChange(this.state.selection);
                }
                if (this.state.hover) {
                    this.handleHoverChange(this.state.hover);
                }
                if (this.state.focus) {
                    this.handleFocusChange(this.state.focus);
                }
                if (this.state.frame) {
                    this.handleFrameChange(this.state.frame);
                }
                if (this.state.measurement) {
                    this.handleMeasurementChange(this.state.measurement);
                }
                if (this.state.camera) {
                    this.handleCameraChange(this.state.camera);
                }
                if (this.state.screenshot) {
                    this.handleScreenshotChange(this.state.screenshot);
                }
                if (this.state.updatefocusonframechange) {
                    this.setState({updatefocusonframechange: this.props.updatefocusonframechange});
                }
                if (this.state.updateselectiononframechange) {
                    this.setState({updateselectiononframechange: this.props.updateselectiononframechange});
                }
            });
        }
    }
    componentDidUpdate(prevProps) {
        if (this.props.data !== prevProps.data) {
            this.handleDataChange(this.props.data);
        }
        if (this.props.selection !== prevProps.selection) {
            this.handleSelectionChange(this.props.selection);
        }
        if (this.props.hover !== prevProps.hover) {
            this.handleHoverChange(this.props.hover);
        }
        if (this.props.focus !== prevProps.focus) {
            this.handleFocusChange(this.props.focus);
        }
        if (this.props.frame !== prevProps.frame) {
            this.handleFrameChange(this.props.frame);
        }
        if (this.props.measurement !== prevProps.measurement) {
            this.handleMeasurementChange(this.props.measurement);
        }
        if (this.props.camera !== prevProps.camera) {
            if (this.isInternalCameraUpdate) {
                this.isInternalCameraUpdate = false;
            } else {
                this.handleCameraChange(this.props.camera);
            }
        }
        if (this.props.screenshot !== prevProps.screenshot) {
            this.handleScreenshotChange(this.props.screenshot);
        }
        if (this.props.updatefocusonframechange !== prevProps.updatefocusonframechange) {
            this.setState({updatefocusonframechange: this.props.updatefocusonframechange});
        }
        if (this.props.updateselectiononframechange !== prevProps.updateselectiononframechange) {
            this.setState({updateselectiononframechange: this.props.updateselectiononframechange});
        }
    }

    componentWillUnmount() {
        this.cleanupViewer();
    }

    cleanupViewer() {
        // Clear debounce timer
        if (this.cameraDebounceTimer) {
            clearTimeout(this.cameraDebounceTimer);
            this.cameraDebounceTimer = null;
        }
        // unsubscribe from all events
        this.focusSubscription.unsubscribe();
        this.focusSubscription = null;
        this.selectionSubscription.unsubscribe();
        this.selectionSubscription = null;
        this.frameSubscription.unsubscribe();
        this.frameSubscription = null;
        this.cameraSubscription.unsubscribe();
        this.cameraSubscription = null;
        this.viewer._plugin.dispose();
        this.viewer = null;

        this.loadedShapes = {};
        this.loadedStructures = {};
    }

    render() {
        return (<div 
            id={this.props.id} 
            ref={this.viewerRef} 
            style={this.state.style}
            className={this.state.className}
            data={this.state.data}
            layout={this.state.layout}
            selection={this.state.selection}
            hover={this.state.hover}
            focus={this.state.focus}
            frame={this.state.frame}
            measurement={this.state.measurement}
            camera={this.state.camera}
            cameradebounce={this.state.cameradebounce}
            cameraresponddrag={this.state.cameraresponddrag}
            screenshot={this.state.screenshot}
            updatefocusonframechange={this.state.updatefocusonframechange}
            updateselectiononframechange={this.state.updateselectiononframechange}
            />
        );
    }
}

MolstarViewer.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The HTML property `style` to control the appearence of the container of molstar viewer.
     */
    style: PropTypes.object,

    /**
     * The HTML property `class` for additional class names of the container of molstar viewer.
     */
    className: PropTypes.string,

    /**
     * Data containing the structure info that should be loaded into molstar viewer, as well as some control flags.
     * The data can be generated with python method `parse_molecule`.
     */
    data: PropTypes.any,

    /**
     * The layout of the molstar viewer. Determining what controls to be displayed. 
     * 
     * The layout is not allowed to be changed once the component has been initialized.
     */
    layout: PropTypes.object,

    /**
     * The structure region to be selected in the molstar viewer.
     */
    selection: PropTypes.object,

    /**
     * The structure region to be hovered in the molstar viewer.
     */
    hover: PropTypes.object,

    /**
     * The structure region to let the camera focus on in the molstar viewer.
     */
    focus: PropTypes.object,

    /**
     * The trajectory frame in the molstar viewer.
     */
    frame: PropTypes.number,

    /**
     * The measurements in the molstar viewer.
     */
    measurement: PropTypes.any,

    /**
     * The camera object in the molstar viewer.
     */
    camera: PropTypes.any,

    /**
     * Debounce time in milliseconds for camera change events.
     * Set to 0 to disable debounce. Default is 100ms.
     */
    cameradebounce: PropTypes.number,

    /**
     * Whether to respond to drag events of the camera.
     * Set to false to disable camera parameter updates while dragging
     * with mouse keys, or scrolling.
     */
    cameraresponddrag: PropTypes.bool,

    /**
     * The screenshot object containing the options for taking 
     * screenshot of the current view in molstar viewer.
     */
    screenshot: PropTypes.object,

    /**
     * Update focus data when frame index have changed.
     */
    updatefocusonframechange: PropTypes.bool,

    /**
     * Update selection data when frame index have changed.
     */
    updateselectiononframechange: PropTypes.bool,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};
