import dash_molstar
from dash import Dash, callback, html, Input, Output
from dash_molstar.utils import molstar_helper
import dash_bootstrap_components as dbc

app = Dash(__name__, assets_folder='dash_molstar/bootstrap')

app.layout = html.Div(dbc.Row(dbc.Col([

    html.Button(id='load_protein', children="Load Protein"),
    dash_molstar.MolstarViewer(
        id='viewer',style={'width': '500px', 'height':'500px'}
    ),

], width=4)), className='container')


@callback(Output('viewer', 'data'), 
Input('load_protein', 'n_clicks'),
prevent_initial_call=True)
def display_output(yes):
    data = molstar_helper.get_data('3u7y.pdb')
    return data


if __name__ == '__main__':
    app.run_server(debug=True, )
