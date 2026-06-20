

def create_box(min_xyz=(0,0,0), max_xyz=(1,1,1), radius=0.1, label="Bounding Box", color='red', opacity=1.0):
    """
    Generate a bounding box in the viewer with given parameters.

    Parameters
    ----------
    `min_xyz` — tuple (optional)
        Minimum of x, y and z values (default: `(0,0,0)`)
    `max_xyz` — tuple (optional)
        Maximum of x, y and z values (default: `(1,1,1)`)
    `radius` — float (optional)
        Edge radius in angstrom (default: `0.1`)
    `label` — str (optional)
        The box label to be shown in the viewer (default: `"Bounding Box"`)
    `color` — str (optional)
        X11 color names (default: `'red'`)
        Avaliable options can be found at [here](https://www.w3.org/TR/css-color-3/#svg-color)
    `opacity` — float (optional)
        Transparency of the box. The value is ranging from 0 to 1.0. (default: `1.0`)

    Returns
    -------
    `dict`
        Dict for the `data` parameter of MolstarViewer

    Raises
    ------
    `ValueError`
        Raised if input coordinates are not 3-dimensional
    """
    if len(min_xyz) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    if len(max_xyz) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    return {
        'type': 'shape',
        'shape': 'box',
        'min': min_xyz,
        'max': max_xyz,
        'radius': radius,
        'label': label,
        'color': color,
        'alpha': opacity
    }

def create_sphere(center=(0,0,0), radius=1.0, label="Sphere", color='blue', opacity=1.0, detail=6):
    """
    Generate a sphere in the viewer with given parameters.

    Parameters
    ----------
    `center` — tuple (optional)
        Center of the sphere (default: `(0,0,0)`)
    `radius` — float (optional)
        Sphere radius in angstrom (default: `0.1`)
    `label` — str (optional)
        The sphere label to be shown in the viewer (default: `"Sphere"`)
    `color` — str (optional)
        X11 color names (default: `'blue'`)
        Avaliable options can be found at [here](https://www.w3.org/TR/css-color-3/#svg-color)
    `opacity` — float (optional)
        Transparency of the box. The value is ranging from 0 to 1.0. (default: `1.0`)
    `detail` — int (optional)
        Controls the subdivision surface of the sphere. The sphere is make of polygons. The higher
        the value, the more it looks like a fine sphere. But also requires longer time to
        render. The recommended value is 6.

    Returns
    -------
    `dict`
        Dict for the `data` parameter of MolstarViewer

    Raises
    ------
    `ValueError`
        Raised if input coordinates are not 3-dimensional
    """
    if len(center) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    return {
        'type': 'shape',
        'shape': 'sphere',
        'center': center,
        'radius': radius,
        'label': label,
        'color': color,
        'alpha': opacity,
        'detail': detail
    }

def create_cylinder(start=(0,0,0), end=(1,1,1), radius=0.1, label="Cylinder", color='yellow', opacity=1.0, dashed=False, dash_segments='auto'):
    """
    Generate a cylinder in the viewer with given parameters.

    Parameters
    ----------
    `start` — tuple (optional)
        Start point of the cylinder (default: `(0,0,0)`)
    `end` — tuple (optional)
        End point of the cylinder (default: `(1,1,1)`)
    `radius` — float (optional)
        Cylinder radius in angstrom (default: `0.1`)
    `label` — str (optional)
        The cylinder label to be shown in the viewer (default: `"Cylinder"`)
    `color` — str (optional)
        X11 color names (default: `'yellow'`)
        Avaliable options can be found at [here](https://www.w3.org/TR/css-color-3/#svg-color)
    `opacity` — float (optional)
        Transparency of the box. The value is ranging from 0 to 1.0. (default: `1.0`)
    `dashed` — bool (optional)
        Whether to create a dashed cylinder (default: `False`)
    `dash_segments` — str (optional)
        Number of segments for the dashed cylinder, including gaps (default: `'auto'`)
    """
    if len(start) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    if len(end) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    
    if dashed:
        if dash_segments == 'auto':
            length = ((start[0]-end[0])**2 + (start[1]-end[1])**2 + (start[2]-end[2])**2)**0.5
            dash_segments = length * 3
    
    return {
        'type': 'shape',
        'shape': 'cylinder',
        'start': start,
        'end': end,
        'props': {
            'radiusTop': radius,
            'radiusBottom': radius,
            'radialSegments': 100,
            'heightSegments': 100,
            'topCap': True,
            'bottomCap': True,
        },
        'label': label,
        'color': color,
        'alpha': opacity,
        'dashed': dashed,
        'dash_segments': dash_segments
    }

