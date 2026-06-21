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

# Shapes

In addition to molecules, the molstar viewer also supports loading shapes. Now dash-molstar supports these basic shapes: [Box](#Box), [Cylinder](#Cylinder), [Sphere](#Sphere), [Plane](#Plane), [Axes](#Axes), [Ellipsoid](#Ellipsoid), [Ribbon](#Ribbon), [Sheet](#Sheet) and [Tube](#Tube). Shapes are identified based on their labels. If loading a shape with a label that already exist in the viewer, the existing one will be removed before loading the new one.

## Box

```{eval-rst}
.. function:: create_box(min_xyz=(0,0,0), max_xyz=(1,1,1), radius=0.1, label="Bounding Box", color='red', opacity=1.0)

   Generate a bounding box in the viewer with the given parameters.

   :param min_xyz: Minimum of x, y, and z values. (default: ``(0,0,0)``)
   :type min_xyz: tuple, optional

   :param max_xyz: Maximum of x, y, and z values. (default: ``(1,1,1)``)
   :type max_xyz: tuple, optional

   :param radius: Edge radius in angstroms. (default: ``0.1``)
   :type radius: float, optional

   :param label: The label to be shown for the bounding box in the viewer. (default: ``"Bounding Box"``)
   :type label: str, optional

   :param color: Color of the box. Should be an X11 color name.
                 Available options can be found at `here <https://www.w3.org/TR/css-color-3/#svg-color>`_. (default: ``'red'``)
   :type color: str, optional

   :param opacity: Transparency of the box, ranging from 0 to 1.0. (default: ``1.0``)
   :type opacity: float, optional

   :returns: A dictionary for the ``data`` property of MolstarViewer.
   :rtype: dict

   :raises ValueError: If the input coordinates are not 3-dimensional.

``` 

This function generates a Bounding Box in the Molstar viewer. Bounding boxes are used to enclose specific regions within the viewer's visualization. 

Each box is identified by a label, allowing you to manage and update existing boxes. If you provide Molstar with a box that has a label that already exists, it will update the existing box with the new parameters, preventing the creation of duplicate boxes with the same label. 

## Sphere

```{eval-rst}
.. function:: create_sphere(center=(0,0,0), radius=1.0, label="Sphere", color='blue', opacity=1.0, detail=6)

   Generate a sphere in the viewer with the given parameters.

   :param center: The center of the sphere. (default: ``(0,0,0)``)
   :type center: tuple, optional

   :param radius: The radius of the sphere in angstroms. (default: ``1.0``)
   :type radius: float, optional

   :param label: The label to be shown for the sphere in the viewer. (default: ``"Sphere"``)
   :type label: str, optional

   :param color: The color of the sphere. Should be an X11 color name.
                 Available options can be found at `here <https://www.w3.org/TR/css-color-3/#svg-color>`_. (default: ``'blue'``)
   :type color: str, optional

   :param opacity: Transparency of the sphere, ranging from 0 to 1.0. (default: ``1.0``)
   :type opacity: float, optional

   :param detail: Controls the subdivision surface of the sphere, which is made of polygons.
                  The higher the value, the finer the sphere appears, but it also requires more time to render. 
                  The recommended value is ``6``.
   :type detail: int, optional

   :returns: A dictionary for the ``data`` property of MolstarViewer.
   :rtype: dict

   :raises ValueError: If the input coordinates are not 3-dimensional.

``` 

This function generates a sphere in the Molstar viewer. Each sphere is also identified by a label, allowing you to manage and update existing spheres.

```py
import dash_molstar
from dash import Dash, html
from dash_molstar.helpers import parse_molecule
from dash_molstar.utils import shapes

mol = parse_molecule('3u7y.pdb')
box = shapes.create_box(min_xyz=(1,2,3), max_xyz=(4,5,6))
sphere = shapes.create_sphere(center=(7,8,9), opacity=0.3)

data = [mol, box, sphere]

app = Dash(__name__)
app.layout = html.Div(
   dash_molstar.MolstarViewer(
      id='viewer', style={'width': '500px', 'height':'500px'},
      data=data,

   )
)
```

## Cylinder

```{eval-rst}
.. function:: create_cylinder(start=(0,0,0), end=(1,1,1), radius=0.1, label="Cylinder", color='yellow', opacity=1.0, dashed=False, dash_segments='auto')

   Generate a cylinder in the viewer with the given parameters.

   :param start: The start point of the cylinder. (default: ``(0,0,0)``)
   :type start: tuple, optional

   :param end: The end point of the cylinder. (default: ``(1,1,1)``)
   :type end: tuple, optional

   :param radius: Cylinder radius in angstroms. (default: ``0.1``)
   :type radius: float, optional

   :param label: The label to be shown for the cylinder in the viewer. (default: ``"Cylinder"``)
   :type label: str, optional

   :param color: Color of the cylinder. Should be an X11 color name.
                 Available options can be found at `here <https://www.w3.org/TR/css-color-3/#svg-color>`_. (default: ``'yellow'``)
   :type color: str, optional

   :param opacity: Transparency of the cylinder, ranging from 0 to 1.0. (default: ``1.0``)
   :type opacity: float, optional

   :param dashed: Whether to create a dashed cylinder. (default: ``False``)
   :type dashed: bool, optional

   :param dash_segments: Number of segments for the dashed cylinder, including gaps.
                         If ``'auto'``, the number of segments is derived from the cylinder length. (default: ``'auto'``)
   :type dash_segments: int | str, optional

   :returns: A dictionary for the ``data`` property of MolstarViewer.
   :rtype: dict

   :raises ValueError: If the input coordinates are not 3-dimensional.

```

This function draws a cylinder between the `start` and `end` points. Setting `dashed=True` produces a dashed cylinder, which is useful for indicating distances or directions without obscuring the structure behind it.

```py
from dash_molstar.utils import shapes

# a solid cylinder
cylinder = shapes.create_cylinder(start=(0,0,0), end=(5,5,5), radius=0.2, color='red')

# a dashed cylinder
dashed_cylinder = shapes.create_cylinder(
   start=(1,2,3), end=(6,7,8), radius=0.2,
   label='dashed_cylinder', color='yellow', dashed=True
)
```

## Plane

```{eval-rst}
.. function:: create_plane(center=(0,0,0), dir_major=(1,0,0), dir_minor=(0,1,0), scale_x=1.0, scale_y=1.0, label="Plane", color='lightblue', opacity=1.0, double_sided=True)

   Generate a plane in the viewer with the given parameters.

   :param center: The center point of the plane. (default: ``(0,0,0)``)
   :type center: tuple, optional

   :param dir_major: Major direction vector of the plane. (default: ``(1,0,0)``)
   :type dir_major: tuple, optional

   :param dir_minor: Minor direction vector of the plane. (default: ``(0,1,0)``)
   :type dir_minor: tuple, optional

   :param scale_x: Scale factor along the major direction. (default: ``1.0``)
   :type scale_x: float, optional

   :param scale_y: Scale factor along the minor direction. (default: ``1.0``)
   :type scale_y: float, optional

   :param label: The label to be shown for the plane in the viewer. (default: ``"Plane"``)
   :type label: str, optional

   :param color: Color of the plane. Should be an X11 color name.
                 Available options can be found at `here <https://www.w3.org/TR/css-color-3/#svg-color>`_. (default: ``'lightblue'``)
   :type color: str, optional

   :param opacity: Transparency of the plane, ranging from 0 to 1.0. (default: ``1.0``)
   :type opacity: float, optional

   :param double_sided: Whether the plane is double-sided. When set to ``False``, the plane is only
                        visible from the side that the normal vector (the cross product of ``dir_major``
                        and ``dir_minor``) points to. (default: ``True``)
   :type double_sided: bool, optional

   :returns: A dictionary for the ``data`` property of MolstarViewer.
   :rtype: dict

   :raises ValueError: If the input coordinates or direction vectors are not 3-dimensional.

```

A plane is defined by a `center` point and two direction vectors, `dir_major` and `dir_minor`, which span the plane. The `scale_x` and `scale_y` parameters control the size of the plane along these two directions.

```py
from dash_molstar.utils import shapes

# a horizontal plane, only visible from one side
plane_horizontal = shapes.create_plane(
   center=(0, 0, 0),
   dir_major=(1, 0, 0),
   dir_minor=(0, 1, 0),
   scale_x=20,
   scale_y=20,
   label="Horizontal Plane",
   color='lightblue',
   double_sided=False
)

# a vertical plane
plane_vertical = shapes.create_plane(
   center=(10, 0, 0),
   dir_major=(0, 1, 0),
   dir_minor=(0, 0, 1),
   scale_x=20,
   scale_y=20,
   label="Vertical Plane",
   color='lightgreen'
)
```

## Axes

```{eval-rst}
.. function:: create_axes(origin=(0,0,0), dir_a=(1,0,0), dir_b=(0,1,0), dir_c=(0,0,1), label="Axes", color='grey', opacity=1.0, radius_scale=1.0)

   Generate coordinate axes in the viewer with the given parameters.

   :param origin: The origin point of the axes. (default: ``(0,0,0)``)
   :type origin: tuple, optional

   :param dir_a: Direction vector for the first axis. (default: ``(1,0,0)``)
   :type dir_a: tuple, optional

   :param dir_b: Direction vector for the second axis. (default: ``(0,1,0)``)
   :type dir_b: tuple, optional

   :param dir_c: Direction vector for the third axis. (default: ``(0,0,1)``)
   :type dir_c: tuple, optional

   :param label: The label to be shown for the axes in the viewer. (default: ``"Axes"``)
   :type label: str, optional

   :param color: Color of the axes. Should be an X11 color name.
                 Available options can be found at `here <https://www.w3.org/TR/css-color-3/#svg-color>`_. (default: ``'grey'``)
   :type color: str, optional

   :param opacity: Transparency of the axes, ranging from 0 to 1.0. (default: ``1.0``)
   :type opacity: float, optional

   :param radius_scale: Scale factor for the radius of the axes arrows. (default: ``1.0``)
   :type radius_scale: float, optional

   :returns: A dictionary for the ``data`` property of MolstarViewer.
   :rtype: dict

   :raises ValueError: If the input coordinates or direction vectors are not 3-dimensional.

```

This function draws a set of three arrows from a common `origin` along the `dir_a`, `dir_b`, and `dir_c` direction vectors. The length of each arrow is the magnitude of its direction vector, so the axes do not need to be unit length or mutually orthogonal.

```py
from dash_molstar.utils import shapes

# standard XYZ axes at the origin
axes_standard = shapes.create_axes(
   origin=(0, 0, 0),
   dir_a=(5, 0, 0),  # X axis
   dir_b=(0, 5, 0),  # Y axis
   dir_c=(0, 0, 5),  # Z axis
   label="Standard Axes",
   color='grey',
   radius_scale=2
)

# rotated, non-orthogonal axes
axes_rotated = shapes.create_axes(
   origin=(15, 0, 0),
   dir_a=(15, 15, 0),
   dir_b=(-15, 15, 0),
   dir_c=(0, 0, 20),
   label="Rotated Axes",
   color='darkgrey'
)
```

## Ellipsoid

```{eval-rst}
.. function:: create_ellipsoid(center=(0,0,0), dir_major=(1,0,0), dir_minor=(0,1,0), radius_scale=(1,1,1), label="Ellipsoid", color='green', opacity=1.0, detail=6)

   Generate an ellipsoid in the viewer with the given parameters.

   :param center: The center point of the ellipsoid. (default: ``(0,0,0)``)
   :type center: tuple, optional

   :param dir_major: Major direction vector of the ellipsoid. (default: ``(1,0,0)``)
   :type dir_major: tuple, optional

   :param dir_minor: Minor direction vector of the ellipsoid. (default: ``(0,1,0)``)
   :type dir_minor: tuple, optional

   :param radius_scale: Scale factors for the three principal axes. (default: ``(1,1,1)``)
   :type radius_scale: tuple, optional

   :param label: The label to be shown for the ellipsoid in the viewer. (default: ``"Ellipsoid"``)
   :type label: str, optional

   :param color: Color of the ellipsoid. Should be an X11 color name.
                 Available options can be found at `here <https://www.w3.org/TR/css-color-3/#svg-color>`_. (default: ``'green'``)
   :type color: str, optional

   :param opacity: Transparency of the ellipsoid, ranging from 0 to 1.0. (default: ``1.0``)
   :type opacity: float, optional

   :param detail: Controls the subdivision surface of the ellipsoid. Higher values create
                  smoother surfaces but require more time to render. (default: ``6``)
   :type detail: int, optional

   :returns: A dictionary for the ``data`` property of MolstarViewer.
   :rtype: dict

   :raises ValueError: If the input coordinates, direction vectors, or radius scale are not 3-dimensional.

```

An ellipsoid is oriented by its `dir_major` and `dir_minor` direction vectors and sized by the `radius_scale`, which gives the radius along each of its three principal axes. Setting all three scale factors equal produces a sphere, while differing values produce an elongated or flattened shape.

```py
from dash_molstar.utils import shapes

# a sphere-like ellipsoid (equal radii)
ellipsoid_sphere = shapes.create_ellipsoid(
   center=(0, 10, 0),
   dir_major=(1, 0, 0),
   dir_minor=(0, 1, 0),
   radius_scale=(2, 2, 2),
   label="Sphere Ellipsoid",
   color='green',
   opacity=0.6
)

# an elongated ellipsoid
ellipsoid_elongated = shapes.create_ellipsoid(
   center=(10, 10, 0),
   dir_major=(1, 0, 0),
   dir_minor=(0, 1, 0),
   radius_scale=(4, 1, 1),
   label="Elongated Ellipsoid",
   color='blue',
   opacity=0.5
)
```

## Ribbon

```{eval-rst}
.. function:: create_ribbon(control_points, normal_vectors, binormal_vectors, width_values, label="Ribbon", color='purple', opacity=1.0, linear_segments='auto', arrow_height=0)

   Generate a ribbon shape in the viewer with the given parameters. The ribbon is a flat band
   defined by a series of control points, each with an associated normal vector, binormal vector,
   and width.

   :param control_points: Flattened list of control point coordinates ``[x0,y0,z0, x1,y1,z1, ...]``.
                          Its length should be ``(linear_segments + 1) * 3``.
   :type control_points: list

   :param normal_vectors: Flattened list of normal vectors at each control point.
                          Must have the same length as ``control_points``.
   :type normal_vectors: list

   :param binormal_vectors: Flattened list of binormal vectors at each control point.
                            Must have the same length as ``control_points``.
   :type binormal_vectors: list

   :param width_values: Width value at each control point. Its length should be the number of control points.
   :type width_values: list

   :param label: The label to be shown for the ribbon in the viewer. (default: ``"Ribbon"``)
   :type label: str, optional

   :param color: Color of the ribbon. Should be an X11 color name.
                 Available options can be found at `here <https://www.w3.org/TR/css-color-3/#svg-color>`_. (default: ``'purple'``)
   :type color: str, optional

   :param opacity: Transparency of the ribbon, ranging from 0 to 1.0. (default: ``1.0``)
   :type opacity: float, optional

   :param linear_segments: Number of segments. If ``'auto'``, it is calculated from the number of
                           control points. (default: ``'auto'``)
   :type linear_segments: int | str, optional

   :param arrow_height: Height of the arrow at the end. Set to ``0`` for no arrow. A non-zero value
                        overrides the ``width_values`` parameter. (default: ``0``)
   :type arrow_height: float, optional

   :returns: A dictionary for the ``data`` property of MolstarViewer.
   :rtype: dict

   :raises ValueError: If the control points are not a flat list of 3D coordinates, or if the
                       normal vectors, binormal vectors, or width values have inconsistent lengths.

```

A ribbon is a flat band that follows a path defined by `control_points`. At every control point you also supply a `normal_vector` (the direction the ribbon faces) and a `binormal_vector` (the in-plane direction across the ribbon's width), each as a flattened list of 3D vectors. The `width_values` list sets the width of the band at each point, so a ribbon can taper along its length. Setting a non-zero `arrow_height` turns the ribbon into an arrow.

```py
from dash_molstar.utils import shapes

# a simple straight ribbon defined by 3 control points
ribbon_straight = shapes.create_ribbon(
   control_points=[0, 0, 0, 5, 0, 0, 10, 0, 0],
   normal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0],
   binormal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1],
   width_values=[0.5, 0.5, 0.5],
   label="Straight Ribbon",
   color='purple',
   opacity=0.8
)

