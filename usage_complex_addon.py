import dash_molstar
from dash import Dash, html
from dash import Input, Output
from dash_molstar.utils import molstar_helper
from rdkit.Chem import AllChem
from rdkit.Chem import SDMolSupplier
from rdkit import Chem

app = Dash(__name__)
app.layout = html.Div(
    [
        dash_molstar.MolstarViewer(
            id="viewer", style={"width": "100%", "height": "600px"}
        ),
        html.Button("Load Protein", id="load_protein"),
        html.Button("focus", id="focus"),
    ],
    style={"width": "100%", "height": "100vh"},
)

@app.callback(
    Output("viewer", "data"),
    Input("load_protein", "n_clicks"),
    prevent_initial_call=True,
)
def display_output(yes):
    data = []
    
    mol = AllChem.MolFromSmiles("CCCCCC")
    AllChem.Compute2DCoords(mol)
    PDBBlock = AllChem.MolToPDBBlock(mol)
    data.append(molstar_helper.parse_molecule(PDBBlock, fmt="pdb", name="ligand0"))


    # mol = AllChem.MolFromSmiles("C1CCCCC1CC2CCCCC2C3CCCCC3C4=CC=CC=C4C5=CC=CC=C5C6=CC=CC=C6C7=CC=CC=C7C8=CC=CC=C8C9=CC=CC=C9C1=CC=CC=C1")
    # AllChem.Compute2DCoords(mol)
    # PDBBlock = AllChem.MolToPDBBlock(mol)
    # # Without a filename to infer format, the format has to be specified manually
    # # data.append(molstar_helper.parse_molecule(PDBBlock, fmt="pdb", name="ligand1"))
    # data.append(molstar_helper.parse_molecule(PDBBlock, fmt="pdb", name="ligand0-111111"))


    from pathlib import Path
    path = Path("./example/outputs/rank_0.sdf")
    file_data = molstar_helper.parse_molecule(
        path.read_text(),
        # pdb_block,
        fmt=path.suffix.replace(".", ""),
        # name=path.name
        name="ligand1"
        # name="ligand0-111111"
    )
    data.append(file_data)
    
    # mol = AllChem.MolFromSmiles("CCCCCC")
    # AllChem.Compute2DCoords(mol)
    # PDBBlock = AllChem.MolToPDBBlock(mol)
    # data.append(molstar_helper.parse_molecule(PDBBlock, fmt="pdb", name="ligand0"))

    
    
    # path2 = Path("./example/outputs/rank_29.sdf")
    # file_data = molstar_helper.parse_molecule(
    #     path2.read_text(),
    #     # pdb_block,
    #     fmt=path2.suffix.replace(".", ""),
    #     # name=path.name
    #     name="ligand1"
    #     # name="ligand0-111111"
    # )
    # data.append(file_data)
    
    
    # mol = AllChem.MolFromSmiles("CCCCCC")
    # AllChem.Compute2DCoords(mol)
    # PDBBlock = AllChem.MolToPDBBlock(mol)
    # data.append(molstar_helper.parse_molecule(PDBBlock, fmt="pdb", name="ligand0"))
    
    # targets = []
    # for name in molstar_helper.get_chain_names("protein.pdb"):
    #     targets.append(molstar_helper.get_targets(chain=name))
    # ag = molstar_helper.create_component("Polymer", targets, "molecular-surface")
    # # append "3u7y.pdb" into data
    # # return molstar_helper.parse_url('https://files.rcsb.org/download/3U7Y.pdb', component=[ag])
    # data.append(
    #     molstar_helper.parse_molecule("protein.pdb", component=[ag], name="protein")
    # )



    return data


@app.callback(
    Output("viewer", "focus"),
    Input("focus", "n_clicks"),
    prevent_initial_call=True,
)
def focusss(n_clicks):
    # ALA, ARG, ASN, ASP, ASX, CYS, GLN, GLU, GLY, GLX, HIS, ILE, LEU, LYS, MET, PHE, PRO, SER, THR, TRP, TYR, VAL, 1MA, 5MC, OMC, 1MG, 2MG, M2G, 7MG, 0MG, H2U, 5MU, PSU, ACE, FOR, HOH, UNK
    residue1 = molstar_helper.get_targets("UNL")
    # return molstar_helper.get_focus([residue1], analyse=True, molecule="ligand0-111111")
    # molstar_helper.get_focus([residue1], analyse=True, molecule="atom_num:38|mol_idx:11|smiles:CCCCCCCCCC|pdbid:ligd|real_atom:10|pred_atom:40.456329345703125|used_atom:38.456329345703125|auc:0|pred_lddt:0.9899556040763855")
    return molstar_helper.get_focus([residue1], analyse=True, molecule="ligand0")


if __name__ == "__main__":
    app.run_server(debug=True)