def create_plane(center=(0,0,0), dir_major=(1,0,0), dir_minor=(0,1,0), scale_x=1.0, scale_y=1.0, label="Plane", color='lightblue', opacity=1.0, double_sided=True):
    """
    Generate a plane in the viewer with given parameters.

    Parameters
    ----------
    `center` — tuple (optional)
        Center point of the plane (default: `(0,0,0)`)
    `dir_major` — tuple (optional)
        Major direction vector of the plane (default: `(1,0,0)`)
    `dir_minor` — tuple (optional)
        Minor direction vector of the plane (default: `(0,1,0)`)
    `scale_x` — float (optional)
        Scale factor in the major direction (default: `1.0`)
    `scale_y` — float (optional)
        Scale factor in the minor direction (default: `1.0`)
    `label` — str (optional)
        The plane label to be shown in the viewer (default: `"Plane"`)
    `color` — str (optional)
        X11 color names (default: `'lightblue'`)
    `opacity` — float (optional)
        Transparency of the plane. The value is ranging from 0 to 1.0. (default: `1.0`)
    `double_sided` — bool (optional)
        Whether the plane is double-sided (default: `True`). 
        When set to `False`, the plane will only be visible from the side where the normal vector 
        is pointing to (cross product of dir_major and dir_minor).

    Returns
    -------
    `dict`
        Dict for the `data` parameter of MolstarViewer
    """
    if len(center) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    if len(dir_major) != 3: raise ValueError("Direction vector must be 3-dimensional!")
    if len(dir_minor) != 3: raise ValueError("Direction vector must be 3-dimensional!")
    return {
        'type': 'shape',
        'shape': 'plane',
        'center': center,
        'dirMajor': dir_major,
        'dirMinor': dir_minor,
        'scaleX': scale_x,
        'scaleY': scale_y,
        'label': label,
        'color': color,
        'alpha': opacity,
        'doubleSided': double_sided
    }

def create_axes(origin=(0,0,0), dir_a=(1,0,0), dir_b=(0,1,0), dir_c=(0,0,1), label="Axes", color='grey', opacity=1.0, radius_scale=1.0):
    """
    Generate coordinate axes in the viewer with given parameters.

    Parameters
    ----------
    `origin` — tuple (optional)
        Origin point of the axes (default: `(0,0,0)`)
    `dir_a` — tuple (optional)
        Direction vector for the first axis (default: `(1,0,0)`)
    `dir_b` — tuple (optional)
        Direction vector for the second axis (default: `(0,1,0)`)
    `dir_c` — tuple (optional)
        Direction vector for the third axis (default: `(0,0,1)`)
    `label` — str (optional)
        The axes label to be shown in the viewer (default: `"Axes"`)
    `color` — str (optional)
        X11 color names (default: `'grey'`)
    `opacity` — float (optional)
        Transparency of the axes. The value is ranging from 0 to 1.0. (default: `1.0`)
    `radius_scale` — float (optional)
        Scale factor for the radius of the axes arrows (default: `1.0`)

    Returns
    -------
    `dict`
        Dict for the `data` parameter of MolstarViewer
    """
    if len(origin) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    if len(dir_a) != 3: raise ValueError("Direction vector must be 3-dimensional!")
    if len(dir_b) != 3: raise ValueError("Direction vector must be 3-dimensional!")
    if len(dir_c) != 3: raise ValueError("Direction vector must be 3-dimensional!")
    return {
        'type': 'shape',
        'shape': 'axes',
        'origin': origin,
        'dirA': dir_a,
        'dirB': dir_b,
        'dirC': dir_c,
        'label': label,
        'color': color,
        'alpha': opacity,
        'radiusScale': radius_scale
    }

def create_ellipsoid(center=(0,0,0), dir_major=(1,0,0), dir_minor=(0,1,0), radius_scale=(1,1,1), label="Ellipsoid", color='green', opacity=1.0, detail=6):
    """
    Generate an ellipsoid in the viewer with given parameters.

    Parameters
    ----------
    `center` — tuple (optional)
        Center point of the ellipsoid (default: `(0,0,0)`)
    `dir_major` — tuple (optional)
        Major direction vector of the ellipsoid (default: `(1,0,0)`)
    `dir_minor` — tuple (optional)
        Minor direction vector of the ellipsoid (default: `(0,1,0)`)
    `radius_scale` — tuple (optional)
        Scale factors for the three principal axes (default: `(1,1,1)`)
    `label` — str (optional)
        The ellipsoid label to be shown in the viewer (default: `"Ellipsoid"`)
    `color` — str (optional)
        X11 color names (default: `'green'`)
    `opacity` — float (optional)
        Transparency of the ellipsoid. The value is ranging from 0 to 1.0. (default: `1.0`)
    `detail` — int (optional)
        Controls the subdivision surface of the ellipsoid. Higher values create smoother surfaces. (default: `6`)

    Returns
    -------
    `dict`
        Dict for the `data` parameter of MolstarViewer
    """
    if len(center) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    if len(dir_major) != 3: raise ValueError("Direction vector must be 3-dimensional!")
    if len(dir_minor) != 3: raise ValueError("Direction vector must be 3-dimensional!")
    if len(radius_scale) != 3: raise ValueError("Radius scale must be 3-dimensional!")
    return {
        'type': 'shape',
        'shape': 'ellipsoid',
        'center': center,
        'dirMajor': dir_major,
        'dirMinor': dir_minor,
        'radiusScale': radius_scale,
        'label': label,
        'color': color,
        'alpha': opacity,
        'detail': detail
    }