# a ribbon rendered as an arrow
ribbon_arrow = shapes.create_ribbon(
   control_points=[0, 5, 0, 5, 5, 0, 10, 5, 0],
   normal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1],
   binormal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0],
   width_values=[0, 0, 0],
   label="Arrow Ribbon",
   arrow_height=0.5
)
```

## Sheet

```{eval-rst}
.. function:: create_sheet(control_points, normal_vectors, binormal_vectors, width_values, height_values, label="Sheet", color='orange', opacity=1.0, linear_segments='auto', arrow_height=0, start_cap=True, end_cap=True)

   Generate a sheet shape in the viewer with the given parameters. A sheet is similar to a ribbon
   but has thickness (a height) and optional caps at both ends.

   :param control_points: Flattened list of control point coordinates ``[x0,y0,z0, x1,y1,z1, ...]``.
   :type control_points: list

   :param normal_vectors: Flattened list of normal vectors at each control point.
                          Must have the same length as ``control_points``.
   :type normal_vectors: list

   :param binormal_vectors: Flattened list of binormal vectors at each control point.
                            Must have the same length as ``control_points``.
   :type binormal_vectors: list

   :param width_values: Width value at each control point. Its length should be the number of control points.
   :type width_values: list

   :param height_values: Height (thickness) value at each control point. Its length should be the number of control points.
   :type height_values: list

   :param label: The label to be shown for the sheet in the viewer. (default: ``"Sheet"``)
   :type label: str, optional

   :param color: Color of the sheet. Should be an X11 color name.
                 Available options can be found at `here <https://www.w3.org/TR/css-color-3/#svg-color>`_. (default: ``'orange'``)
   :type color: str, optional

   :param opacity: Transparency of the sheet, ranging from 0 to 1.0. (default: ``1.0``)
   :type opacity: float, optional

   :param linear_segments: Number of segments. If ``'auto'``, it is calculated from the number of
                           control points. (default: ``'auto'``)
   :type linear_segments: int | str, optional

   :param arrow_height: Height of the arrow at the end. Set to ``0`` for no arrow. (default: ``0``)
   :type arrow_height: float, optional

   :param start_cap: Whether to add a cap at the start. (default: ``True``)
   :type start_cap: bool, optional

   :param end_cap: Whether to add a cap at the end. (default: ``True``)
   :type end_cap: bool, optional

   :returns: A dictionary for the ``data`` property of MolstarViewer.
   :rtype: dict

   :raises ValueError: If the control points are not a flat list of 3D coordinates, or if the
                       normal vectors, binormal vectors, width values, or height values have inconsistent lengths.

