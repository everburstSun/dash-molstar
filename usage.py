import dash_molstar
from dash import Dash, callback, html, Input, Output, State, dcc, ctx
import dash
import pandas as pd
import plotly.express as px
from dash_molstar.utils import molstar_helper
import dash_bootstrap_components as dbc

app = Dash(__name__, assets_folder='bootstrap')
df = pd.read_json("H_G_interaction.json")
app.layout = html.Div([
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
    ])
], className='container')


@callback(Output('viewer', 'data'), 
          Input('load_protein', 'n_clicks'),
          Input('load_protein_rep', 'n_clicks'),
          Input('load_protein_url', 'n_clicks'),
          prevent_initial_call=True)
def load_protein(yes, yess, yesss):
    if not ctx.triggered_id == 'load_protein_url':
        CDRs = [
            # CDRs on heavy chain
            molstar_helper.get_targets(chain="H", residue=[24,25,26,27,28,29,30,31,49,50,51,52,53,54,55,56,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109]),
            # CDRs on light chain
            molstar_helper.get_targets(chain="L", residue=[24,25,26,27,45,46,47,84,85,86,87,88])
        ]
        cdrs = molstar_helper.create_component("CDRs", CDRs, 'orientation')
        ag = molstar_helper.create_component("Antigen", molstar_helper.get_targets(chain="G"), 'molecular-surface')
        #ag = molstar_helper.create_component("Antigen", molstar_helper.get_targets(chain="G"), 'ball-and-stick')

        component = None
        if ctx.triggered_id == 'load_protein_rep':
            component = [ag, cdrs]
        data = molstar_helper.parse_molecule('3u7y.pdb', component=component)
    else:
        data = molstar_helper.parse_url('https://files.rcsb.org/download/3U7Y.pdb')
    return data


@callback(Output('viewer', 'selection'),
          Output('viewer', 'focus'),
          Input('figure', 'hoverData'),
          Input('figure', 'clickData'),
          State('onclick', 'value'),
          prevent_initial_call=True)
def mouse_event(hoverData, clickData, onclick):
    focusdata = dash.no_update
    if ctx.triggered_prop_ids.get('figure.hoverData'):
        data = hoverData
        select = False
        focus = False
    else:
        data = clickData
        if onclick == '1':
            select = True
            focus = False
        elif onclick == '2':
            select = False
            focus = True
        elif onclick == '3':
            select = True
            focus = True
    if not data: return molstar_helper.get_selection([], select=select, add=False), focusdata
    residue1 = data['points'][0]['x']
    residue1 = molstar_helper.get_targets(residue1[0], residue1[1:])
    residue2 = data['points'][0]['y']
    residue2 = molstar_helper.get_targets(residue2[0], residue2[1:])
    seldata = molstar_helper.get_selection([residue1, residue2], select=select, add=True)
    if focus: focusdata = molstar_helper.get_focus([residue1, residue2], analyse=True)
    return seldata, focusdata



if __name__ == '__main__':
    app.run_server(debug=True, )
