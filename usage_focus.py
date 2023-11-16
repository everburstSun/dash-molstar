from dash import Dash, html, ALL, ctx, callback
from dash import Input
from tests.molstar_test import (get_mol, get_mol_data_by_path)
from pathlib import Path

import json
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate



COMPARE_WITH_INPUT_LIGAND_KEY = "compare_with_input_ligand"
checkbox_styles = {
    "input": {
        ":checked": {
            "background-color": "#5a3196",
            "border-color": "#5a3196",
        }
    }
}

current_pdb = "./tests/3d20_protein.pdb"

app = Dash(__name__)

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

molstar_placeholder, add_mol = get_mol(data=get_mol_data_by_path([Path(current_pdb)]))

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
