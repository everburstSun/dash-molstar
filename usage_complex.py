import dash_molstar
from dash import Dash, html, Patch, State, ctx
from dash import Input, Output
from dash.exceptions import PreventUpdate
from dash_molstar.utils import molstar_helper
import dash_bootstrap_components as dbc
from dash_pane_split import DashPaneSplit


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(
    [
        DashPaneSplit(
            splitMode="vertical",
            panelOrder="mainFirst",
            sidebarDefaultSize=300,
            mainChildren=dash_molstar.MolstarViewer(
                data=[],
                autoFocus=True,
                id="viewer", style={"width": "100%", "height": "100%"}
            ),
            sidebarStyle={"padding": "1rem"},
            sidebarChildren=[
                dbc.Row(
                    children=[
                        dbc.Label("Protein"),
                        dbc.Button(
                            "Load Protein",
                            id="load_protein",
                            style={"marginTop": "5px"},
                            size="sm",
                        ),
                        dbc.Button(
                            "Remove Protein",
                            id="remove_protein",
                            style={"marginTop": "5px"},
                            size="sm",
                        ),
                    ]
                ),
                html.Hr(),
                dbc.Row(
                    children=[
                        dbc.Label("Ligand Original"),
                        dbc.Button(
                            "Load Ligand",
                            id="load_ligand_original",
                            style={"marginTop": "5px"},
                            size="sm",
                        ),
                        dbc.Button(
                            "Remove Ligand",
                            id="remove_ligand_original",
                            style={"marginTop": "5px"},
                            size="sm",
                        ),
                        dbc.Button(
                            "Focus Ligand",
                            id="focus_ligand_original",
                            style={"marginTop": "5px"},
                            size="sm",
                        ),
                    ]
                ),
                html.Hr(),
                dbc.Row(
                    children=[
                        dbc.Label("Ligand Optimized"),
                        dbc.Button(
                            "Load Ligand",
                            id="load_ligand_optimized",
                            style={"marginTop": "5px"},
                            size="sm",
                        ),
                        dbc.Button(
                            "Remove Ligand",
                            id="remove_ligand_optimized",
                            style={"marginTop": "5px"},
                            size="sm",
                        ),
                        dbc.Button(
                            "Focus Ligand",
                            id="focus_ligand_optimized",
                            style={"marginTop": "5px"},
                            size="sm",
                        ),
                    ]
                ),
                html.Hr(),
                dbc.Row(
                    children=[
                        dbc.Label("Box Center"),
                        dbc.Input(
                            id="center_x",
                            value=0,
                            type="number",
                            placeholder="x",
                            size="sm",
                        ),
                        dbc.Input(
                            id="center_y",
                            value=0,
                            type="number",
                            placeholder="y",
                            size="sm",
                        ),
                        dbc.Input(
                            id="center_z",
                            value=0,
                            type="number",
                            placeholder="z",
                            size="sm",
                        ),
                        dbc.Label("Box Size"),
                        dbc.Input(
                            id="size_x",
                            value=10,
                            type="number",
                            placeholder="x",
                            size="sm",
                        ),
                        dbc.Input(
                            id="size_y",
                            value=10,
                            type="number",
                            placeholder="y",
                            size="sm",
                        ),
                        dbc.Input(
                            id="size_z",
                            value=10,
                            type="number",
                            placeholder="z",
                            size="sm",
                        ),
                        dbc.Button(id="add-box", children="Add Box", size="sm"),
                    ]
                ),
                html.Hr(),
                dbc.Row(
                    children=[
                        dbc.Button("Clear All", id="clear_all", size="sm"),
                    ]
                ),
            ],
        ),
    ],
    style={"width": "100%", "height": "100vh"},
)


@app.callback(
    Output("viewer", "data", allow_duplicate=True),
    Input("clear_all", "n_clicks"),
    prevent_initial_call=True,
)
def clear_all(n_clicks):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    return []


@app.callback(
    Output("viewer", "data", allow_duplicate=True),
    Input("remove_protein", "n_clicks"),
    State("viewer", "data"),
    prevent_initial_call=True,
)
def remove_protein(n_clicks, data):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    patch = Patch()
    for i, d in enumerate(data):
        if d.get('label', None) == "Target Protein":
            del patch[i]
    return patch


