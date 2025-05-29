import json
import os

import dash
import dash_bootstrap_components as dbc
import dash_molstar
import pandas as pd
import plotly.express as px
from dash import (Dash, Input, Output, State, callback, clientside_callback,
                  ctx, dash_table, dcc, html, set_props)
from dash_molstar.utils import molstar_helper
from dash_molstar.utils.representations import Representation
from dash_molstar.utils.target import Target

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
        html.H1("Load Protein"),
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
    dbc.Row([
        dbc.Col([html.Strong("Current Focus"), html.Hr(style={'margin': '5px 0 10px 0'}),], width=6),
        dbc.Col([html.Strong("Current Selection"), html.Hr(style={'margin': '5px 0 10px 0'}),], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                data=[],
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '10px', 'width': '180px', 'maxWidth': '180px',
                },
                style_table={'overflowX': 'auto', 'height': '232px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left'},
                columns=[{'id': 'chain', 'name': 'chain', 'selectable': False}],
                selected_rows=[0],
                fixed_rows={'headers':True, 'data':0},
                id='focus-table-chain',
                row_selectable="single")
        ], width=2),
        dbc.Col([
            dash_table.DataTable(
                data=[],
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '10px', 'width': '180px', 'maxWidth': '180px',
                },
                style_table={'overflowX': 'auto', 'height': '232px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left'},
                columns=[{'id': 'residue', 'name': 'residue', 'selectable': False}],
                selected_rows=[0],
                fixed_rows={'headers':True, 'data':0},
                id='focus-table-res',
                row_selectable="single")
        ], width=2),
        dbc.Col([
            dash_table.DataTable(
                data=[],
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '10px', 'width': '180px', 'maxWidth': '180px',
                },
                style_table={'overflowX': 'auto', 'height': '232px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left'},
                columns=[{'id': 'atom', 'name': 'atom', 'selectable': False}],
                fixed_rows={'headers':True, 'data':0},
                id='focus-table-atom',
                row_selectable="single")
        ], width=2),
        dbc.Col([
            dash_table.DataTable(
                data=[],
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '10px', 'width': '180px', 'maxWidth': '180px',
                },
                style_table={'overflowX': 'auto', 'height': '232px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left'},
                columns=[{'id': 'chain', 'name': 'chain', 'selectable': False}],
                selected_rows=[0],
                fixed_rows={'headers':True, 'data':0},
                id='sel-table-chain',
                row_selectable="single")
        ], width=2),
        dbc.Col([
            dash_table.DataTable(
                data=[],
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '10px', 'width': '180px', 'maxWidth': '180px',
                },
                style_table={'overflowX': 'auto', 'height': '232px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left'},
                columns=[{'id': 'residue', 'name': 'residue', 'selectable': False}],
                selected_rows=[0],
                fixed_rows={'headers':True, 'data':0},
                id='sel-table-res',
                row_selectable="single")
        ], width=2),
        dbc.Col([
            dash_table.DataTable(
                data=[],
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'minWidth': '10px', 'width': '180px', 'maxWidth': '180px',
                },
                style_table={'overflowX': 'auto', 'height': '232px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left'},
                columns=[{'id': 'atom', 'name': 'atom', 'selectable': False}],
                fixed_rows={'headers':True, 'data':0},
                id='sel-table-atom',
                row_selectable="single")
        ], width=2)
    ]),
    html.Hr(style={'margin': '25px 0 25px 0'}),
    # Trajectory loading
    dbc.Row([
        html.H1("Load Trajectory"),
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
        html.H1("Load Shape"),
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

@callback(Output('viewer', 'hover'),
          Input('figure', 'hoverData'),
          prevent_initial_call=True)
def mouse_hover(hoverData):
    data = hoverData

    if not data: return molstar_helper.get_selection(None, add=False)

    residue1 = data['points'][0]['x']
    residue1 = molstar_helper.get_targets(residue1[0], residue1[1:], auth=True)
    residue2 = data['points'][0]['y']
    residue2 = molstar_helper.get_targets(residue2[0], residue2[1:], auth=True)

    seldata = molstar_helper.get_selection([residue1, residue2], add=False)

    return seldata

@callback(Input('figure', 'clickData'),
          State('onclick', 'value'),
          prevent_initial_call=True)
def mouse_click(clickData, onclick):
    data = clickData
    focusdata = dash.no_update

    residue1 = data['points'][0]['x']
    residue1 = molstar_helper.get_targets(residue1[0], residue1[1:], auth=True)
    residue2 = data['points'][0]['y']
    residue2 = molstar_helper.get_targets(residue2[0], residue2[1:], auth=True)

    seldata = molstar_helper.get_selection([residue1, residue2], add=False)
    focusdata = molstar_helper.get_focus([residue1, residue2], analyse=True)

    if onclick == '1':
        set_props('viewer', {'selection': seldata})
    elif onclick == '2':
        set_props('viewer', {'focus': focusdata})
    elif onclick == '3':
        set_props('viewer', {'selection': seldata})
        set_props('viewer', {'focus': focusdata})


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

@callback(Input('viewer', 'selection'),
          Input('viewer', 'focus'),
          prevent_initial_call=True)
def update_tables(selection, focus):
    if 'viewer.focus' in ctx.triggered_prop_ids.keys():
        if len(focus) == 1:
            target = Target(focus)
            chains = target.chains
            if chains:
                residues = chains[0].residues
                set_props('focus-table-chain', {'data': [{'chain': chain.name} for chain in chains]})
            else:
                residues = []
                set_props('focus-table-chain', {'data': [{'chain': ''}]})
            if residues:
                atoms = residues[0].atoms
                set_props('focus-table-res', {'data': [{'residue': f"{residue.number}{residue.ins_code}: {residue.name}"} for residue in residues]})
            else:
                atoms = []
                set_props('focus-table-res', {'data': [{'residue': ''}]})
            if atoms:
                set_props('focus-table-atom', {'data': [{'atom': f"{atom.index}: {atom.name}"} for atom in atoms]})
            else:
                set_props('focus-table-atom', {'data': [{'atom': ''}]})
    if 'viewer.selection' in ctx.triggered_prop_ids.keys():
        if len(selection) == 1:
            target = Target(selection)
            chains = target.chains
            if chains:
                residues = chains[0].residues
                set_props('sel-table-chain', {'data': [{'chain': chain.name} for chain in chains]})
            else:
                residues = []
                set_props('sel-table-chain', {'data': [{'chain': ''}]})
            if residues:
                atoms = residues[0].atoms
                set_props('sel-table-res', {'data': [{'residue': f"{residue.number}{residue.ins_code}: {residue.name}"} for residue in residues]})
            else:
                atoms = []
                set_props('sel-table-res', {'data': [{'residue': ''}]})
            if atoms:
                set_props('sel-table-atom', {'data': [{'atom': f"{atom.index}: {atom.name}"} for atom in atoms]})
            else:
                set_props('sel-table-atom', {'data': [{'atom': ''}]})

@callback(Input('focus-table-chain', 'selected_rows'),
          Input('focus-table-res', 'selected_rows'),
          Input('sel-table-chain', 'selected_rows'),
          Input('sel-table-res', 'selected_rows'),
          State('viewer', 'selection'), # In real use case, this should be cached
          State('viewer', 'focus'),     # at the server for performance.
          prevent_initial_call=True)
def table_update_cascade(focus_chain, focus_res, sel_chain, sel_res, selection, focus):
    selection = Target(selection)
    focus = Target(focus)
    if ctx.triggered_id == 'focus-table-chain':
        if focus_chain:
            chain = focus.chains[focus_chain[0]]
            residues = chain.residues
            res_focus = focus_res[0] if len(residues) >= focus_res[0] else 0
            if residues:
                atoms = residues[res_focus].atoms
                set_props('focus-table-res', {'data': [{'residue': f"{residue.number}{residue.ins_code}: {residue.name}"} for residue in residues]})
            else:
                atoms = []
                set_props('focus-table-res', {'data': [{'residue': ''}]})
            if atoms:
                set_props('focus-table-atom', {'data': [{'atom': f"{atom.index}: {atom.name}"} for atom in atoms]})
            else:
                set_props('focus-table-atom', {'data': [{'atom': ''}]})
    elif ctx.triggered_id == 'focus-table-res':
        chain = focus.chains[focus_chain[0]]
        residue = chain.residues[focus_res[0]]
        if focus_res:
            atoms = residue.atoms
            set_props('focus-table-atom', {'data': [{'atom': f"{atom.index}: {atom.name}"} for atom in atoms]})
    elif ctx.triggered_id == 'sel-table-chain':
        if sel_chain:
            chain = selection.chains[sel_chain[0]]
            residues = chain.residues
            res_sel = sel_res[0] if len(residues) >= sel_res[0] else 0
            if residues:
                atoms = residues[res_sel].atoms
                set_props('sel-table-res', {'data': [{'residue': f"{residue.number}{residue.ins_code}: {residue.name}"} for residue in residues]})
            else:
                atoms = []
                set_props('sel-table-res', {'data': [{'residue': ''}]})
            if atoms:
                set_props('sel-table-atom', {'data': [{'atom': f"{atom.index}: {atom.name}"} for atom in atoms]})
            else:
                set_props('sel-table-atom', {'data': [{'atom': ''}]})
    elif ctx.triggered_id == 'sel-table-res':
        chain = selection.chains[sel_chain[0]]
        residue = chain.residues[sel_res[0]]
        if sel_res:
            atoms = residue.atoms
            set_props('sel-table-atom', {'data': [{'atom': f"{atom.index}: {atom.name}"} for atom in atoms]})

def add_measurement():
    residue = molstar_helper.get_targets("H", 111)
    atoms = [
        molstar_helper.get_targets("H", 111, 890),
        molstar_helper.get_targets("H", 111, 891),
        molstar_helper.get_targets("H", 111, 892),
        molstar_helper.get_targets("H", 112, 898),
    ]
    measurements = [
        molstar_helper.get_measurement(residue, 'label'),
        molstar_helper.get_measurement(atoms[:2], 'distance'),
        molstar_helper.get_measurement(atoms[:3], 'angle'),
        molstar_helper.get_measurement(atoms, 'dihedral')
    ]
    return measurements

if __name__ == '__main__':
    app.run(debug=True)