```

A sheet behaves like a ribbon but adds thickness through the `height_values` list, producing a solid slab rather than a flat band. The `start_cap` and `end_cap` parameters control whether the open ends of the sheet are closed off.

```py
from dash_molstar.utils import shapes

# a sheet with capped ends
sheet_simple = shapes.create_sheet(
   control_points=[0, 0, 10, 5, 0, 10, 10, 0, 10],
   normal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0],
   binormal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1],
   width_values=[0.8, 0.8, 0.8],
   height_values=[0.2, 0.2, 0.2],
   label="Simple Sheet",
   color='orange',
   opacity=0.9
)

# a sheet with open ends
sheet_no_caps = shapes.create_sheet(
   control_points=[0, 5, 10, 5, 5, 10, 10, 5, 10],
   normal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0],
   binormal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1],
   width_values=[0.6, 0.6, 0.6],
   height_values=[0.15, 0.15, 0.15],
   label="Sheet No Caps",
   color='gold',
   start_cap=False,
   end_cap=False
)
```

## Tube

```{eval-rst}
.. function:: create_tube(control_points, normal_vectors, binormal_vectors, width_values, height_values, label="Tube", color='cyan', opacity=1.0, linear_segments='auto', radial_segments=24, start_cap=True, end_cap=True, cross_section='elliptical', round_cap=False)

   Generate a tube shape in the viewer with the given parameters. A tube follows a path of control
   points and has a customizable cross-section.

   :param control_points: Flattened list of control point coordinates ``[x0,y0,z0, x1,y1,z1, ...]``.
   :type control_points: list

   :param normal_vectors: Flattened list of normal vectors at each control point.
                          Must have the same length as ``control_points``.
   :type normal_vectors: list

   :param binormal_vectors: Flattened list of binormal vectors at each control point.
                            Must have the same length as ``control_points``.
   :type binormal_vectors: list

   :param width_values: Width value (cross-section radius along the binormal) at each control point.
                        Its length should be the number of control points.
   :type width_values: list

   :param height_values: Height value (cross-section radius along the normal) at each control point.
                         Its length should be the number of control points.
   :type height_values: list

   :param label: The label to be shown for the tube in the viewer. (default: ``"Tube"``)
   :type label: str, optional

   :param color: Color of the tube. Should be an X11 color name.
                 Available options can be found at `here <https://www.w3.org/TR/css-color-3/#svg-color>`_. (default: ``'cyan'``)
   :type color: str, optional

   :param opacity: Transparency of the tube, ranging from 0 to 1.0. (default: ``1.0``)
   :type opacity: float, optional

   :param linear_segments: Number of linear segments. If ``'auto'``, it is calculated from the number
                           of control points. (default: ``'auto'``)
   :type linear_segments: int | str, optional

   :param radial_segments: Number of radial segments for the cross-section. (default: ``24``)
   :type radial_segments: int, optional

   :param start_cap: Whether to add a cap at the start. (default: ``True``)
   :type start_cap: bool, optional

   :param end_cap: Whether to add a cap at the end. (default: ``True``)
   :type end_cap: bool, optional

   :param cross_section: Cross-section shape, either ``'elliptical'`` or ``'rounded'``. (default: ``'elliptical'``)
   :type cross_section: str, optional

   :param round_cap: Whether to use rounded caps. (default: ``False``)
   :type round_cap: bool, optional

   :returns: A dictionary for the ``data`` property of MolstarViewer.
   :rtype: dict

   :raises ValueError: If the control points are not a flat list of 3D coordinates; if the normal
                       vectors, binormal vectors, width values, or height values have inconsistent lengths;
                       or if ``cross_section`` is not ``'elliptical'`` or ``'rounded'``.

