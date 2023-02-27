# AUTO GENERATED FILE - DO NOT EDIT

export molstarviewer

"""
    molstarviewer(;kwargs...)

A MolstarViewer component.
The Molstar viewer component for dash
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `component` (Dict; optional): The additional components to be created in the molstar viewer. Leave it undefined to keep the molstar default settings.
- `data` (Bool | Real | String | Dict | Array; optional): Data containing the structure info that should be loaded into molstar viewer, as well as some control flags.
The data can be generated with python method `parse_for_molstar`.
- `focus` (Dict; optional): The structure region to let the camera focus on in the molstar viewer.
- `layout` (Dict; optional): The layout of the molstar viewer. Determining what controls to be displayed. 

The layout is not allowed to be changed once the component has been initialized.
- `selection` (Dict; optional): The structure region to be selected in the molstar viewer.
- `style` (Dict; optional): The HTML property `style` to control the appearence of the container of molstar viewer.
"""
function molstarviewer(; kwargs...)
        available_props = Symbol[:id, :component, :data, :focus, :layout, :selection, :style]
        wild_props = Symbol[]
        return Component("molstarviewer", "MolstarViewer", "dash_molstar", available_props, wild_props; kwargs...)
end

