from dash import Dash, html, ALL, ctx, callback
from dash import Input, Output
from tests.molstar_test import (get_mol, get_mol_data_by_path)
from pathlib import Path

import json
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate

from tests.select import select_with_on_change

select_placeholer, on_change = select_with_on_change()


COMPARE_WITH_INPUT_LIGAND_KEY = "compare_with_input_ligand"
HIDDEN_INPUT_PROTEIN_SURFACE = "hidden_input_protein_surface"

checkbox_styles = {
    "input": {
        ":checked": {
            "background-color": "#5a3196",
            "border-color": "#5a3196",
        }
    }
}

# current_pdb = "./tests/3d20_protein.pdb"
current_pdb = "./dash-example-protein.pdb"

app = Dash(__name__)
tmp = None

ligand_file_json = None
with open("./tests/outputs/result.vdgen.json", "r") as file:
    ligand_file_json = json.load(file)

options = [
    {
        "name": ligand_file_json[i]["ligand_path"],
        "rank": ligand_file_json[i]["rank_order"],
        "energy": ligand_file_json[i]["energy"],
        "path":  Path("./tests/outputs") / f"{ligand_file_json[i]['ligand_path']}",
    }
    for i in range(len(ligand_file_json))
]


common_style = {"padding": "0 16px", "borderBottom": "1px solid #eee"}

molstar_placeholder, add_mol = get_mol(data=get_mol_data_by_path([Path(current_pdb)], False))

app.layout = html.Div(
    [
        html.Div(
            molstar_placeholder.get_element(),
            style={
                "width": "100%",
                "height": 600
            },
            id="test-1"
        ),
        dmc.Button("Add Pockets", id="add-pockets", style={"margin": "16px"}),
        dmc.Button("Add Surface", id="add-surface", style={"margin": "16px"}),
        dmc.Button("Show PDB", id="show-pdb", style={"margin": "16px"}),
        dmc.Select(
            data=[],
            placeholder="Select a pocket",
            id="select-test"
        ),
        html.Div(
            [
                    dmc.Card(
                        children=[
                            dmc.CardSection(
                                dmc.Group(
                                    [
                                        dmc.Text(ligand.get("name"), weight=500),
                                        dmc.Checkbox(
                                            id={
                                                "type": COMPARE_WITH_INPUT_LIGAND_KEY,
                                                "ligand_path": str(ligand.get("path")),
                                            },
                                            label="Compare with input ligand",
                                            styles={
                                                "label": {"padding-left": "6px"},
                                                **checkbox_styles,
                                            },
                                        ),
                                    ],
                                    position="apart",
                                    mt="md",
                                    mb="xs",
                                ),
                                style=common_style,
                            ),
                            dmc.CardSection(
                                dmc.List(
                                    [
                                        dmc.ListItem(
                                            dmc.Text(
                                                f"Path: {ligand.get('path')}",
                                                size="sm",
                                                color="dimmed",
                                            )
                                        ),
                                    ]
                                ),
                                style={
                                    **common_style,
                                    "paddingTop": "16px",
                                    "paddingBottom": "16px",
                                },
                            ),
                        ],
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        style={"width": 350, "margin": "16px"},
                    )
                    for ligand in options
                ],
            style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "width": "100%", "height": 600},
        )
    ]
)


curent_checked_compare_ligands = []

@callback(
    # molstar_placeholder.get_output(component_property="data", allow_duplicate=True),
    Output("select-test", "data"),
    Input("add-pockets", "n_clicks"),
    prevent_initial_call=True,
)
def handler_add_pockets(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    import pandas
    output = "dash-example-output/dash-example-protein.pdb_predictions.csv"
    df = pandas.read_csv(output)
    df = df.rename(columns=lambda x: x.strip())
    data = df.to_dict("records")
    options = [{"label": d["name"], "value": json.dumps(d)} for d in data]
    return options

show = True
@callback(
    molstar_placeholder.get_output(component_property="data", allow_duplicate=True),
    Input("show-pdb", "n_clicks"),
    prevent_initial_call=True,
)
def handler_add_surface(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    # if n_clicks % 2 == 0:
    #     return add_mol([current_pdb], False)
    global show
    show = not show
    return add_mol([current_pdb], False) if show else add_mol([], False)


@callback(
    molstar_placeholder.get_output(component_property="data", allow_duplicate=True),
    Input("add-surface", "n_clicks"),
    prevent_initial_call=True,
)
def handler_add_surface(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    # if n_clicks % 2 == 0:
    #     return add_mol([current_pdb], False)
    global tmp
    tmp = not tmp
    res = add_mol([current_pdb], tmp)
    return res

@callback(
    molstar_placeholder.get_output(component_property="selection", allow_duplicate=True),
    Input("select-test", "value"),
    prevent_initial_call=True,
)
def handler_select_test(value):
    # if not data:
    # print("这里的 data 是什么？", data)
    from collections import defaultdict
    from dash_molstar.utils import molstar_helper

    # raise PreventUpdate
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
    return molstar_helper.get_selection(selections, rotate=True, select=True, add=False, molecule=Path(current_pdb).name)


@callback(
    molstar_placeholder.get_output(component_property="data", allow_duplicate=True),
    Input(
        {
            "type": COMPARE_WITH_INPUT_LIGAND_KEY,
            "ligand_path": ALL,
        },
        "checked",
    ),
    prevent_initial_call=True,
)
def handle_compare_with_input_ligand_checked(is_checked):
    if not list(filter(lambda x: x is not None, is_checked)):
        raise PreventUpdate

    current_id = ctx.triggered_id
    current_is_checked = ctx.triggered[0]["value"]

    current_path = current_id.get("ligand_path", "")

    current_actived_job_checked = curent_checked_compare_ligands
    if current_is_checked and current_path not in current_actived_job_checked:
        current_actived_job_checked.append(current_path)
    else:
        current_path in current_actived_job_checked and current_actived_job_checked.remove(
            current_path
        )

    all_paths = [current_pdb, *current_actived_job_checked]
    all_paths = [Path(p) for p in all_paths]
    return add_mol(all_paths)


if __name__ == "__main__":
    app.run_server(debug=True)