```{toctree}
:maxdepth: 2

   load
   helper
   shapes
   properties
   callbacks
   targets
   representations
   camera
```

# Camera control

The `camera` property of `MolstarViewer` is **bidirectional**. As an `Output`, it moves the camera to a given state. As an `Input` or `State`, it reports the current camera state (the position, target, orientation, and clipping settings) so that callbacks can read where the user has navigated to.

To control the camera, two helpers work together:

- The {py:class}`Camera` class describes a camera state.
- The {py:func}`set_camera` function packages a `Camera` (and an optional transition `duration`) into the value expected by the `camera` property.

```py
from dash_molstar.helpers import set_camera
from dash_molstar.utils import Camera
```

Two related properties of the viewer control how camera changes are reported back:

- **cameradebounce** – Debounce time in milliseconds for camera-change events (default: `100`). Set to `0` to disable debouncing.
- **cameraresponddrag** – Whether the `camera` property updates while the user is dragging or scrolling (default: `True`).

```py
dash_molstar.MolstarViewer(
   id='viewer',
   data=mol,
   cameradebounce=100,
   cameraresponddrag=True,
)
```

## The Camera class

```{eval-rst}
.. class:: Camera(snapshot=None)

   Describe a camera state for the molstar viewer.

   :param snapshot: An optional dictionary of camera properties used to initialize the instance.
                    Any key that is omitted keeps its default value. This is typically a camera
                    snapshot read back from the viewer's ``camera`` property. (default: ``None``)
   :type snapshot: dict, optional

   The following properties can be set on the constructor's ``snapshot`` dictionary or
   assigned directly on an instance:

   :param mode: Projection mode, either ``'perspective'`` or ``'orthographic'``. (default: ``'perspective'``)
   :type mode: str

   :param fov: Field of view. (default: ``45.0``)
   :type fov: float

   :param position: Camera position as an ``(x, y, z)`` tuple or list. (default: ``(0.0, 0.0, 100.0)``)
   :type position: tuple

   :param up: Camera up vector as an ``(x, y, z)`` tuple or list. (default: ``(0.0, 1.0, 0.0)``)
   :type up: tuple

   :param target: The look-at point as an ``(x, y, z)`` tuple or list. (default: ``(0.0, 0.0, 0.0)``)
   :type target: tuple

   :param radius: Visible radius. Objects outside this radius fall into fog. (default: ``59.94``)
   :type radius: float

   :param radiusMax: Maximum visible radius (the radius enclosing all visible objects). (default: ``59.94``)
   :type radiusMax: float

   :param fog: Fog intensity, from 0 to 100. (default: ``15.0``)
   :type fog: float

   :param clipFar: Whether to clip geometry at the far plane. (default: ``True``)
   :type clipFar: bool

   :param minNear: Minimum near clipping-plane distance. (default: ``5.0``)
   :type minNear: float

   :param minFar: Minimum far clipping-plane distance. (default: ``1.0``)
   :type minFar: float

   :raises ValueError: If ``mode`` is not ``'perspective'`` or ``'orthographic'``, or if
                       ``position``, ``up``, or ``target`` do not contain exactly 3 elements.
```

A `Camera` can be built from scratch, from a snapshot dictionary, or by assigning its properties:

```py
from dash_molstar.utils import Camera

# from a snapshot dictionary
camera = Camera({
   'mode': 'perspective',
   'position': [0, 0, 120],
   'target': [0, 0, 0],
   'up': [0, 1, 0],
})

# or by assigning properties
camera = Camera()
camera.position = (0, 0, 120)
camera.mode = 'orthographic'
```

```{eval-rst}
.. function:: set_camera(camera=None, duration=0)

   Create a camera operation for the ``camera`` property.

   :param camera: The :class:`Camera` instance to move to. If ``None``, the camera is reset to
                  automatically frame the loaded structure. (default: ``None``)
   :type camera: Camera, optional

   :param duration: The transition duration in milliseconds. A value of ``0`` moves the camera
                    instantly. (default: ``0``)
   :type duration: int, optional

   :returns: The value for the ``camera`` property of MolstarViewer.
   :rtype: dict

   :raises TypeError: If ``camera`` is provided but is not a :class:`Camera` instance.
```

## Setting the camera

Return the output of `set_camera()` to the `camera` property to move the camera. Pass a `Camera` describing the desired state, and an optional `duration` for a smooth transition:

```py
from dash import Dash, Input, Output, html
import dash_molstar
from dash_molstar.helpers import parse_molecule, set_camera
from dash_molstar.utils import Camera

mol = parse_molecule('3u7y.pdb')

app = Dash(__name__)
app.layout = html.Div([
   dash_molstar.MolstarViewer(id='viewer', style={'width': '600px', 'height': '600px'}, data=mol),
   html.Button("Move camera", id='btn'),
])

@app.callback(
   Output('viewer', 'camera'),
   Input('btn', 'n_clicks'),
   prevent_initial_call=True
)
def move_camera(n_clicks):
   camera = Camera({'position': [0, 0, 150], 'target': [0, 0, 0], 'up': [0, 1, 0]})
   return set_camera(camera=camera, duration=250)  # animate over 250 ms
```

