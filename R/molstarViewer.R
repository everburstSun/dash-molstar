# AUTO GENERATED FILE - DO NOT EDIT

#' @export
molstarViewer <- function(id=NULL, data=NULL, focus=NULL, layout=NULL, selection=NULL, style=NULL) {
    
    props <- list(id=id, data=data, focus=focus, layout=layout, selection=selection, style=style)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'MolstarViewer',
        namespace = 'dash_molstar',
        propNames = c('id', 'data', 'focus', 'layout', 'selection', 'style'),
        package = 'dashMolstar'
        )

    structure(component, class = c('dash_component', 'list'))
}
