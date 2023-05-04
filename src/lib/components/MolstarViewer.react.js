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
            'z-index': 10,
            'position': 'relative'
        };
        this.state = {
            data: props.data,
            layout: defaultLayout,
            style: defaultStyle,
            selection: props.selection,
            focus: props.focus
        };
        this.viewerRef = createRef();
        const updatedLayout = Object.assign({}, this.state.layout, props.layout);
        this.state.layout = updatedLayout;
        const updatedStyle = Object.assign({}, this.state.style, props.style);
        this.state.style = updatedStyle;
    }
    handleDataChange(data) {
        this.viewer.clear();
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
            if (selection.targets) {
                for (let target of selection.targets) {
                    const newTarget = {
                        modelId: id,
                        labelAsymId: target.chain_name,
                    }
                    if (target.hasOwnProperty('residue_numbers')) {
                        for (let number of target.residue_numbers) {
                            const newTargetWithSeqId = Object.assign({}, newTarget, {labelSeqId: number});
                            targets.push(newTargetWithSeqId);
                        }
                    } else {
                        targets.push(newTarget);
                    }
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
            if (focus.targets) {
                for (let target of focus.targets) {
                    const newTarget = {
                        modelId: id,
                        labelAsymId: target.chain_name,
                    }
                    if (target.hasOwnProperty('residue_numbers')) newTarget.labelSeqId = target.residue_numbers
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
                this.viewer.loadStructureFromData(data.data, data.format, false).then(() => {
                    // if user specified component(s), add them to the structure
                    if (data.hasOwnProperty('component')) {
                        this.handleComponentChange(data.component);
                    }
                });
            } else if (data.type === 'shape') {
                this.loadShape(data);
            }
        }
    }
    loadShape(data) {
        
    }
    addComponent(component) {
        const model_index = this.viewer._plugin.managers.structure.hierarchy.current.structures.length - 1;
        if (model_index >= 0) {
            const id = this.viewer._plugin.managers.structure.hierarchy.current.structures[model_index].cell.obj.data.units[0].model.id;
            const targets = [];
            for (let target of component.targets) {
                const newTarget = {
                    modelId: id,
                    labelAsymId: target.chain_name,
                }
                if (target.hasOwnProperty('residue_numbers')) newTarget.labelSeqId = target.residue_numbers
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