```

A tube sweeps a closed cross-section along the path defined by `control_points`. At each point, `width_values` and `height_values` set the cross-section radius along the binormal and normal directions respectively, so the tube can swell or shrink along its length. The `radial_segments` parameter controls how smooth the cross-section appears, while `cross_section` and `round_cap` adjust its shape and end style.

```py
from dash_molstar.utils import shapes

# a simple straight tube
tube_straight = shapes.create_tube(
   control_points=[0, 0, 20, 5, 0, 20, 10, 0, 20],
   normal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0],
   binormal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1],
   width_values=[0.3, 0.3, 0.3],
   height_values=[0.3, 0.3, 0.3],
   label="Straight Tube",
   color='cyan',
   opacity=0.8
)

# a tube with a rounded cross-section and rounded caps
tube_rounded = shapes.create_tube(
   control_points=[0, 5, 20, 5, 5, 20, 10, 5, 20],
   normal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0],
   binormal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1],
   width_values=[0.4, 0.4, 0.4],
   height_values=[0.4, 0.4, 0.4],
   label="Rounded Tube",
   color='teal',
   cross_section='rounded',
   round_cap=True
)
```

Because the ribbon, sheet, and tube shapes are all built from control points and vectors, you can generate them programmatically to trace curved paths. For example, the following builds a curved tube along a quarter-circle arc:

```py
import math
from dash_molstar.utils import shapes

num_segments = 20
control_points, normal_vectors, binormal_vectors = [], [], []
width_values, height_values = [], []

for i in range(num_segments + 1):
   angle = (math.pi / 2) * (i / num_segments)  # 0 to 90 degrees
   radius = 5
   control_points.extend([math.cos(angle) * radius, 10, 20 + math.sin(angle) * radius])
   normal_vectors.extend([0, 1, 0])
   binormal_vectors.extend([-math.cos(angle), 0, -math.sin(angle)])
   width_values.append(0.25)
   height_values.append(0.25)

tube_curved = shapes.create_tube(
   control_points=control_points,
   normal_vectors=normal_vectors,
   binormal_vectors=binormal_vectors,
   width_values=width_values,
   height_values=height_values,
   label="Curved Tube",
   color='deepskyblue'
)
```

