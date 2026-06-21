# AUTO GENERATED FILE - DO NOT EDIT

#' @export
molstarViewer <- function(id=NULL, camera=NULL, cameradebounce=NULL, cameraresponddrag=NULL, className=NULL, data=NULL, focus=NULL, frame=NULL, hover=NULL, layout=NULL, measurement=NULL, screenshot=NULL, selection=NULL, style=NULL, updatefocusonframechange=NULL, updateselectiononframechange=NULL) {
    
    props <- list(id=id, camera=camera, cameradebounce=cameradebounce, cameraresponddrag=cameraresponddrag, className=className, data=data, focus=focus, frame=frame, hover=hover, layout=layout, measurement=measurement, screenshot=screenshot, selection=selection, style=style, updatefocusonframechange=updatefocusonframechange, updateselectiononframechange=updateselectiononframechange)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'MolstarViewer',
        namespace = 'dash_molstar',
        propNames = c('id', 'camera', 'cameradebounce', 'cameraresponddrag', 'className', 'data', 'focus', 'frame', 'hover', 'layout', 'measurement', 'screenshot', 'selection', 'style', 'updatefocusonframechange', 'updateselectiononframechange'),
        package = 'dashMolstar'
        )

    structure(component, class = c('dash_component', 'list'))
}
