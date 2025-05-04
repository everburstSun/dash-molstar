# AUTO GENERATED FILE - DO NOT EDIT

#' @export
molstarViewer <- function(id=NULL, className=NULL, data=NULL, focus=NULL, frame=NULL, layout=NULL, selection=NULL, style=NULL) {
    
    props <- list(id=id, className=className, data=data, focus=focus, frame=frame, layout=layout, selection=selection, style=style)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'MolstarViewer',
        namespace = 'dash_molstar',
        propNames = c('id', 'className', 'data', 'focus', 'frame', 'layout', 'selection', 'style'),
        package = 'dashMolstar'
        )

    structure(component, class = c('dash_component', 'list'))
}
