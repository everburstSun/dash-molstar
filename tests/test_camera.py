"""
Test camera properties display with Dash callbacks.
Rotate/zoom the molecule in the viewer to see camera properties update in real-time.
Users can also manually edit camera parameters and click Update to apply changes.
"""

import dash_molstar
import dash_bootstrap_components as dbc
from dash import Dash, callback, Output, Input, State, html, dcc
from dash_molstar.helpers import parse_molecule, set_camera, Camera
import dash

# Constants
FRAME_RATE = 24  # frames per second

# Load a sample molecule
mol = parse_molecule('3u7y.pdb')

app = Dash(__name__, 
    external_scripts=[{
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js',
        'integrity': 'sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm',
        'crossorigin': 'anonymous'
    }],
    external_stylesheets=[{
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css',
        'integrity': 'sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9',
        'crossorigin': 'anonymous',
        'rel': 'stylesheet'
    }]
)


app.layout = html.Div([
    html.H1("Camera Properties Test"),
    
    dbc.Row([
        # Left column: Molstar Viewer
        dbc.Col([
            dash_molstar.MolstarViewer(
                id='viewer',
                style={'width': 'auto', 'height': '600px'},
                data=mol,
                cameradebounce=100
            )
        ], width=6),
        
        # Right column: Camera Controls
        dbc.Col([
            html.H4("Camera Controls"),
            
            # Buttons
            dbc.Row([
                dbc.Col([
                    html.Button("Reset", id='btn-reset', n_clicks=0, 
                               className="btn btn-secondary", style={'width': '100%'}),
                ], width=6),
                dbc.Col([
                    html.Button("Update", id='btn-update', n_clicks=0,
                               className="btn btn-success", style={'width': '100%'}),
                ], width=6),
            ], className="mb-3"),
            
            html.Hr(),
            
            # Projection Mode
            dbc.InputGroup([
                dbc.InputGroupText("Mode"),
                dbc.Select(
                    id='camera-mode',
                    options=[
                        {'label': 'Perspective', 'value': 'perspective'},
                        {'label': 'Orthographic', 'value': 'orthographic'}
                    ],
                    value='perspective'
                ),
            ], className="mb-2"),
            
            # FOV
            dbc.InputGroup([
                dbc.InputGroupText("FOV (rad)"),
                dbc.Input(id='camera-fov', type='number', value=0.7854, step=0.1),
            ], className="mb-2"),
            
            html.Hr(),
            
            # Position
            html.Strong("Position"),
            dbc.Row([
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("x"),
                        dbc.Input(id='camera-pos-x', type='number', value=0, step=1),
                    ], size="sm"),
                ], width=4),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("y"),
                        dbc.Input(id='camera-pos-y', type='number', value=0, step=1),
                    ], size="sm"),
                ], width=4),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("z"),
                        dbc.Input(id='camera-pos-z', type='number', value=100, step=1),
                    ], size="sm"),
                ], width=4),
            ], className="mb-2"),
            
            # Target
            html.Strong("Target"),
            dbc.Row([
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("x"),
                        dbc.Input(id='camera-target-x', type='number', value=0, step=1),
                    ], size="sm"),
                ], width=4),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("y"),
                        dbc.Input(id='camera-target-y', type='number', value=0, step=1),
                    ], size="sm"),
                ], width=4),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("z"),
                        dbc.Input(id='camera-target-z', type='number', value=0, step=1),
                    ], size="sm"),
                ], width=4),
            ], className="mb-2"),
            
            # Up Vector
            html.Strong("Up Vector"),
            dbc.Row([
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("x"),
                        dbc.Input(id='camera-up-x', type='number', value=0, step=0.1),
                    ], size="sm"),
                ], width=4),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("y"),
                        dbc.Input(id='camera-up-y', type='number', value=1, step=0.1),
                    ], size="sm"),
                ], width=4),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("z"),
                        dbc.Input(id='camera-up-z', type='number', value=0, step=0.1),
                    ], size="sm"),
                ], width=4),
            ], className="mb-2"),
            
            html.Hr(),
            
            # Radius parameters
            dbc.Row([
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("Radius"),
                        dbc.Input(id='camera-radius', type='number', value=50, step=1),
                    ], size="sm"),
                ], width=6),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("RadiusMax"),
                        dbc.Input(id='camera-radius-max', type='number', value=100, step=1),
                    ], size="sm"),
                ], width=6),
            ], className="mb-2"),
            
            # Fog & Clipping
            dbc.Row([
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("Fog"),
                        dbc.Input(id='camera-fog', type='number', value=50, step=1),
                    ], size="sm"),
                ], width=4),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("MinNear"),
                        dbc.Input(id='camera-min-near', type='number', value=5, step=0.5),
                    ], size="sm"),
                ], width=4),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("MinFar"),
                        dbc.Input(id='camera-min-far', type='number', value=0, step=0.5),
                    ], size="sm"),
                ], width=4),
            ], className="mb-2"),
            
            # ClipFar checkbox
            dbc.Checkbox(
                id='camera-clip-far',
                label="ClipFar",
                value=True,
                className="mb-2"
            ),
            
            html.Hr(),
            
            # Animation duration
            dbc.InputGroup([
                dbc.InputGroupText("Animation (ms)"),
                dbc.Input(id='camera-duration', type='number', value=250, step=100),
            ], className="mb-2"),
            
        ], width=6),
    ]),
    
    html.Hr(),
    
    # Keyframe Animation Timeline
    dbc.Row([
        dbc.Col([
            html.H4("Keyframe Animation"),
            
            # Controls row
            dbc.Row([
                # Total frames input
                dbc.Col([
                    dbc.InputGroup([
                        dbc.InputGroupText("Total Frames"),
                        dbc.Input(id='total-frames', type='number', value=240, min=24, step=1),
                    ], size="sm"),
                ], width=2),
                
                # Keyframe buttons
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("◀ Prev", id='btn-prev-keyframe', color="secondary", size="sm"),
                        dbc.Button("Keyframe", id='btn-add-keyframe', color="primary", size="sm"),
                        dbc.Button("Remove", id='btn-remove-keyframe', color="danger", size="sm"),
                        dbc.Button("Next ▶", id='btn-next-keyframe', color="secondary", size="sm"),
                    ]),
                ], width=5),
                
                # Play button and current frame display
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("▶ Play", id='btn-play', color="success", size="sm"),
                    ]),
                    html.Span(id='current-frame-display', className="ms-3", 
                              style={'fontWeight': 'bold'}),
                ], width=3),
                
                # Keyframe info
                dbc.Col([
                    html.Span(id='keyframe-info', className="text-muted"),
                ], width=2),
            ], className="mb-2"),
            
            # Timeline slider
            dcc.Slider(
                id='timeline-slider',
                min=1,
                max=240,
                step=1,
                value=1,
                marks={1: '1'},
                tooltip={'placement': 'bottom', 'always_visible': False},
            ),
            
        ], width=12),
    ], className="mt-3"),
    
    # Hidden stores for keyframe data
    dcc.Store(id='keyframes-store', data={}),  # {frame_number: camera_snapshot}
    dcc.Store(id='current-keyframe-index', data=0),  # For navigation
    
], className='container')


