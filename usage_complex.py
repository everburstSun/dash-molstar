from collections import defaultdict
import sh
import pandas
import json
import dash_molstar
from dash import Dash, html, Patch, State, ctx, no_update
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
                autoFocus=False,
                id="viewer",
                style={"width": "100%", "height": "100%"},
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
                        dbc.Button(
                            "Load Pockets",
                            id="load_pockets",
                            style={"marginTop": "5px"},
                            size="sm",
                        ),
                        dbc.Select(
                            options=[],
                            id="pockets",
                            disabled=True,
                            placeholder="Select pocket",
                            style={"marginTop": "5px"},
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
    Output("viewer", "selection", allow_duplicate=True),
    Output("viewer", "focus", allow_duplicate=True),
    Input("clear_all", "n_clicks"),
    prevent_initial_call=True,
)
def clear_all(n_clicks):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate
    return [], None, None


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
        if d.get("label", None) == "Target Protein":
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
        if d.get("label", None) == "Target Protein":
            raise PreventUpdate
    patch = Patch()
    targets = []
    for name in molstar_helper.get_chain_names("dash-example-protein.pdb"):
        targets.append(molstar_helper.get_targets(chain=name))
    ag = molstar_helper.create_component("Polymer", targets, "molecular-surface")
    patch.append(
        molstar_helper.parse_molecule(
            "dash-example-protein.pdb", component=[ag], name="Target Protein"
        )
    )
    return patch


@app.callback(
    [
        Output("pockets", "options", allow_duplicate=True),
        Output("pockets", "disabled", allow_duplicate=True),
        Output("pockets", "value", allow_duplicate=True),
    ],
    Input("load_pockets", "n_clicks"),
    State("viewer", "data"),
    prevent_initial_call=True,
)
def load_pockets(n_clicks, data):
    if not n_clicks or len(ctx.triggered) > 1:
        raise PreventUpdate

    loaded = False
    for d in data:
        if d.get("label", None) == "Target Protein":
            loaded = True

    if not loaded:
        raise PreventUpdate

    # cmd = sh.Command("./p2rank_2.4/prank")
    # cmd("predict", "-f", "dash-example-protein.pdb", "-o", "dash-example-output")
    output = "dash-example-output/dash-example-protein.pdb_predictions.csv"
    df = pandas.read_csv(output)
    df = df.rename(columns=lambda x: x.strip())
    data = df.to_dict("records")
    options = [{"label": d["name"], "value": json.dumps(d)} for d in data]
    return options, False, options[0]["value"]


@app.callback(
    Output("viewer", "selection", allow_duplicate=True),
    Input("pockets", "value"),
    State("viewer", "data"),
    prevent_initial_call=True,
)
def select_pocket(value, data):
    if not value or len(ctx.triggered) > 1:
        raise PreventUpdate
    found = False
    for d in data:
        if d.get("label", None) == "Target Protein":
            found = True

    if not found:
        raise PreventUpdate
    data = json.loads(value)
    residue_ids = data["residue_ids"].strip().split()
    targets = defaultdict(list)
    selections = []
    for residue_id in residue_ids:
        chain_name, residue_number = residue_id.split("_")
        targets[chain_name].append(residue_number)
    for chain_name, residue_numbers in targets.items():
        selections.append(
            molstar_helper.get_targets(chain=chain_name, residue=residue_numbers)
        )
    return molstar_helper.get_selection(selections, rotate=True, select=True, add=False, molecule="Target Protein")


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
        if d.get("label", None) == "Ligand Original":
            raise PreventUpdate
    patch = Patch()
    with open("dash-example-ligand-origin.sdf") as f:
        patch.append(
            molstar_helper.parse_molecule(f.read(), fmt="sdf", name="Ligand Original")
        )
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
    found = False
    for d in data:
        if d.get("label", None) == "Ligand Original":
            found = True
    if not found:
        raise PreventUpdate
    residue_all = molstar_helper.get_targets("UNL")
    return molstar_helper.get_focus(
        [residue_all], analyse=True, molecule="Ligand Original"
    )


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
        if d.get("label", None) == "Ligand Original":
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
        if d.get("label", None) == "Ligand Optimized":
            raise PreventUpdate
    patch = Patch()
    with open("dash-example-ligand-result.sdf") as f:
        patch.append(
            molstar_helper.parse_molecule(f.read(), fmt="sdf", name="Ligand Optimized")
        )
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
        if d.get("label", None) == "Ligand Optimized":
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
    found = False
    for d in data:
        if d.get("label", None) == "Ligand Optimized":
            found = True
    if not found:
        raise PreventUpdate
    residue_all = molstar_helper.get_targets("UNL")
    return molstar_helper.get_focus(
        [residue_all], analyse=True, molecule="Ligand Optimized"
    )


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