@app.callback(
    Output("viewer", "data", allow_duplicate=True),
    Input("load_protein", "n_clicks"),
    State("viewer", "data"),
    prevent_initial_call=True,
)
def load_protein(n_clicks, data):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    for d in data:
        if d.get('label', None) == "Target Protein":
            raise PreventUpdate
    patch = Patch()
    targets = []
    for name in molstar_helper.get_chain_names("dash-example-protein.pdb"):
        targets.append(molstar_helper.get_targets(chain=name))
    ag = molstar_helper.create_component("Polymer", targets, "molecular-surface")
    patch.append(
        molstar_helper.parse_molecule("dash-example-protein.pdb", component=[ag], name="Target Protein")
    )
    return patch


@app.callback(
    Output("viewer", "data", allow_duplicate=True),
    Input("load_ligand_original", "n_clicks"),
    State("viewer", "data"),
    prevent_initial_call=True,
)
def load_ligand_original(n_clicks, data):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    for d in data:
        if d.get('label', None) == "Ligand Original":
            raise PreventUpdate
    patch = Patch()
    with open("dash-example-ligand-origin.sdf") as f:
        patch.append(molstar_helper.parse_molecule(f.read(), fmt="sdf", name="Ligand Original"))
    return patch

@app.callback(
    Output("viewer", "focus", allow_duplicate=True),
    Input("focus_ligand_original", "n_clicks"),
    State("viewer", "data"),
    prevent_initial_call=True,
)
def focus_ligand_original(n_clicks, data):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    for d in data:
        if d.get('label', None) == "Ligand Original":
            raise PreventUpdate
    residue_all = molstar_helper.get_targets("UNL")
    return molstar_helper.get_focus([residue_all], analyse=True, molecule="Ligand Original")

@app.callback(
    Output("viewer", "data", allow_duplicate=True),
    Input("remove_ligand_original", "n_clicks"),
    State("viewer", "data"),
    prevent_initial_call=True,
)
def remove_ligand_original(n_clicks, data):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    patch = Patch()
    for i, d in enumerate(data):
        if d.get('label', None) == "Ligand Original":
            del patch[i]
    return patch



@app.callback(
    Output("viewer", "data"),
    Input("load_ligand_optimized", "n_clicks"),
    State("viewer", "data"),
    prevent_initial_call=True,
)
def load_ligand_optimized(n_clicks, data):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    for d in data:
        if d.get('label', None) == "Ligand Optimized":
            raise PreventUpdate
    patch = Patch()
    with open("dash-example-ligand-result.sdf") as f:
        patch.append(molstar_helper.parse_molecule(f.read(), fmt="sdf", name="Ligand Optimized"))
    return patch

@app.callback(
    Output("viewer", "data", allow_duplicate=True),
    Input("remove_ligand_optimized", "n_clicks"),
    State("viewer", "data"),
    prevent_initial_call=True,
)
def remove_ligand_optimized(n_clicks, data):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    patch = Patch()
    for i, d in enumerate(data):
        if d.get('label', None) == "Ligand Optimized":
            del patch[i]
    return patch

@app.callback(
    Output("viewer", "focus", allow_duplicate=True),
    Input("focus_ligand_optimized", "n_clicks"),
    State("viewer", "data"),
    prevent_initial_call=True,
)
def focus_ligand_optimized(n_clicks, data):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    for d in data:
        if d.get('label', None) == "Ligand Optimized":
            raise PreventUpdate
    residue_all = molstar_helper.get_targets("UNL")
    return molstar_helper.get_focus([residue_all], analyse=True, molecule="Ligand Optimized")


@app.callback(
    Output("viewer", "data", allow_duplicate=True),
    Input("add-box", "n_clicks"),
    State("center_x", "value"),
    State("center_y", "value"),
    State("center_z", "value"),
    State("size_x", "value"),
    State("size_y", "value"),
    State("size_z", "value"),
    prevent_initial_call=True,
)
def add_box(n_clicks, center_x, center_y, center_z, size_x, size_y, size_z):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    patched = Patch()
    _min = (center_x - size_x / 2, center_y - size_y / 2, center_z - size_z / 2)
    _max = (center_x + size_x / 2, center_y + size_y / 2, center_z + size_z / 2)
    box = molstar_helper.get_box(_min, _max)
    patched.append(box)
    return patched


if __name__ == "__main__":
    app.run_server(debug=True)
