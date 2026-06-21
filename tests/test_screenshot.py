from dash.dependencies import Input, Output
from dash_molstar.helpers import parse_molecule, get_screenshot
from dash_molstar.utils import named_params, default_axes_params, Screenshot
import dash_molstar
from dash import Dash, html

mol_data = parse_molecule('3u7y.pdb')


uhd_transparent = Screenshot(
    resolution=named_params('ultra-hd'),
    transparent=True,
    axes=named_params('off'),
)
customize_resolution = Screenshot(
    resolution=named_params('custom', {'width': 4096, 'height': 4096}),
    transparent=False,
    axes=named_params('off'),
)
crop_viewport = Screenshot(
    resolution=named_params('ultra-hd'),
    transparent=False,
    axes=named_params('off'),
    illumination=None,
    crop={'x': 0.25, 'y': 0.25, 'width': 0.5, 'height': 0.5}
)
enable_axes = Screenshot(
    resolution=named_params('ultra-hd'),
    transparent=False,
    axes=named_params('on', default_axes_params),
)

app = Dash(__name__)
app.layout = html.Div([
    html.H3("Molstar Screenshot Demo"),
    dash_molstar.MolstarViewer(
        id='viewer', 
        style={'width': '800px', 'height':'600px'},
        data=mol_data
    ),
    html.Button("Download Screenshot", id='download-btn'),
])

@app.callback(
    Output("viewer", "screenshot"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_screenshot(n_clicks):
    # return get_screenshot(filename='uhd_transparent', params=uhd_transparent)
    # return get_screenshot(filename='customize_resolution', params=customize_resolution)
    # return get_screenshot(filename='crop_viewport', params=crop_viewport)
    return get_screenshot(filename='enable_axes', params=enable_axes)

if __name__ == '__main__':
    app.run(debug=True)