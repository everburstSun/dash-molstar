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
            component: props.component,
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
        
        this.setState({component: component});
    }
    handleSelectionChange(selection) {
        
        this.setState({selection: selection});
    }
    handleFocusChange(focus) {
        
        this.setState({focus: focus});
    }
    loadData(data) {
        if (typeof data === "object") {
            if (data.type === "mol") {
                this.viewer.loadStructureFromData(data.data, data.format, false);
            } else if (data.type === 'shape') {
                this.loadShape(data);
            }
        }
    }
    loadShape(data) {
        
    }
    componentDidMount() {
        if (this.viewerRef.current) {
            this.viewer = new rcsbMolstar.Viewer(this.viewerRef.current, this.state.layout);
            if (this.state.data) {
                const { data } = this.state.data;
                if (Array.isArray(data)) {
                    data.forEach((obj) => {
                        this.loadData(obj);
                    });
                } else if (typeof data === "object") {
                    this.loadData(data);
                }
            }
        }
    }
    componentDidUpdate(prevProps) {
        if (this.props.data !== prevProps.data) {
          this.handleDataChange(this.props.data);
        }
        if (this.props.component !== prevProps.component) {
          this.handleComponentChange(this.props.component);
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
            component={this.props.component}
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
     * The data can be generated with python method `parse_for_molstar`.
     */
    data: PropTypes.any,

    /**
     * The layout of the molstar viewer. Determining what controls to be displayed. 
     * 
     * The layout is not allowed to be changed once the component has been initialized.
     */
    layout: PropTypes.object,
    
    /**
     * The additional components to be created in the molstar viewer. Leave it undefined to keep the molstar default settings.
     */
    component: PropTypes.object,
    
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
