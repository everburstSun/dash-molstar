# AUTO GENERATED FILE - DO NOT EDIT

export molstarviewer

"""
    molstarviewer(;kwargs...)

A MolstarViewer component.
The Molstar viewer component for dash
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `camera` (Bool | Real | String | Dict | Array; optional): The camera object in the molstar viewer.
- `cameradebounce` (Real; optional): Debounce time in milliseconds for camera change events.
Set to 0 to disable debounce. Default is 100ms.
- `cameraresponddrag` (Bool; optional): Whether to respond to drag events of the camera.
Set to false to disable camera parameter updates while dragging
with mouse keys, or scrolling.
- `className` (String; optional): The HTML property `class` for additional class names of the container of molstar viewer.
- `data` (Bool | Real | String | Dict | Array; optional): Data containing the structure info that should be loaded into molstar viewer, as well as some control flags.
The data can be generated with python method `parse_molecule`.
- `focus` (Dict; optional): The structure region to let the camera focus on in the molstar viewer.
- `frame` (Real; optional): The trajectory frame in the molstar viewer.
- `hover` (Dict; optional): The structure region to be hovered in the molstar viewer.
- `layout` (Dict; optional): The layout of the molstar viewer. Determining what controls to be displayed. 

The layout is not allowed to be changed once the component has been initialized.
- `measurement` (Bool | Real | String | Dict | Array; optional): The measurements in the molstar viewer.
- `screenshot` (Dict; optional): The screenshot object containing the options for taking 
screenshot of the current view in molstar viewer.
- `selection` (Dict; optional): The structure region to be selected in the molstar viewer.
- `style` (Dict; optional): The HTML property `style` to control the appearence of the container of molstar viewer.
- `updatefocusonframechange` (Bool; optional): Update focus data when frame index have changed.
- `updateselectiononframechange` (Bool; optional): Update selection data when frame index have changed.
"""
function molstarviewer(; kwargs...)
        available_props = Symbol[:id, :camera, :cameradebounce, :cameraresponddrag, :className, :data, :focus, :frame, :hover, :layout, :measurement, :screenshot, :selection, :style, :updatefocusonframechange, :updateselectiononframechange]
        wild_props = Symbol[]
        return Component("molstarviewer", "MolstarViewer", "dash_molstar", available_props, wild_props; kwargs...)
end