@callback(
    Output('camera-mode', 'value'),
    Output('camera-fov', 'value'),
    Output('camera-pos-x', 'value'),
    Output('camera-pos-y', 'value'),
    Output('camera-pos-z', 'value'),
    Output('camera-target-x', 'value'),
    Output('camera-target-y', 'value'),
    Output('camera-target-z', 'value'),
    Output('camera-up-x', 'value'),
    Output('camera-up-y', 'value'),
    Output('camera-up-z', 'value'),
    Output('camera-radius', 'value'),
    Output('camera-radius-max', 'value'),
    Output('camera-fog', 'value'),
    Output('camera-min-near', 'value'),
    Output('camera-min-far', 'value'),
    Output('camera-clip-far', 'value'),
    Input('viewer', 'camera')
)
def sync_camera_to_inputs(camera):
    """Sync camera state from viewer to input fields."""
    if camera is None or type(camera) != dict:
        raise dash.exceptions.PreventUpdate
    if camera.get('duration') is not None:
        # Ignore camera updates that are triggered by our own set_camera calls
        raise dash.exceptions.PreventUpdate
    
    pos = camera.get('position', [0, 0, 0])
    target = camera.get('target', [0, 0, 0])
    up = camera.get('up', [0, 1, 0])
    
    return (
        camera.get('mode', 'perspective'),
        round(camera.get('fov', 0.7854), 4),
        round(pos[0], 4) if pos else 0,
        round(pos[1], 4) if pos else 0,
        round(pos[2], 4) if pos else 100,
        round(target[0], 4) if target else 0,
        round(target[1], 4) if target else 0,
        round(target[2], 4) if target else 0,
        round(up[0], 4) if up else 0,
        round(up[1], 4) if up else 1,
        round(up[2], 4) if up else 0,
        round(camera.get('radius', 50), 2),
        round(camera.get('radiusMax', 100), 2),
        round(camera.get('fog', 50), 0),
        round(camera.get('minNear', 5), 2),
        round(camera.get('minFar', 0), 2),
        camera.get('clipFar', True)
    )


