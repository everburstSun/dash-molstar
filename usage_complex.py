import dash_molstar
from dash import Dash, html, Patch, State
from dash import Input, Output
from dash_molstar.utils import molstar_helper
from rdkit.Chem import AllChem
import dash_bootstrap_components as dbc
from dash_pane_split import DashPaneSplit


app = Dash(__name__)
app.layout = html.Div(
    [
        DashPaneSplit(
            splitMode="vertical",
            panelOrder="mainFirst",
            sidebarDefaultSize=200,
            mainChildren=dash_molstar.MolstarViewer(
                id="viewer", style={"width": "100%", "height": "100%"}
            ),
            sidebarChildren=[
                html.Button("Load Protein", id="load_protein"),
                html.Button("Remove First", id="remove_first"),
                html.Button("clear", id="clear"),
                html.Button("focus", id="focus"),
                html.Button("selection", id="selection"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Center"),
                                        dbc.Input(
                                            id="center_x",
                                            value=0,
                                            type="number",
                                            placeholder="x",
                                        ),
                                        dbc.Input(
                                            id="center_y",
                                            value=0,
                                            type="number",
                                            placeholder="y",
                                        ),
                                        dbc.Input(
                                            id="center_z",
                                            value=0,
                                            type="number",
                                            placeholder="z",
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Size"),
                                        dbc.Input(
                                            id="size_x",
                                            value=10,
                                            type="number",
                                            placeholder="x",
                                        ),
                                        dbc.Input(
                                            id="size_y",
                                            value=10,
                                            type="number",
                                            placeholder="y",
                                        ),
                                        dbc.Input(
                                            id="size_z",
                                            value=10,
                                            type="number",
                                            placeholder="z",
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                            ],
                            width=6,
                        ),
                    ]
                ),
                dbc.Button(id="add-box", children="Add Box"),
            ],
        ),
    ],
    style={"width": "100%", "height": "100vh"},
)


@app.callback(
    Output("viewer", "data", allow_duplicate=True),
    Input("clear", "n_clicks"),
    prevent_initial_call=True,
)
def clear(n_clicks):
    return []


@app.callback(
    Output("viewer", "data", allow_duplicate=True),
    Input("remove_first", "n_clicks"),
    prevent_initial_call=True,
)
def remove_first(n_clicks):
    data = []
    mol = AllChem.MolFromSmiles("CC(C1=CC=CC=C1)=O")
    AllChem.Compute2DCoords(mol)
    PDBBlock = AllChem.MolToPDBBlock(mol)
    # Without a filename to infer format, the format has to be specified manually
    data.append(molstar_helper.parse_molecule(PDBBlock, fmt="pdb", name="ligand0"))

    # mol = AllChem.MolFromSmiles("CCCCCC")
    # AllChem.Compute2DCoords(mol)
    # PDBBlock = AllChem.MolToPDBBlock(mol)
    # data.append(molstar_helper.parse_named_molecule("ligand", PDBBlock, fmt="pdb"))

    # suppl = SDMolSupplier('ligand.sdf')
    # for mol in suppl:
    #     if mol is not None:
    #         print("mol")
    #         AllChem.Compute2DCoords(mol)
    #         PDBBlock = AllChem.MolToPDBBlock(mol)
    #         data.append(molstar_helper.parse_molecule(PDBBlock, fmt="pdb"))

    # targets = []
    # for name in get_chain_names("protein.pdb"):
    #     targets.append(molstar_helper.get_targets(chain=name))
    # ag = molstar_helper.create_component("Antigen", targets, "molecular-surface")
    # # append "3u7y.pdb" into data
    # # return molstar_helper.parse_url('https://files.rcsb.org/download/3U7Y.pdb', component=[ag])
    # data.append(
    #     molstar_helper.parse_molecule(
    #         "7qo7.pdb", component=[ag]
    #     )
    # )
    # append a new molecule Acetophenone to data

    return data


@app.callback(
    Output("viewer", "data"),
    Input("load_protein", "n_clicks"),
    prevent_initial_call=True,
)
def display_output(yes):
    data = []

    mol = AllChem.MolFromSmiles("CC(C1=CC=CC=C1)=O")
    AllChem.Compute2DCoords(mol)
    PDBBlock = AllChem.MolToPDBBlock(mol)
    # Without a filename to infer format, the format has to be specified manually
    data.append(molstar_helper.parse_molecule(PDBBlock, fmt="pdb", name="ligand0"))

    mol = AllChem.MolFromSmiles("CCCCCC")
    AllChem.Compute2DCoords(mol)
    PDBBlock = AllChem.MolToPDBBlock(mol)
    data.append(molstar_helper.parse_molecule(PDBBlock, fmt="pdb", name="ligand1"))

    suppl = SDMolSupplier("ligand.sdf")
    for mol in suppl:
        if mol is not None:
            print("mol")
            AllChem.Compute2DCoords(mol)
            PDBBlock = AllChem.MolToPDBBlock(mol)
            data.append(
                molstar_helper.parse_molecule(PDBBlock, fmt="pdb", name="ligand2")
            )

    targets = []
    for name in molstar_helper.get_chain_names("protein.pdb"):
        targets.append(molstar_helper.get_targets(chain=name))
    ag = molstar_helper.create_component("Polymer", targets, "molecular-surface")
    # append "3u7y.pdb" into data
    # return molstar_helper.parse_url('https://files.rcsb.org/download/3U7Y.pdb', component=[ag])
    data.append(
        molstar_helper.parse_molecule("protein.pdb", component=[ag], name="protein")
    )

    return data


@app.callback(
    Output("viewer", "focus"),
    Input("focus", "n_clicks"),
    prevent_initial_call=True,
)
def focusss(n_clicks):
    residue1 = molstar_helper.get_targets("UNL")
    return molstar_helper.get_focus([residue1], analyse=True, molecule="ligand0")


@app.callback(
    Output("viewer", "selection"),
    Input("selection", "n_clicks"),
    prevent_initial_call=True,
)
def focusssselection(n_clicks):
    residue1 = molstar_helper.get_targets("All")
    return molstar_helper.get_selection(
        [residue1], select=True, add=True, molecule="ligand0"
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
def updateBox(n_clicks, center_x, center_y, center_z, size_x, size_y, size_z):
    patched_figure = Patch()
    _min = (center_x - size_x / 2, center_y - size_y / 2, center_z - size_z / 2)
    _max = (center_x + size_x / 2, center_y + size_y / 2, center_z + size_z / 2)
    box = molstar_helper.get_box(_min, _max)
    patched_figure.append(box)
    # data = []
    # mol = AllChem.MolFromSmiles("CC(C1=CC=CC=C1)=O")
    # AllChem.Compute2DCoords(mol)
    # PDBBlock = AllChem.MolToPDBBlock(mol)
    # # Without a filename to infer format, the format has to be specified manually
    # data.append(molstar_helper.parse_molecule(PDBBlock, fmt="pdb"))

    # targetAg = molstar_helper.get_targets(chain="G")
    # ag = molstar_helper.create_component("Antigen", [targetAg], "molecular-surface")
    # # append "3u7y.pdb" into data
    # # return molstar_helper.parse_url('https://files.rcsb.org/download/3U7Y.pdb', component=[ag])
    # data.append(
    #     molstar_helper.parse_url(
    #         "https://files.rcsb.org/download/3U7Y.pdb", component=[ag]
    #     )
    # )
    # # append a new molecule Acetophenone to data
    # data.append(box)
    return patched_figure


if __name__ == "__main__":
    app.run_server(debug=True)
