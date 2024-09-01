import React, {Component, createRef} from 'react';
import PropTypes from 'prop-types';

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
            data: props.data,
            layout: defaultLayout,
            style: defaultStyle,
            className: props.className,
            selection: props.selection,
            focus: props.focus
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
        this.setState({selection: selection});
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
        this.setState({focus: focus});
    }
    loadData(data) {
        if (typeof data === "object") {
            if (data.type === "mol") {
                // first load the structure into viewer
                this.viewer.loadStructureFromData(data.data, data.format, false, {props: data.preset}).then(() => {
                    // if user specified component(s), add them to the structure
                    if (data.hasOwnProperty('component')) {
                        this.handleComponentChange(data.component);
                    }
                });
            } else if (data.type === 'url') {
                // load url for molecules
                if (data.urlfor === 'mol') {
                    this.viewer.loadStructureFromUrl(data.data, data.format, false, {props: data.preset}).then(() => {
                        if (data.hasOwnProperty('component')) {
                            this.handleComponentChange(data.component);
                        }
                    });
                } else {
                    // load url for molstar snapshot file
                    this.viewer.loadSnapshotFromUrl(data.data, data.format);
                }
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
            this.viewer.createBoundingBox(data.label, data.min, data.max, data.radius, data.color).then((ref) => {
            this.loadedShapes[data.label] = ref;
        });
        // } else if (data.shape === 'sphere') {
        //     this.viewer.createSphere(data.label, data.center, data.radius, data.color).then((ref) => {
        //     this.loadedShapes[data.label] = ref;
        }//);
    }
    addComponent(component) {
        // check if there was any structure loaded in the viewer
        const model_index = this.viewer._plugin.managers.structure.hierarchy.current.structures.length - 1;
        if (model_index >= 0) {
            // get molstar internal structure ID for the last loaded model
            const id = this.viewer._plugin.managers.structure.hierarchy.current.structures[model_index].cell.obj.data.units[0].model.id;
            // construct molstar target object from python helper data
            const targets = [];
            for (let target of component.targets) {
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
            this.viewer.createComponent(component.label, targets, component.representation);
        }
    }
    componentDidMount() {
        if (this.viewerRef.current) {
            this.viewer = new rcsbMolstar.Viewer(this.viewerRef.current, this.state.layout);
            if (this.state.data) {
                this.handleDataChange(this.state.data);
            }
            if (this.state.selection) {
                this.handleSelectionChange(this.state.selection);
            }
            if (this.state.focus) {
                this.handleFocusChange(this.state.focus);
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
    }

    render() {
        return (<div 
            id={this.props.id} 
            ref={this.viewerRef} 
            style={this.state.style}
            className={this.state.className}
            data={this.props.data}
            layout={this.state.layout}
            selection={this.props.selection}
            focus={this.props.focus}
            />
        );
    }
}

MolstarViewer.defaultProps = {};

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
    setProps: PropTypes.func
};