@callback(
    Output('viewer', 'camera'),
    Input('btn-reset', 'n_clicks'),
    Input('btn-update', 'n_clicks'),
    State('camera-mode', 'value'),
    State('camera-fov', 'value'),
    State('camera-pos-x', 'value'),
    State('camera-pos-y', 'value'),
    State('camera-pos-z', 'value'),
    State('camera-target-x', 'value'),
    State('camera-target-y', 'value'),
    State('camera-target-z', 'value'),
    State('camera-up-x', 'value'),
    State('camera-up-y', 'value'),
    State('camera-up-z', 'value'),
    State('camera-radius', 'value'),
    State('camera-radius-max', 'value'),
    State('camera-fog', 'value'),
    State('camera-min-near', 'value'),
    State('camera-min-far', 'value'),
    State('camera-clip-far', 'value'),
    State('camera-duration', 'value'),
    prevent_initial_call=True
)
def update_camera(reset_clicks, update_clicks, mode, fov, 
                  pos_x, pos_y, pos_z, 
                  target_x, target_y, target_z,
                  up_x, up_y, up_z,
                  radius, radius_max, fog, min_near, min_far, clip_far, duration):
    """Update camera based on user input or reset to defaults."""
    from dash import ctx
    
    triggered_id = ctx.triggered_id
    
    if triggered_id == 'btn-reset':
        return set_camera(camera=None, duration=250)
    
    elif triggered_id == 'btn-update':
        camera = Camera({
            'mode': mode,
            'fov': fov,
            'position': [pos_x, pos_y, pos_z],
            'target': [target_x, target_y, target_z],
            'up': [up_x, up_y, up_z],
            'radius': radius,
            'radiusMax': radius_max,
            'fog': fog,
            'clipFar': bool(clip_far),
            'minNear': min_near,
            'minFar': min_far,
        })
        return set_camera(camera=camera, duration=duration)
    
    return None


# Callback to update slider marks when keyframes change
@callback(
    Output('timeline-slider', 'marks'),
    Input('keyframes-store', 'data'),
    Input('total-frames', 'value'),
    prevent_initial_call=True
)
def update_slider_marks(keyframes, total_frames):
    """Update slider marks when keyframes or total frames change."""
    if total_frames is None or total_frames < 24:
        total_frames = 24
    
    # Create marks: always show 1 and max
    marks = {1: '1', int(total_frames): str(int(total_frames))}
    
    # Add keyframe markers with frame number
    if keyframes:
        for frame in keyframes.keys():
            frame_int = int(frame)
            marks[frame_int] = f'◆{frame_int}'
    
    return marks


# Callback to update slider max value when total frames changes
@callback(
    Output('timeline-slider', 'max'),
    Input('total-frames', 'value'),
)
def update_slider_range(total_frames):
    """Update slider range when total frames changes."""
    if total_frames is None or total_frames < 24:
        total_frames = 24
    return total_frames


