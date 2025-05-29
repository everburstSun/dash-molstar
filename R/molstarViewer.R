# AUTO GENERATED FILE - DO NOT EDIT

#' @export
molstarViewer <- function(id=NULL, className=NULL, data=NULL, focus=NULL, frame=NULL, hover=NULL, layout=NULL, measurement=NULL, selection=NULL, style=NULL, updatefocusonframechange=NULL, updateselectiononframechange=NULL) {
    
    props <- list(id=id, className=className, data=data, focus=focus, frame=frame, hover=hover, layout=layout, measurement=measurement, selection=selection, style=style, updatefocusonframechange=updatefocusonframechange, updateselectiononframechange=updateselectiononframechange)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'MolstarViewer',
        namespace = 'dash_molstar',
        propNames = c('id', 'className', 'data', 'focus', 'frame', 'hover', 'layout', 'measurement', 'selection', 'style', 'updatefocusonframechange', 'updateselectiononframechange'),
        package = 'dashMolstar'
        )

    structure(component, class = c('dash_component', 'list'))
}
