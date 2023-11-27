import React, { Component, createRef } from 'react';
import PropTypes from 'prop-types';
import { Vec3, Mat3 } from 'molstar/lib/mol-math/linear-algebra';
import { changeCameraRotation, structureLayingTransform } from 'molstar/lib/mol-plugin-state/manager/focus-camera/orient-axes';
import { Structure } from 'molstar/lib/mol-model/structure/structure';
import _ from 'lodash';

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
            showMembraneOrientationPreset: false,
            showNakbColorTheme: false,
            detachedFromSierra: true,
            layoutIsExpanded: false,
            layoutShowControls: false,
            layoutControlsDisplay: 'reactive',
            layoutShowSequence: true,
            layoutShowLog: false,
            viewportShowExpand: true,
            viewportShowSelectionMode: true,
            showWelcomeToast: false,
        };
        const defaultStyle = {
            'zIndex': 10,
            'position': 'relative'
        };
        this.state = {
            data: props.data || [],
            layout: defaultLayout,
            style: defaultStyle,
            className: props.className,
            selection: props.selection,
            //focus: props.focus,
        };


        this.loadedShapes = {};
        this.loadedStructures = {};
        this.loadedComponents = {};
        this.loadedSnapshots = {};

        this.setProps = props.setProps;
        this.viewerRef = createRef();
        const updatedLayout = Object.assign({}, this.state.layout, props.layout);
        this.state.layout = updatedLayout;
        const updatedStyle = Object.assign({}, this.state.style, props.style);
        this.state.style = updatedStyle;
    }


    getStructureByLabel(name) {
        for (const structure of this.viewer._plugin.managers.structure.hierarchy.current.structures) {
            if (structure.cell.obj.data.state.label === name) {
                return structure;
            }
        }
    }

    getStructuresByLabel(name) {
        return this.viewer._plugin.managers.structure.hierarchy.current.structures.filter((structure) => structure.cell.obj.data.state.label === name);
    }

    syncItems() {
        let items = this.state.data;

        if (!Array.isArray(items)) {
            items = [items];
        }

        const structureItems = items.filter((item) => item.type === 'mol' || item.type === 'url');
        const shapeItems = items.filter((item) => item.type === 'shape');

        // sync structures  
        let newLabels = [];
        structureItems.forEach((item) => {
            const label = item.hasOwnProperty('label') ? item.label : '';
            newLabels.push(label);
            this.syncStructure(label, item);
        });
        for (const [label, ref] of Object.entries(this.loadedStructures)) {
            if (!newLabels.includes(label)) {
                delete this.loadedComponents[label];
                this.getStructuresByLabel(label).forEach((structure) => {

                    this.viewer.removeRef(structure.cell.sourceRef);
                });
                delete this.loadedStructures[label];
            }
        };

        // sync shapes
        newLabels = [];
        shapeItems.forEach((item) => {
            const label = item.hasOwnProperty('label') ? item.label : '';
            newLabels.push(label);
            this.syncShape(item);
        });
        for (const [label, ref] of Object.entries(this.loadedShapes)) {
            if (!newLabels.includes(label)) {
                this.viewer.removeRef(ref);
                delete this.loadedShapes[label];
            }
        };
    }

    syncAutoFocus(focus=false) {
        focus && this.props.setProps({ focus: {
            molecule: this.state.data[this.state.data.length - 1]?.label
        }});
    }

    autoRotate(structures, rotate = false) {
        if (!rotate) {
            return;
        }
        const { rotation } = structureLayingTransform(structures);
        const x = Mat3.create(
            Math.cos(Math.PI / 180 * 180),
            Math.sin(Math.PI / 180 * 180),
            0,
            -Math.sin(Math.PI / 180 * 180),
            Math.cos(Math.PI / 180 * 180),
            0,
            0,
            0,
            1,
        );
        const newViewMatrix = Mat3.mul(Mat3(), rotation, x);
        const newSnapshot = changeCameraRotation(this.viewer._plugin.canvas3d.camera.getSnapshot(), newViewMatrix);
        const durationMs = 10;
        this.viewer._plugin.managers.camera.setSnapshot(newSnapshot, durationMs);
    }

    syncStructure(label, item) {
        if (!this.loadedStructures[label]) {
            this.loadedStructures[label] = 1;
            if (item.type === "mol") {
                this.viewer.loadStructureFromData(item.data, item.format, false, { props: { dataLabel: label } }).then((x) => {
                    this.loadedStructures[label] = 2;
                    item.hasOwnProperty('component') && this.syncComponent(label, item.component);
                    this.autoRotate([x.structure.data]);
                    this.syncAutoFocus(item.focus);
                });
            } else if (item.type === "url") {
                if (item.urlfor === 'mol') {
                    this.viewer.loadStructureFromUrl(item.data, item.format, false).then((x) => {
                        this.loadedStructures[label] = 2;
                        item.hasOwnProperty('component') && this.syncComponent(label, item.component);
                        this.autoRotate([x.structure.data]);
                        this.syncAutoFocus(item.focus);
                    });
                } else {
                    this.viewer.loadSnapshotFromUrl(item.data, item.format).then((x) => {
                        this.loadedSnapshots[label] = x.snapshot.ref;
                        this.autoRotate([x.structure.data]);
                        this.syncAutoFocus(item.focus);
                    });
                }
            }
        } if ((item.type === "mol" || (item.type === 'url' && item.urlfor === 'mol')) && this.loadedStructures[label] === 2) {
            item.hasOwnProperty('component') && this.syncComponent(label, item.component);
        }
    }


    syncComponent(label, components) {
        components = components || [];
        if (!Array.isArray(components)) {
            components = [components];
        }
        const loadedComponents = this.loadedComponents[label] || [];
        this.loadedComponents[label] = loadedComponents;
        const structure = this.getStructureByLabel(label);
        const id = structure.cell.obj.data.units[0].model.id;
        components.forEach((component) => {
            let componentLabel = component.hasOwnProperty('label') ? component.label : '';
            if (componentLabel === 'Polymer') {
                this.viewer.removeComponent(componentLabel);
            }
            componentLabel = `${label}.${componentLabel}`;

            if (!loadedComponents.includes(componentLabel)) {

                const targets = [];
                for (let target of component.targets) {
                    const newTarget = {
                        modelId: id,
                        ...target.author ? { authAsymId: target.chain_name } : { labelAsymId: target.chain_name },
                    }
                    if (target.hasOwnProperty('residue_numbers')) {
                        if (target.author) {
                            newTarget.authSeqId = target.residue_numbers;
                        } else {
                            newTarget.labelSeqId = target.residue_numbers;
                        }
                    }
                    targets.push(newTarget);
                }

                this.viewer.createComponent(componentLabel, targets, component.representation);
            }
            loadedComponents.push(componentLabel);
        });

        structure.components.forEach((component) => {
            const componentLabel = component.cell.obj.data.label;
            if (!loadedComponents.includes(componentLabel) && componentLabel.startsWith(`${label}.`)) {
                this.viewer.removeComponent(componentLabel);
                // remove from list
                loadedComponents.splice(loadedComponents.indexOf(componentLabel), 1);
            }
        });
    }


    getSelectionSubStructure(){
        const structure = this.viewer._plugin.managers.structure.selection.entries.values().next().value._selection.structure;
        const elements = this.viewer._plugin.managers.structure.selection.entries.values().next().value._selection.elements[0].unit.elements;
        const indices = this.viewer._plugin.managers.structure.selection.entries.values().next().value._selection.elements[0].indices;
        const elementIds = indices.map(index => elements[index]);

        const builder = Structure.Builder()
        const elementSet = new Set(elementIds)
        for (const unit of structure.units) {
            const elements = elementIds
            ? [...(unit.elements)].filter((item) => elementSet.has(item))
            : unit.elements
            if (elements.length) {
            builder.addUnit(
                unit.kind,
                unit.model,
                unit.conformation.operator,
                elements,
                unit.traits
            )
            }
        }
        return builder.getStructure()
    }

    syncSelections() {
        const selection = this.state.selection;
        if (!selection) {
            this.viewer.clearSelection("select");
            this.viewer.clearSelection("hover");
            return;
        }
        const molecule_name = this.state.selection.molecule;
        let structure = null;
        if (!molecule_name) {
            const model_index = this.viewer._plugin.managers.structure.hierarchy.current.structures.length - 1;
            structure = this.viewer._plugin.managers.structure.hierarchy.current.structures[model_index];
        } else {
            structure = this.getStructureByLabel(molecule_name);
        }

        const id = structure.cell.obj.data.units[0].model.id;
        const targets = [];
        if (selection.targets) {
            // convert data from python to molstar data structure
            for (let target of selection.targets) {
                const newTarget = {
                    modelId: id,
                    ...target.auth ? { authAsymId: target.chain_name } : { labelAsymId: target.chain_name },
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
        const subStructure = this.getSelectionSubStructure();
        this.autoRotate([subStructure], selection.rotate);
    }

    syncFocus() {
        const focus = this.props.focus;
        if (!focus) {
            this.viewer.clearFocus();
            return;
        }
        const molecule_name = focus?.molecule
        if (!molecule_name) {
            return;
        }
        let currentComponents = null;
        const componentGroups = this.viewer._plugin.managers.structure.hierarchy.currentComponentGroups;
        for (let i = 0; i < componentGroups.length; i++) {
            currentComponents = componentGroups[i].filter(e => e.cell.obj.data.state.label === molecule_name);
            if (currentComponents.length) {
                break;
            }
        }

        if (!currentComponents || !currentComponents.length) {
            return;
        }

        this.viewer._plugin.managers.camera.focusSpheres(currentComponents, e => {
            if (e.cell.state.isHidden) return;
            return e.cell.obj?.data.boundary.sphere;
        });
    }

    syncShape(item) {
        if (this.loadedShapes[item.label]) {
            return;
        }
        if (item.shape === 'box') {
            this.viewer.createBoundingBox(item.label, item.min, item.max, item.radius, item.color).then((ref) => {
                this.loadedShapes[item.label] = ref;
            });
        }
    }


    syncViewerState() {
        this.syncItems();
        this.syncFocus();
        this.syncSelections();
    }

    componentDidMount() {
        if (this.viewerRef.current) {
            this.viewer = new rcsbMolstar.Viewer(this.viewerRef.current, this.state.layout);
            this.syncViewerState();
        }
        let timeoutid = null;
        if (this.viewerRef.current) {
            this.resizeObserver = new ResizeObserver((entries) => {
                for (const entry of entries) {
                    timeoutid && clearTimeout(timeoutid);
                    timeoutid = setTimeout(this.viewer.handleResize.bind(this.viewer), 100);
                }
            });
            this.resizeObserver.observe(this.viewerRef.current);
        }
    }

    componentDidUpdate(prevProps) {
        if (this.props.data !== prevProps.data) {
            const data = _.differenceWith(prevProps.data, this.props.data, _.isEqual);
            if (data && data.length) {
                for (let d of data) {
                    d.label && this.viewer.removeComponent(d.label);
                }
            }
            this.state.data = this.props.data || [];
            this.syncItems();
        }
        if (this.props.selection !== prevProps.selection) {
            this.state.selection = this.props.selection;
            this.syncSelections();
        }
        if (this.state.focus !== this.props.focus) {
            this.state.focus = this.props.focus;
            this.syncFocus();
        }
    }

    render() {
        return (<div
            id={this.props.id}
            ref={this.viewerRef}
            style={this.state.style}
            className={this.state.className}
        />
        );
    }
}


MolstarViewer.defaultProps = {
    data: [],
};


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
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,
};