### Resetting the camera

Calling `set_camera()` without a `camera` (or with `camera=None`) resets the camera so that it automatically frames the loaded structure:

```py
return set_camera(camera=None, duration=250)
```

## Reading the camera state

When the user rotates, zooms, or pans the structure, the viewer reports the new state through the `camera` property. Use it as an `Input` to react to camera movement. The reported value is a dictionary of the same keys accepted by `Camera`, which can be passed straight back into `Camera()` to inspect or modify:

```py
import dash
from dash import Input, Output

@app.callback(
   Output('camera-info', 'children'),
   Input('viewer', 'camera')
)
def show_camera(camera):
   if camera is None or not isinstance(camera, dict):
      raise dash.exceptions.PreventUpdate
   # ignore updates produced by our own set_camera() calls
   if camera.get('duration') is not None:
      raise dash.exceptions.PreventUpdate
   pos = camera.get('position', [0, 0, 0])
   return f"Camera position: {pos}"
```

:::{note}
A value produced by `set_camera()` carries a `duration` key, while a state read back from user navigation does not. Checking for `duration` lets a callback ignore the camera updates triggered by its own `set_camera()` output, as shown above.

The frequency of these updates is governed by the `cameradebounce` and `cameraresponddrag` properties described above.
:::

## Animating through keyframes

If a **list** of `set_camera()` operations is returned to the `camera` property, they are executed sequentially, each using its own `duration`. This makes it possible to play a keyframe animation by interpolating the camera between saved states:

```py
FRAME_RATE = 24  # frames per second

@app.callback(
   Output('viewer', 'camera'),
   Input('btn-play', 'n_clicks'),
   State('keyframes-store', 'data'),
   prevent_initial_call=True
)
def play_animation(n_clicks, keyframes):
   # keyframes: {frame_number: camera_snapshot}
   sorted_frames = sorted((int(f), keyframes[f]) for f in keyframes)

   sequence = []
   for i, (frame, snapshot) in enumerate(sorted_frames):
      camera = Camera(snapshot)
      if i == 0:
         sequence.append(set_camera(camera=camera, duration=0))  # jump to the first keyframe
      else:
         prev_frame = sorted_frames[i - 1][0]
         duration_ms = int(((frame - prev_frame) / FRAME_RATE) * 1000)
         sequence.append(set_camera(camera=camera, duration=duration_ms))
   return sequence
```

## Importing a view from PyMOL

The {py:meth}`Camera.from_pymol_view` class method constructs a `Camera` from the 18-value output of PyMOL's `get_view()` command, making it easy to reproduce a view set up in PyMOL.

```{eval-rst}
.. classmethod:: Camera.from_pymol_view(view)

   Create a :class:`Camera` from PyMOL's ``get_view()`` output.

   :param view: Either the string printed by PyMOL's ``get_view()`` command, or a tuple/list of
                18 floats. The 18 values encode a 3×3 rotation matrix, the camera offset, the
                rotation center, the front and rear clipping planes, and an orthoscopic flag.
   :type view: str | tuple | list

   :returns: A new camera instance with the converted settings.
   :rtype: Camera

   :raises ValueError: If the input does not contain exactly 18 values.
```

```py
from dash_molstar.helpers import Camera, set_camera

view_str = '''(
    0.984808,    0.000000,   -0.173648,
    0.000000,    1.000000,    0.000000,
    0.173648,    0.000000,    0.984808,
    0.000000,    0.000000, -150.000000,
   10.000000,   20.000000,   30.000000,
  100.000000,  200.000000,    0.000000 )'''

camera = Camera.from_pymol_view(view_str)
return set_camera(camera=camera, duration=500)
```

## Saving and loading camera configurations

A `Camera` can be serialized to JSON and restored later, which is convenient for storing preset views.

```{eval-rst}
.. method:: Camera.save_config(filename)

   Save the current camera configuration to a JSON file. The ``.json`` extension is appended
   automatically if missing.

   :param filename: The JSON filename to write.
   :type filename: str
```

```{eval-rst}
.. classmethod:: Camera.from_config(filename)

   Load a JSON configuration file and construct a new camera instance.

   :param filename: The JSON filename to read.
   :type filename: str

   :returns: The camera instance.
   :rtype: Camera
```

```py
from dash_molstar.helpers import Camera

# save a configured view
camera.save_config('my_view')          # writes my_view.json

# restore it in another session
camera = Camera.from_config('my_view.json')
```
