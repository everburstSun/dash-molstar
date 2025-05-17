import dash_molstar
from dash import Dash, callback, html, Input, Output, State, dcc, clientside_callback
import dash
import os
import json
import pandas as pd
import plotly.express as px
from dash_molstar.utils import molstar_helper
from dash_molstar.utils.representations import Representation
import dash_bootstrap_components as dbc

app = Dash(__name__, assets_folder='bootstrap')
df = pd.read_json(os.path.join("tests", "H_G_interaction.json"))

enable_outline = {
    'postprocessing': {
        'outline': Representation.np('on', {
            'scale': 1,
            'threshold': 0.33,
            'color': 0x000000,
            'includeTransparent': True
        })
    }
}

app.layout = html.Div([
    # Protein loading
    dbc.Row([
        dbc.Col([
            html.Button(id='load_protein', children="Load Protein", className="btn btn-primary", style={'padding': '5px', 'margin': '5px'}),
            html.Button(id='load_protein_rep', children="Load Protein With Component", className="btn btn-primary", style={'padding': '5px', 'margin': '5px'}),
            html.Button(id='load_protein_url', children="Load Protein From Internet", className="btn btn-primary", style={'padding': '5px', 'margin': '5px'}),
        ], className='mx-auto')
    ]),
    dbc.Row([
        dbc.Col([
            dash_molstar.MolstarViewer(
                id='viewer',style={'width': 'auto', 'height':'500px'}
            )
        ]),
        dbc.Col([
            dcc.Graph(id='figure', clear_on_unhover=True, figure=px.imshow(df, labels=dict(color="energy"), color_continuous_scale='Blues_r',range_color=[-80, 0], text_auto=True)),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("onClick Event"),
                    dbc.Select(
                        id="onclick",
                        options=[
                            {"label": "select", "value": '1'},
                            {"label": "focus", "value": '2'},
                            {"label": "select+focus", "value": '3'},
                        ],
                        value='2'
                    )
                ],
                className="mb-3",
            ),
        ])
    ]),
    html.Hr(style={'margin': '25px 0 25px 0'}),
    # Trajectory loading
    dbc.Row([
        dbc.Col([
            dash_molstar.MolstarViewer(
                id='viewer-2',style={'width': 'auto', 'height':'500px'},
                layout={'canvas3d': enable_outline}
            )
        ]),
        dbc.Col([
            html.Button(id='load_traj', children="Load Trajectory", className="btn btn-primary", style={'padding': '5px', 'margin': '5px'}),
            html.Br(),
            html.Span([html.Label("Current Frame Number: ", style={'margin': '10px 10px 50px 5px'}), html.Strong(id='frame_number')]),
            html.Br(),
            html.Label("Select Frame", style={'margin': '5px 0 5px 5px'}),
            dcc.Slider(1, 10, 1, value=1, id='frame_select',updatemode='drag'),
        ])
    ]),
    html.Hr(style={'margin': '25px 0 25px 0'}),
    # Shape loading
    dbc.Row([
        dbc.Col([
            dash_molstar.MolstarViewer(
                id='viewer-3',style={'width': 'auto', 'height':'500px'}
            )
        ]),
        dbc.Col([
            html.Button(id='load_protein_shapes', children="Load Shapes", className="btn btn-primary", style={'padding': '5px', 'margin': '5px'}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Strong("Box center:"),
                    dbc.InputGroup(
                            [
                                dbc.InputGroupText("x"),
                                dbc.Input(value=-1.6, type="number", id='center_x-box'),
                            ],
                            className="mb-3",
                        ),
                    dbc.InputGroup(
                            [
                                dbc.InputGroupText("y"),
                                dbc.Input(value=-0.8, type="number", id='center_y-box'),
                            ],
                            className="mb-3",
                        ),
                    dbc.InputGroup(
                            [
                                dbc.InputGroupText("z"),
                                dbc.Input(value=13.7, type="number", id='center_z-box'),
                            ],
                            className="mb-3",
                        ),
                ], width=6),
                dbc.Col([
                    html.Strong("Box size:"),
                    dbc.InputGroup(
                            [
                                dbc.InputGroupText("x"),
                                dbc.Input(value=10.3, type="number", id='size_x-box'),
                            ],
                            className="mb-3",
                        ),
                    dbc.InputGroup(
                            [
                                dbc.InputGroupText("y"),
                                dbc.Input(value=14.3, type="number", id='size_y-box'),
                            ],
                            className="mb-3",
                        ),
                    dbc.InputGroup(
                            [
                                dbc.InputGroupText("z"),
                                dbc.Input(value=13.8, type="number", id='size_z-box'),
                            ],
                            className="mb-3",
                        ),
                ], width=6)
            ])
        ])
    ])
], className='container')


@callback(Output('viewer', 'data'), 
          Input('load_protein', 'n_clicks'),
          prevent_initial_call=True)
def load_protein(yes):
    data = molstar_helper.parse_molecule(os.path.join('tests', '3u7y.pdb'))
    return data

@callback(Output('viewer', 'data', allow_duplicate=True), 
          Input('load_protein_url', 'n_clicks'),
          prevent_initial_call=True)
def load_protein_from_url(yes):
    data = molstar_helper.parse_url('https://files.rcsb.org/download/3U7Y.pdb')
    return data

@callback(Output('viewer', 'data', allow_duplicate=True), 
          Input('load_protein_rep', 'n_clicks'),
          prevent_initial_call=True)