def create_ribbon(control_points, normal_vectors, binormal_vectors, width_values, label="Ribbon", color='purple', opacity=1.0, linear_segments='auto', arrow_height=0):
    """
    Generate a ribbon shape in the viewer with given parameters.

    The ribbon is defined by a series of control points with associated normal and binormal vectors.
    The number of control points should be (linear_segments + 1).

    Parameters
    ----------
    `control_points` — list
        Flattened list of control point coordinates [x0,y0,z0, x1,y1,z1, ...]
        Length should be (linear_segments + 1) * 3
    `normal_vectors` — list
        Flattened list of normal vectors at each control point
        Length should be (linear_segments + 1) * 3
    `binormal_vectors` — list
        Flattened list of binormal vectors at each control point
        Length should be (linear_segments + 1) * 3
    `width_values` — list
        Width value at each control point. Length should be (linear_segments + 1)
    `label` — str (optional)
        The ribbon label to be shown in the viewer (default: `"Ribbon"`)
    `color` — str (optional)
        X11 color names (default: `'purple'`)
    `opacity` — float (optional)
        Transparency of the ribbon. The value is ranging from 0 to 1.0. (default: `1.0`)
    `linear_segments` — int or str (optional)
        Number of segments. If 'auto', calculated from control_points length. (default: `'auto'`)
    `arrow_height` — float (optional)
        Height of the arrow at the end. Set to 0 for no arrow. (default: `0`) None zero value will overwrite the `width_values` parameters.

    Returns
    -------
    `dict`
        Dict for the `data` parameter of MolstarViewer
    """
    if len(control_points) % 3 != 0: raise ValueError("Control points must be a flat list of 3D coordinates!")
    if len(normal_vectors) != len(control_points): raise ValueError("Normal vectors must have the same length as control points!")
    if len(binormal_vectors) != len(control_points): raise ValueError("Binormal vectors must have the same length as control points!")
    
    num_points = len(control_points) // 3
    if len(width_values) != num_points: raise ValueError(f"Width values length ({len(width_values)}) must equal number of control points ({num_points})!")
    
    if linear_segments == 'auto':
        linear_segments = num_points - 1
    
    return {
        'type': 'shape',
        'shape': 'ribbon',
        'controlPoints': list(control_points),
        'normalVectors': list(normal_vectors),
        'binormalVectors': list(binormal_vectors),
        'widthValues': list(width_values),
        'label': label,
        'color': color,
        'alpha': opacity,
        'linearSegments': linear_segments,
        'arrowHeight': arrow_height
    }