# Callback to manage keyframes
@callback(
    Output('keyframes-store', 'data'),
    Output('timeline-slider', 'value'),
    Output('keyframe-info', 'children'),
    Input('btn-add-keyframe', 'n_clicks'),
    Input('btn-remove-keyframe', 'n_clicks'),
    Input('btn-prev-keyframe', 'n_clicks'),
    Input('btn-next-keyframe', 'n_clicks'),
    State('keyframes-store', 'data'),
    State('timeline-slider', 'value'),
    State('camera-mode', 'value'),
    State('camera-fov', 'value'),
    State('camera-pos-x', 'value'),
    State('camera-pos-y', 'value'),
    State('camera-pos-z', 'value'),
    State('camera-target-x', 'value'),
    State('camera-target-y', 'value'),
    State('camera-target-z', 'value'),
    State('camera-up-x', 'value'),
    State('camera-up-y', 'value'),
    State('camera-up-z', 'value'),
    State('camera-radius', 'value'),
    State('camera-radius-max', 'value'),
    State('camera-fog', 'value'),
    State('camera-min-near', 'value'),
    State('camera-min-far', 'value'),
    State('camera-clip-far', 'value'),
    prevent_initial_call=True
)
def manage_keyframes(add_clicks, remove_clicks, prev_clicks, next_clicks,
                     keyframes, current_frame,
                     mode, fov, pos_x, pos_y, pos_z,
                     target_x, target_y, target_z,
                     up_x, up_y, up_z,
                     radius, radius_max, fog, min_near, min_far, clip_far):
    """Add, remove, or navigate keyframes."""
    from dash import ctx
    
    if keyframes is None:
        keyframes = {}
    
    triggered_id = ctx.triggered_id
    frame_key = str(current_frame)
    sorted_frames = sorted([int(f) for f in keyframes.keys()])
    
    if triggered_id == 'btn-add-keyframe':
        # Add current camera state as keyframe at current frame
        camera_snapshot = {
            'mode': mode,
            'fov': fov,
            'position': [pos_x, pos_y, pos_z],
            'target': [target_x, target_y, target_z],
            'up': [up_x, up_y, up_z],
            'radius': radius,
            'radiusMax': radius_max,
            'fog': fog,
            'clipFar': bool(clip_far),
            'minNear': min_near,
            'minFar': min_far,
        }
        keyframes[frame_key] = camera_snapshot
        info = f"Keyframes: {len(keyframes)}"
        return keyframes, current_frame, info
    
    elif triggered_id == 'btn-remove-keyframe':
        # Remove keyframe at current frame if exists
        if frame_key in keyframes:
            del keyframes[frame_key]
        info = f"Keyframes: {len(keyframes)}"
        return keyframes, current_frame, info
    
    elif triggered_id == 'btn-prev-keyframe':
        # Navigate to previous keyframe
        if sorted_frames:
            prev_frames = [f for f in sorted_frames if f < current_frame]
            if prev_frames:
                new_frame = prev_frames[-1]
            else:
                new_frame = sorted_frames[-1]  # Wrap around
            info = f"Keyframes: {len(keyframes)}"
            return keyframes, new_frame, info
    
    elif triggered_id == 'btn-next-keyframe':
        # Navigate to next keyframe
        if sorted_frames:
            next_frames = [f for f in sorted_frames if f > current_frame]
            if next_frames:
                new_frame = next_frames[0]
            else:
                new_frame = sorted_frames[0]  # Wrap around
            info = f"Keyframes: {len(keyframes)}"
            return keyframes, new_frame, info
    
    raise dash.exceptions.PreventUpdate


# Callback to display current frame and load keyframe data when navigating
@callback(
    Output('current-frame-display', 'children'),
    Output('viewer', 'camera', allow_duplicate=True),
    Input('timeline-slider', 'value'),
    State('keyframes-store', 'data'),
    prevent_initial_call=True
)
def display_and_load_keyframe(frame, keyframes):
    """Display current frame and load keyframe data if at a keyframe position."""
    frame_key = str(frame)
    
    if keyframes and frame_key in keyframes:
        # At a keyframe position - load the keyframe data to viewer
        camera = keyframes[frame_key]
        camera_obj = Camera(camera)
        return f"Frame {frame} ◆", set_camera(camera=camera_obj, duration=0)
    
    # Not at a keyframe - just update display
    return f"Frame {frame}", dash.no_update


# Callback to play animation
@callback(
    Output('viewer', 'camera', allow_duplicate=True),
    Input('btn-play', 'n_clicks'),
    State('keyframes-store', 'data'),
    State('total-frames', 'value'),
    prevent_initial_call=True
)
def play_animation(n_clicks, keyframes, total_frames):
    """Generate camera animation sequence from keyframes."""
    if not keyframes or len(keyframes) < 2:
        raise dash.exceptions.PreventUpdate
    
    # Sort keyframes by frame number
    sorted_frames = sorted([(int(f), keyframes[f]) for f in keyframes.keys()])
    
    # Build animation sequence
    animation_sequence = []
    
    for i, (frame, camera_data) in enumerate(sorted_frames):
        camera = Camera(camera_data)
        
        if i == 0:
            # First keyframe: no duration (instant)
            animation_sequence.append(set_camera(camera=camera, duration=0))
        else:
            # Calculate duration based on frame difference
            prev_frame = sorted_frames[i - 1][0]
            frame_diff = frame - prev_frame
            duration_ms = int((frame_diff / FRAME_RATE) * 1000)
            animation_sequence.append(set_camera(camera=camera, duration=duration_ms))
    
    return animation_sequence


if __name__ == '__main__':
    app.run(debug=True)