def load_protein_with_rep(yes):
    # select the targets
    CDRs = [
        # CDRs on heavy chain
        molstar_helper.get_targets(chain="H", residue=[24,25,26,27,28,29,30,31,49,50,51,52,53,54,55,56,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109]),
        # CDRs on light chain
        molstar_helper.get_targets(chain="L", residue=[24,25,26,27,45,46,47,84,85,86,87,88])
    ]

    # create the components
    cdr_rep = Representation(type='orientation')
    cdr_rep.set_type_params({'alpha': 0.5})
    cdrs = molstar_helper.create_component("CDRs", CDRs, cdr_rep)
    ag_rep = Representation('molecular-surface')
    ag_rep.set_type_params({'xrayShaded': True})
    ag = molstar_helper.create_component("Antigen", molstar_helper.get_targets(chain="G"), ag_rep)

    component=[ag,cdrs]
    data = molstar_helper.parse_molecule(os.path.join('tests', '3u7y.pdb'), component=component)

    return data

@callback(Output('viewer-3', 'data'), 
          Input('load_protein_shapes', 'n_clicks'),
          prevent_initial_call=True)
def load_protein_with_shapes(yes):
    color_mapping = {
        'HydrogenDonor': 'white',
        'HydrogenAcceptor': 'orange',
        'Hydrophobic': 'green'
    }
    with open('./tests/pharmit.json') as f:
        shape_data = json.load(f)['points']

    surface = Representation('molecular-surface', 'uniform')
    surface.set_type_params({'xrayShaded': True})
    surface.set_color_params({'value': 0xD0D0D0})
    chainA = molstar_helper.create_component("ChainA", molstar_helper.get_targets(chain="A"), surface)

    component=[chainA]
    mol = molstar_helper.parse_molecule(os.path.join('tests', '7u28.cif'), component=component)
    shapes = [ molstar_helper.get_sphere(center=(shape['x'], shape['y'], shape['z']),
                                         radius=shape['radius'],
                                         label=shape['name'],
                                         color=color_mapping[shape['name']],
                                         opacity=0.7) 
              for shape in shape_data ]
    box = molstar_helper.get_box(min_xyz=(-6.76, -7.916, 6.788), max_xyz=(3.559, 6.406, 20.594))
    data = [mol, box]
    data.extend(shapes)

    return data

@dash.callback(
    Output('viewer-3', 'data', allow_duplicate=True),
    Input('center_x-box', 'value'),
    Input('center_y-box', 'value'),
    Input('center_z-box', 'value'),
    Input('size_x-box', 'value'),
    Input('size_y-box', 'value'),
    Input('size_z-box', 'value'),
    prevent_initial_call=True
)
def update_box(center_x, center_y, center_z, size_x, size_y, size_z):
    _min = (center_x-size_x/2, center_y-size_y/2, center_z-size_z/2)
    _max = (center_x+size_x/2, center_y+size_y/2, center_z+size_z/2)
    box = molstar_helper.get_box(_min, _max)
    return box

@callback(Output('viewer', 'selection'),
          Input('figure', 'hoverData'),
          prevent_initial_call=True)
def mouse_hover(hoverData):
    data = hoverData

    if not data: return molstar_helper.get_selection(None, select=False, add=False)

    residue1 = data['points'][0]['x']
    residue1 = molstar_helper.get_targets(residue1[0], residue1[1:], auth=True)
    residue2 = data['points'][0]['y']
    residue2 = molstar_helper.get_targets(residue2[0], residue2[1:], auth=True)

    seldata = molstar_helper.get_selection([residue1, residue2], select=False, add=False)

    return seldata

@callback(Output('viewer', 'selection', allow_duplicate=True),
          Output('viewer', 'focus'),
          Input('figure', 'clickData'),
          State('onclick', 'value'),
          prevent_initial_call=True)
def mouse_click(clickData, onclick):
    data = clickData
    focusdata = dash.no_update

    residue1 = data['points'][0]['x']
    residue1 = molstar_helper.get_targets(residue1[0], residue1[1:], auth=True)
    residue2 = data['points'][0]['y']
    residue2 = molstar_helper.get_targets(residue2[0], residue2[1:], auth=True)

    if onclick == '1':
        select = True
        focus = False
    elif onclick == '2':
        select = False
        focus = True
    elif onclick == '3':
        select = True
        focus = True

    seldata = molstar_helper.get_selection([residue1, residue2], select=select, add=False)
    if focus: focusdata = molstar_helper.get_focus([residue1, residue2], analyse=True)

    return seldata, focusdata

@callback(Output('viewer-2', 'data'), 
          Input('load_traj', 'n_clicks'),
          prevent_initial_call=True)
def load_traj(yes):
    chainA = molstar_helper.get_targets(chain="A")

    cartoon = Representation('cartoon', 'secondary-structure', 'uniform')
    surface = Representation('gaussian-surface', 'uniform', 'physical')
    surface.set_type_params({'radiusOffset': 0.3, 'ignoreHydrogens': True, 'alpha': 0.1})
    surface.set_color_params({'value': 0x009CE0})
    polymer = molstar_helper.create_component("polymer", chainA, [cartoon, surface])

    topo = molstar_helper.parse_molecule(os.path.join('tests', 'Villin.gro'), component=polymer, preset={'kind': 'empty'})
    coords = molstar_helper.parse_coordinate(os.path.join('tests', 'Villin.trr'))

    data = molstar_helper.get_trajectory(topo, coords)
    return data

clientside_callback(
    """
    function (value) {
        return value-1; // 0-based index for the frame
    }
    """,
    Output('viewer-2', 'frame'), 
    Input('frame_select', 'value'),
    prevent_initial_call=True
)

clientside_callback(
    """
    function (value) {
        return value+1; // 1-based index for the frame
    }
    """,
    Output('frame_number', 'children'),
    Input('viewer-2', 'frame'),
    prevent_initial_call=True
)


if __name__ == '__main__':
    app.run(debug=True)