def create_sheet(control_points, normal_vectors, binormal_vectors, width_values, height_values, label="Sheet", color='orange', opacity=1.0, linear_segments='auto', arrow_height=0, start_cap=True, end_cap=True):
    """
    Generate a sheet shape in the viewer with given parameters.

    Similar to ribbon but with optional caps at both ends.

    Parameters
    ----------
    `control_points` — list
        Flattened list of control point coordinates [x0,y0,z0, x1,y1,z1, ...]
    `normal_vectors` — list
        Flattened list of normal vectors at each control point
    `binormal_vectors` — list
        Flattened list of binormal vectors at each control point
    `width_values` — list
        Width value at each control point
    `height_values` — list
        Height value at each control point
    `label` — str (optional)
        The sheet label to be shown in the viewer (default: `"Sheet"`)
    `color` — str (optional)
        X11 color names (default: `'orange'`)
    `opacity` — float (optional)
        Transparency of the sheet. The value is ranging from 0 to 1.0. (default: `1.0`)
    `linear_segments` — int or str (optional)
        Number of segments. If 'auto', calculated from control_points length. (default: `'auto'`)
    `arrow_height` — float (optional)
        Height of the arrow at the end. Set to 0 for no arrow. (default: `0`)
    `start_cap` — bool (optional)
        Whether to add a cap at the start (default: `True`)
    `end_cap` — bool (optional)
        Whether to add a cap at the end (default: `True`)

    Returns
    -------
    `dict`
        Dict for the `data` parameter of MolstarViewer
    """
    if len(control_points) % 3 != 0: raise ValueError("Control points must be a flat list of 3D coordinates!")
    if len(normal_vectors) != len(control_points): raise ValueError("Normal vectors must have the same length as control points!")
    if len(binormal_vectors) != len(control_points): raise ValueError("Binormal vectors must have the same length as control points!")
    
    num_points = len(control_points) // 3
    if len(width_values) != num_points: raise ValueError(f"Width values length ({len(width_values)}) must equal number of control points ({num_points})!")
    if len(height_values) != num_points: raise ValueError(f"Height values length ({len(height_values)}) must equal number of control points ({num_points})!")
    
    if linear_segments == 'auto':
        linear_segments = num_points - 1
    
    return {
        'type': 'shape',
        'shape': 'sheet',
        'controlPoints': list(control_points),
        'normalVectors': list(normal_vectors),
        'binormalVectors': list(binormal_vectors),
        'widthValues': list(width_values),
        'heightValues': list(height_values),
        'label': label,
        'color': color,
        'alpha': opacity,
        'linearSegments': linear_segments,
        'arrowHeight': arrow_height,
        'startCap': start_cap,
        'endCap': end_cap
    }

def create_tube(control_points, normal_vectors, binormal_vectors, width_values, height_values, label="Tube", color='cyan', opacity=1.0, linear_segments='auto', radial_segments=24, start_cap=True, end_cap=True, cross_section='elliptical', round_cap=False):
    """
    Generate a tube shape in the viewer with given parameters.

    A tube is defined by control points with customizable cross-section.

    Parameters
    ----------
    `control_points` — list
        Flattened list of control point coordinates [x0,y0,z0, x1,y1,z1, ...]
    `normal_vectors` — list
        Flattened list of normal vectors at each control point
    `binormal_vectors` — list
        Flattened list of binormal vectors at each control point
    `width_values` — list
        Width value at each control point
    `height_values` — list
        Height value at each control point
    `label` — str (optional)
        The tube label to be shown in the viewer (default: `"Tube"`)
    `color` — str (optional)
        X11 color names (default: `'cyan'`)
    `opacity` — float (optional)
        Transparency of the tube. The value is ranging from 0 to 1.0. (default: `1.0`)
    `linear_segments` — int or str (optional)
        Number of linear segments. If 'auto', calculated from control_points length. (default: `'auto'`)
    `radial_segments` — int (optional)
        Number of radial segments for the cross-section (default: `24`)
    `start_cap` — bool (optional)
        Whether to add a cap at the start (default: `True`)
    `end_cap` — bool (optional)
        Whether to add a cap at the end (default: `True`)
    `cross_section` — str (optional)
        Cross-section shape: 'elliptical' or 'rounded' (default: `'elliptical'`)
    `round_cap` — bool (optional)
        Whether to use rounded caps (default: `False`)

    Returns
    -------
    `dict`
        Dict for the `data` parameter of MolstarViewer
    """
    if len(control_points) % 3 != 0: raise ValueError("Control points must be a flat list of 3D coordinates!")
    if len(normal_vectors) != len(control_points): raise ValueError("Normal vectors must have the same length as control points!")
    if len(binormal_vectors) != len(control_points): raise ValueError("Binormal vectors must have the same length as control points!")
    
    num_points = len(control_points) // 3
    if len(width_values) != num_points: raise ValueError(f"Width values length ({len(width_values)}) must equal number of control points ({num_points})!")
    if len(height_values) != num_points: raise ValueError(f"Height values length ({len(height_values)}) must equal number of control points ({num_points})!")
    
    if cross_section not in ['elliptical', 'rounded']:
        raise ValueError("cross_section must be 'elliptical' or 'rounded'!")
    
    if linear_segments == 'auto':
        linear_segments = num_points - 1
    
    return {
        'type': 'shape',
        'shape': 'tube',
        'controlPoints': list(control_points),
        'normalVectors': list(normal_vectors),
        'binormalVectors': list(binormal_vectors),
        'widthValues': list(width_values),
        'heightValues': list(height_values),
        'label': label,
        'color': color,
        'alpha': opacity,
        'linearSegments': linear_segments,
        'radialSegments': radial_segments,
        'startCap': start_cap,
        'endCap': end_cap,
        'crossSection': cross_section,
        'roundCap': round_cap
    }