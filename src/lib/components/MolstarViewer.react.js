import React, {Component, createRef} from 'react';
import PropTypes from 'prop-types';
import {ColorNames} from 'molstar/lib/mol-util/color/names';

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
            focus: props.focus,
            frame: props.frame,
            updatefocusonframechange: props.updatefocusonframechange,
            updateselectiononframechange: props.updateselectiononframechange,
        };
        this.loadedShapes = {};
        this.loadedStructures = {};
        this.viewerRef = createRef();
        const updatedLayout = Object.assign({}, this.state.layout, props.layout);
        this.state.layout = updatedLayout;
        const updatedStyle = Object.assign({}, this.state.style, props.style);
        this.state.style = updatedStyle;
    }
    handleDataChange(data) {
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
            if (Array.isArray(data)) {
                data.forEach((obj) => {
                    this.loadData(obj);
                });
            } else if (typeof data === "object") {
                this.loadData(data);
            }
        }
        this.setState({data: data});
    }
    handleComponentChange(component) {
        if (component) {
            if (Array.isArray(component)) {
                component.forEach((obj) => {
                    this.addComponent(obj);
                });
            } else if (typeof component === "object") {
                this.addComponent(component);
            }
        }
    }
    handleSelectionChange(selection) {
        const model_index = this.viewer._plugin.managers.structure.hierarchy.current.structures.length - 1;
        if (model_index >= 0) {
            const id = this.viewer._plugin.managers.structure.hierarchy.current.structures[model_index].cell.obj.data.units[0].model.id;
            const targets = [];
            if (selection.targets && selection.targets[0] !== null) {
                // convert data from python to molstar data structure
                for (let target of selection.targets) {
                    const newTarget = {
                        modelId: id,
                        ...target.auth ? {authAsymId: target.chain_name} : {labelAsymId: target.chain_name},
                    }
                    // check if any residue number has been selected
                    if (target.hasOwnProperty('residue_numbers')) {
                        if (target.auth) {
                            newTarget.authSeqId = target.residue_numbers;
                        } else {
                            newTarget.labelSeqId = target.residue_numbers;
                        }
                    }
                    targets.push(newTarget);
                }
            }
            this.viewer.select(targets, selection.mode, selection.modifier);
        }
        this.setState({selection: this.viewer.getCurrentSelection()});
    }
    handleFocusChange(focus) {
        const model_index = this.viewer._plugin.managers.structure.hierarchy.current.structures.length - 1;
        if (model_index >= 0) {
            const id = this.viewer._plugin.managers.structure.hierarchy.current.structures[model_index].cell.obj.data.units[0].model.id;
            const targets = [];
            if (focus.targets && focus.targets[0] !== null) {
                // convert data from python to molstar data structure
                for (let target of focus.targets) {
                    const newTarget = {
                        modelId: id,
                        ...target.auth ? {authAsymId: target.chain_name} : {labelAsymId: target.chain_name},
                    }
                    // check if any residue number has been selected
                    if (target.hasOwnProperty('residue_numbers')) {
                        if (target.auth) {
                            newTarget.authSeqId = target.residue_numbers;
                        } else {
                            newTarget.labelSeqId = target.residue_numbers;
                        }
                    }
                    targets.push(newTarget);
                }
            }
            this.viewer.setFocus(targets, focus.analyse);
        }
        this.setState({focus: this.viewer.getCurrentFocus()});
    }
    handleFrameChange(frame_index) {
        if (Object.keys(this.loadedStructures).length != 0) {
            if (typeof frame_index === 'number') {
                this.viewer.setFrame(frame_index);
            }
            this.setState({frame: frame_index});
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
    loadData(data) {
        if (typeof data === "object") {
            const model_index = Object.keys(this.loadedStructures).length + 1;
            if (data.type === "mol") { // loading a structure
                this.viewer.loadStructureFromData(data.data, data.format, false, {props: data.preset})
                .then((result) => {
                    // add the structure ID to this.loadedStructures
                    this.loadedStructures[model_index] = result.structure.cell.obj.data.units[0].model.id;
                    // if user specified component(s), add them to the structure
                    if (data.hasOwnProperty('component')) {
                        this.bindingComponentToMolecule(data, model_index);
                        this.handleComponentChange(data.component);
                    }
                });
            } else if (data.type === 'url') { // loading a URL
                // load url for molecules
                if (data.urlfor === 'mol') { // loading a structure from URL
                    this.viewer.loadStructureFromUrl(data.data, data.format, false, {props: data.preset})
                    .then((result) => {
                        // add the structure ID to this.loadedStructures
                        this.loadedStructures[model_index] = result.structure.cell.obj.data.units[0].model.id;
                        // if user specified component(s), add them to the structure
                        if (data.hasOwnProperty('component')) {
                            this.bindingComponentToMolecule(data, model_index);
                            this.handleComponentChange(data.component);
                        }
                    });
                } else if (data.urlfor === 'snapshot') { // load url for molstar snapshot file
                    this.viewer.loadSnapshotFromUrl(data.data, data.format);
                }
            } else if (data.type === 'traj') {
                const { topo, coords } = data;
                this.viewer.loadTrajectory(topo, coords, {props: topo.preset})
                .then((result) => {
                    // add the structure ID to this.loadedStructures
                    this.loadedStructures[model_index] = result.structure.cell.obj.data.units[0].model.id;
                    // if user specified component(s), add them to the structure
                    if (topo.hasOwnProperty('component')) {
                        this.bindingComponentToMolecule(topo, model_index);
                        this.handleComponentChange(topo.component);
                    }
                });
            } else if (data.type === 'shape') {
                this.loadShape(data);
            }
        }
    }
    loadShape(data) {
        // if the provided data label existed, remove it first before creating a new one
        if (data.label && this.loadedShapes[data.label]) {
            this.viewer.removeRef(this.loadedShapes[data.label]);
            delete this.loadedShapes[data.label];
        }
        // creating new shapes
        if (data.shape === 'box') {
            this.viewer.createBoundingBox(data.label, data.min, data.max, data.radius, data.color, data.alpha).then((ref) => {
            this.loadedShapes[data.label] = ref;
        });
        } else if (data.shape === 'sphere') {
            this.viewer.createSphere(data.label, data.center, data.radius, data.color, data.alpha, data.detail).then((ref) => {
            this.loadedShapes[data.label] = ref;
        })};
    }
    addComponent(component) {
        // construct molstar target object from python helper data
        const targets = [];
        for (let target of component.targets) {
            const newTarget = {
                modelId: component.modelId,
                ...target.auth ? {authAsymId: target.chain_name} : {labelAsymId: target.chain_name},
            }
            // check if any residue number has been selected
            if (target.hasOwnProperty('residue_numbers')) {
                if (target.auth) {
                    newTarget.authSeqId = target.residue_numbers;
                } else {
                    newTarget.labelSeqId = target.residue_numbers;
                }
            }
            targets.push(newTarget);
        }
        this.viewer.createComponent(component.label, targets, component.representation);
    }
    componentDidMount() {
        if (this.viewerRef.current) {
            this.viewer = new rcsbMolstar.Viewer(this.viewerRef.current, this.state.layout);

            // subscribe to focus change
            this.viewer._plugin.managers.structure.focus.behaviors.current.subscribe(() => {
                this.setState({focus: this.viewer.getCurrentFocus()});
                this.props.setProps({focus: this.viewer.getCurrentFocus()});
            });

            // subscribe to selection change
            this.viewer._plugin.managers.structure.selection.events.changed.subscribe(() => {
                this.setState({selection: this.viewer.getCurrentSelection()});
                this.props.setProps({selection: this.viewer.getCurrentSelection()});
            });

            // subscribe to frame change
            this.viewer._plugin.state.data.events.changed.subscribe(({ state }) => {
                this.setState({frame: this.viewer.getCurrentFrame(state)});
                this.props.setProps({frame: this.viewer.getCurrentFrame(state)});
                if (this.state.updatefocusonframechange) {
                    this.setState({focus: this.viewer.getCurrentFocus()});
                }
                if (this.state.updateselectiononframechange) {
                    this.setState({selection: this.viewer.getCurrentSelection()});
                }
            });

            if (this.state.data) {
                this.handleDataChange(this.state.data);
            }
            if (this.state.selection) {
                this.handleSelectionChange(this.state.selection);
            }
            if (this.state.focus) {
                this.handleFocusChange(this.state.focus);
            }
            if (this.state.frame) {
                this.handleFrameChange(this.state.frame);
            }
            if (this.state.updatefocusonframechange) {
                this.setState({updatefocusonframechange: this.props.updatefocusonframechange});
            }
            if (this.state.updateselectiononframechange) {
                this.setState({updateselectiononframechange: this.props.updateselectiononframechange});
            }
        }
    }
    componentDidUpdate(prevProps) {
        if (this.props.data !== prevProps.data) {
            this.handleDataChange(this.props.data);
        }
        if (this.props.selection !== prevProps.selection) {
            this.handleSelectionChange(this.props.selection);
        }
        if (this.props.focus !== prevProps.focus) {
            this.handleFocusChange(this.props.focus);
        }
        if (this.props.frame !== prevProps.frame) {
            this.handleFrameChange(this.props.frame);
        }
        if (this.props.updatefocusonframechange !== prevProps.updatefocusonframechange) {
            this.setState({updatefocusonframechange: this.props.updatefocusonframechange});
        }
        if (this.props.updateselectiononframechange !== prevProps.updateselectiononframechange) {
            this.setState({updateselectiononframechange: this.props.updateselectiononframechange});
        }
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
            focus={this.state.focus}
            frame={this.state.frame}
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
     * The structure region to let the camera focus on in the molstar viewer.
     */
    focus: PropTypes.object,

    /**
     * The trajectory frame in the molstar viewer.
     */
    frame: PropTypes.number,

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
