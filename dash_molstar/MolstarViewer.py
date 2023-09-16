# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MolstarViewer(Component):
    """A MolstarViewer component.
The Molstar viewer component for dash

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    The HTML property `class` for additional class names of the
    container of molstar viewer.

- data (boolean | number | string | dict | list; optional):
    Data containing the structure info that should be loaded into
    molstar viewer, as well as some control flags. The data can be
    generated with python method `parse_molecule`.

- focus (dict; optional):
    The structure region to let the camera focus on in the molstar
    viewer.

- layout (dict; optional):
    The layout of the molstar viewer. Determining what controls to be
    displayed.   The layout is not allowed to be changed once the
    component has been initialized.

- selection (dict; optional):
    The structure region to be selected in the molstar viewer.

- style (dict; optional):
    The HTML property `style` to control the appearence of the
    container of molstar viewer."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_molstar'
    _type = 'MolstarViewer'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, data=Component.UNDEFINED, layout=Component.UNDEFINED, selection=Component.UNDEFINED, focus=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'data', 'focus', 'layout', 'selection', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'data', 'focus', 'layout', 'selection', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(MolstarViewer, self).__init__(**args)
