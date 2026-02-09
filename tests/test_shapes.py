import dash_molstar
import math
from dash import Dash, html
from dash_molstar.utils import molstar_helper
from dash_molstar.utils import shapes

# ============================================
# Basic Shape Tests
# ============================================

mol = molstar_helper.parse_molecule('3u7y.pdb')
box = shapes.create_box(min_xyz=(1,2,3), max_xyz=(4,5,6))
sphere = shapes.create_sphere(center=(7,8,9), opacity=0.3)
cylinder = shapes.create_cylinder(start=(0,0,0), end=(5,5,5), radius=0.2, color='red')
dashed_cylinder = shapes.create_cylinder(start=(1,2,3), end=(6,7,8), radius=0.2, label='dashed_cylinder', color='yellow', dashed=True)

# ============================================
# Plane Tests
# ============================================

# Simple horizontal plane at origin
plane_horizontal = shapes.create_plane(
    center=(0, 0, 0),
    dir_major=(1, 0, 0),
    dir_minor=(0, 1, 0),
    scale_x=20,
    scale_y=20,
    label="Horizontal Plane",
    color='lightblue',
    opacity=1,
    double_sided=False
)

# Vertical plane
plane_vertical = shapes.create_plane(
    center=(10, 0, 0),
    dir_major=(0, 1, 0),
    dir_minor=(0, 0, 1),
    scale_x=20,
    scale_y=20,
    label="Vertical Plane",
    color='lightgreen',
    opacity=1
)

# ============================================
# Axes Tests
# ============================================

# Standard XYZ axes at origin
axes_standard = shapes.create_axes(
    origin=(0, 0, 0),
    dir_a=(5, 0, 0),  # X axis
    dir_b=(0, 5, 0),  # Y axis
    dir_c=(0, 0, 5),  # Z axis
    label="Standard Axes",
    color='grey',
    radius_scale=2
)

# Rotated axes
axes_rotated = shapes.create_axes(
    origin=(15, 0, 0),
    dir_a=(15, 15, 0),
    dir_b=(-15, 15, 0),
    dir_c=(0, 0, 20),
    label="Rotated Axes",
    color='darkgrey',
    radius_scale=1
)

# ============================================
# Ellipsoid Tests
# ============================================

# Sphere-like ellipsoid
ellipsoid_sphere = shapes.create_ellipsoid(
    center=(0, 10, 0),
    dir_major=(1, 0, 0),
    dir_minor=(0, 1, 0),
    radius_scale=(2, 2, 2),
    label="Sphere Ellipsoid",
    color='green',
    opacity=0.6,
)

# Elongated ellipsoid
ellipsoid_elongated = shapes.create_ellipsoid(
    center=(10, 10, 0),
    dir_major=(1, 0, 0),
    dir_minor=(0, 1, 0),
    radius_scale=(4, 1, 1),
    label="Elongated Ellipsoid",
    color='blue',
    opacity=0.5,
)

# ============================================
# Ribbon Tests
# ============================================

# Simple straight ribbon
ribbon_straight = shapes.create_ribbon(
    control_points=[0, 0, 0, 5, 0, 0, 10, 0, 0],  # 3 points
    normal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0],
    binormal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1],
    width_values=[0.5, 0.5, 0.5],
    label="Straight Ribbon",
    color='purple',
    opacity=0.8
)

# Ribbon with arrow
ribbon_arrow = shapes.create_ribbon(
    control_points=[0, 5, 0, 5, 5, 0, 10, 5, 0],
    normal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1],
    binormal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0],
    width_values=[0, 0, 0],
    label="Arrow Ribbon",
    color='magenta',
    opacity=1.0,
    arrow_height=0.5
)

# Tapered ribbon (width changes)
ribbon_tapered = shapes.create_ribbon(
    control_points=[0, 10, 0, 3, 10, 0, 3, 10, 0, 9, 10, 0],
    normal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    binormal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    width_values=[0.0, 0.3, 0.1, 0.1],
    label="Tapered Ribbon",
    color='pink'
)

# ============================================
# Sheet Tests
# ============================================

# Simple sheet with caps
sheet_simple = shapes.create_sheet(
    control_points=[0, 0, 10, 5, 0, 10, 10, 0, 10],
    normal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0],
    binormal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1],
    width_values=[0.8, 0.8, 0.8],
    height_values=[0.2, 0.2, 0.2],
    label="Simple Sheet",
    color='orange',
    opacity=0.9,
)

# Sheet without caps
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

# ============================================
# Tube Tests
# ============================================

# Simple straight tube
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

# Tube with rounded cross-section
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

# Curved tube (arc shape)
num_segments = 20
arc_control_points = []
arc_normal_vectors = []
arc_binormal_vectors = []
arc_width_values = []
arc_height_values = []

for i in range(num_segments + 1):
    angle = (math.pi / 2) * (i / num_segments)  # 0 to 90 degrees
    radius = 5
    # Control points along the arc
    arc_control_points.extend([
        math.cos(angle) * radius,
        10,
        20 + math.sin(angle) * radius
    ])
    # Normal vectors pointing up
    arc_normal_vectors.extend([0, 1, 0])
    # Binormal vectors pointing toward center
    arc_binormal_vectors.extend([
        -math.cos(angle),
        0,
        -math.sin(angle)
    ])
    arc_width_values.append(0.25)
    arc_height_values.append(0.25)

tube_curved = shapes.create_tube(
    control_points=arc_control_points,
    normal_vectors=arc_normal_vectors,
    binormal_vectors=arc_binormal_vectors,
    width_values=arc_width_values,
    height_values=arc_height_values,
    label="Curved Tube",
    color='deepskyblue',
    radial_segments=24,
    start_cap=True,
    end_cap=True
)

# Variable width tube
tube_variable = shapes.create_tube(
    control_points=[15, 0, 20, 18, 0, 20, 21, 0, 20, 24, 0, 20],
    normal_vectors=[0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    binormal_vectors=[0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    width_values=[0.2, 0.5, 0.3, 0.6],
    height_values=[0.2, 0.5, 0.3, 0.6],
    label="Variable Tube",
    color='dodgerblue'
)

# ============================================
# Combined Data for Visualization
# ============================================

# All shapes for testing
all_shapes = [
   # mol,
   box,
   sphere,
   cylinder,
   dashed_cylinder,
   plane_horizontal,
   plane_vertical,
   axes_standard,
   axes_rotated,
   ellipsoid_sphere,
   ellipsoid_elongated,
   ribbon_straight,
   ribbon_arrow,
   ribbon_tapered,
   sheet_simple,
   sheet_no_caps,
   tube_straight,
   tube_rounded,
   tube_curved,
   tube_variable,
]

app = Dash(__name__)
app.layout = html.Div(
   dash_molstar.MolstarViewer(
      id='viewer', 
      style={'width': '800px', 'height':'600px'},
      data=all_shapes,  # Change to 'data' for minimal test
   )
)

if __name__ == '__main__':
    app.run(debug=True)