# from typing import List, Dict, Union
# import dash_molstar
# from pathlib import Path
# from dash_molstar.utils import molstar_helper
# from rdkit.Chem import AllChem
# from rdkit.Chem import SDMolSupplier

# from tests.base import Placeholder

    
# def get_mol_data_by_path(path: Union[Path, str], surface=False):
#     path = [ Path(p) if isinstance(p, str) else p for p in path ]
#     current_path = [p for p in path if p.exists()]
#     # current_path = sorted(current_path, key=lambda x: 1 if x.suffix == ".pdb" else 0)
#     file_data = []
#     for p in current_path:
#         if p.suffix == ".pdb":
#             targets = []
#             for name in get_chain_names(str(p)):
#                 targets.append(molstar_helper.get_targets(chain=name))

#             ag = molstar_helper.create_component("All", targets, "molecular-surface")
#             print("这里的 surface 是: ", surface)
#             file_data.append(
#                 molstar_helper.parse_molecule(
#                     str(p),
#                     component=[ag] if surface else [],
#                     name=p.name
#                 )
#             )
#         else:
#             file_data.append(
#                 molstar_helper.parse_molecule(
#                     p.read_text(),
#                     fmt=p.suffix.replace(".", ""),
#                     name=p.name,
#                     focus=True,
#                 )
#             )
#     if not file_data:
#         return None
#     # return render_mol(id=id, file_data=file_data, style=style)
#     return file_data


# def get_mol(data: Union[List, Dict] = None, style: Dict = {"height": "100%"}):
    
#     molstar = Placeholder.create(dash_molstar.MolstarViewer(
#         data=data, style=style,
#         # autoFocus=True
#     ))
    
    
#     def _add_mol(path: Union[Path, str], surface=False):
#         return get_mol_data_by_path(path, surface)

    
#     return molstar, _add_mol
    

# def render_mol(
#     id: str = "mol-viewer",
#     style: Dict = {"height": "100%"},
#     focus: str = "",
#     file_data: Union[List, Dict] = None,
# ):
#     if not file_data:
#         return []
#     # residue1 = molstar_helper.get_targets("UNL")
#     # return molstar_helper.get_focus([residue1], analyse=True, molecule="ligand0")
#     # test = molstar_helper.get_focus([residue1], analyse=True, molecule="ligand0")
#     return dash_molstar.MolstarViewer(id=id, data=file_data, style=style)


# def get_chain_names(pdb_file):
#     from Bio.PDB import PDBParser

#     parser = PDBParser()
#     structure = parser.get_structure("pdb_structure", pdb_file)
#     return [c.id for c in structure.get_chains()]


# def render_mol_with_path(
#     path: Path,
#     id: str = "mol-viewer",
#     style: dict = {"height": "100%", "width": "100%"},
# ):
#     if path.exists():
#         file_data = None
#         if path.suffix == ".pdb":
#             targets = []
#             for name in get_chain_names(str(path)):
#                 targets.append(molstar_helper.get_targets(chain=name))

#             ag = molstar_helper.create_component("All", targets, "molecular-surface")
#             print(33333)
#             file_data = molstar_helper.parse_molecule(
#                 str(path),
#                 component=[ag],
#                 name=path.name
#             )
#         else:
#             print(44444)
#             file_data = molstar_helper.parse_molecule(
#                 path.read_text(),
#                 fmt=path.suffix.replace(".", ""),
#                 name=path.name
#             )

#         return render_mol(id=id, file_data=file_data, style=style)
#     return None


# def render_mol_with_multi_path(
#     path: List[Union[Path, str]],
#     id: str = "mol-viewer",
#     style: Dict = {"height": "100%"},
# ):
#     path = [ Path(p) if isinstance(p, str) else p for p in path ]
#     current_path = [p for p in path if p.exists()]
#     current_path = sorted(current_path, key=lambda x: 1 if x.suffix == ".pdb" else 0)
#     file_data = []
#     for p in current_path:
#         if p.suffix == ".pdb":
#             targets = []
#             for name in get_chain_names(str(p)):
#                 targets.append(molstar_helper.get_targets(chain=name))

#             ag = molstar_helper.create_component("All", targets, "molecular-surface")
#             file_data.append(
#                 molstar_helper.parse_molecule(
#                     str(p),
#                     component=[ag],
#                       name=p.name
#                 )
#             )
#         else:
#             # print(11111111, p.read_text())
         
#             # suppl = SDMolSupplier(str(p))
#             # for mol in suppl:
#             #     print("这里的 p.name 是: ", p.name)
#             #     if mol is not None:
#             #         AllChem.Compute2DCoords(mol)
#             #         PDBBlock = AllChem.MolToPDBBlock(mol)
#             #         file_data.append(
#             #             molstar_helper.parse_molecule(PDBBlock, fmt="pdb", name=p.name)
#             #         )
            

#             file_data.append(
#                 molstar_helper.parse_molecule(
#                     p.read_text(),
#                     fmt=p.suffix.replace(".", ""),
#                     name=p.name
#                 )
#             )
#     if not file_data:
#         return None
#     return render_mol(id=id, file_data=file_data, style=style)





# # from typing import List, Dict, Union
# # import dash_molstar
# # from pathlib import Path
# # from dash_molstar.utils import molstar_helper


# # def render_mol(
# #     id: str = "mol-viewer",
# #     style: Dict = {"height": "100%"},
# #     focus: str = "",
# #     file_data: Union[List, Dict] = None,
# # ):
# #     if not file_data:
# #         return []
# #     # residue1 = molstar_helper.get_targets("UNL")
# #     # return molstar_helper.get_focus([residue1], analyse=True, molecule="ligand0")
# #     # test = molstar_helper.get_focus([residue1], analyse=True, molecule="ligand0")
# #     return dash_molstar.MolstarViewer(id=id, data=file_data, style=style)


# # def get_chain_names(pdb_file):
# #     from Bio.PDB import PDBParser

# #     parser = PDBParser()
# #     structure = parser.get_structure("pdb_structure", pdb_file)
# #     return [c.id for c in structure.get_chains()]


# # def render_mol_with_path(
# #     path: Path,
# #     id: str = "mol-viewer",
# #     style: dict = {"height": "100%", "width": "100%"},
# # ):
# #     if path.exists():
# #         file_data = None
# #         if path.suffix == ".pdb":
# #             targets = []
# #             for name in get_chain_names(str(path)):
# #                 targets.append(molstar_helper.get_targets(chain=name))

# #             ag = molstar_helper.create_component("All", targets, "molecular-surface")
# #             file_data = molstar_helper.parse_molecule(
# #                 str(path),
# #                 component=[ag],
# #                 name=path.name
# #             )
# #         else:
# #             file_data = molstar_helper.parse_molecule(
# #                 path.read_text(),
# #                 fmt=path.suffix.replace(".", ""),
# #                 name=path.name
# #             )

# #         return render_mol(id=id, file_data=file_data, style=style)
# #     return None


# # def render_mol_with_multi_path(
# #     path: List[Path],
# #     id: str = "mol-viewer",
# #     style: Dict = {"height": "100%"},
# # ):
# #     current_path = [p for p in path if p.exists()]
# #     current_path = sorted(current_path, key=lambda x: 1 if x.suffix == ".pdb" else 0)
# #     file_data = []
# #     for p in current_path:
# #         if p.suffix == ".pdb" and 0:
# #             targets = []
# #             for name in get_chain_names(str(p)):
# #                 targets.append(molstar_helper.get_targets(chain=name))

# #             ag = molstar_helper.create_component("All", targets, "molecular-surface")
# #             file_data.append(
# #                 molstar_helper.parse_molecule(
# #                     str(p),
# #                     component=[ag],
# #                       name=p.name
# #                 )
# #             )
# #         else:
# #             file_data.append(
# #                 molstar_helper.parse_molecule(
# #                     p.read_text(),
# #                     fmt=p.suffix.replace(".", ""),
# #                     name=p.name
# #                 )
# #             )

# #     if not file_data:
# #         return None
# #     return render_mol(id=id, file_data=file_data, style=style)


from typing import List, Dict, Union
import dash_molstar
from pathlib import Path
from dash_molstar.utils import molstar_helper
from .base import Placeholder

index = 1

MOL_VIEWER_PREFIX = "mol_viewer_prefix"


def get_mol_data_by_path(path: Union[Path, str], surface: bool = True):
    path = [Path(p) if isinstance(p, str) else p for p in path]
    current_path = [p for p in path if p.exists()]
    file_data = []
    for p in current_path:
        if p.suffix == ".pdb":
            targets = []
            for name in get_chain_names(str(p)):
                targets.append(molstar_helper.get_targets(chain=name))

            ag = molstar_helper.create_component("All", targets, "molecular-surface")
            print("这里的 surface 是: ", surface)
            file_data.append(
                molstar_helper.parse_molecule(
                    str(p),
                    component=[ag] if surface else [],
                    name=p.name,
                    focus=True,
                )
                # if surface
                # else molstar_helper.parse_molecule(
                #     str(p),
                #     component=None,
                #     name=p.name,
                #     focus=True,
                # )
            )
        else:
            file_data.append(
                molstar_helper.parse_molecule(
                    p.read_text(),
                    fmt=p.suffix.replace(".", ""),
                    name=p.name,
                    focus=True,
                )
            )
    if not file_data:
        return None
    return file_data


def get_mol(
    data: Union[List, Dict] = None,
    style: Dict = {"height": "100%"},
    focus: bool = True,
    id: str = "",
):
    global index
    molstar = Placeholder.create(
        # dash_molstar.MolstarViewer(data=data, style=style),
        dash_molstar.MolstarViewer(data=data, style=style),
        id=id or f"{MOL_VIEWER_PREFIX}_{index}",
    )

    if not id:
        index += 1

    def _add_mol(path: Union[Path, str], surface: bool = True):
        return get_mol_data_by_path(path, surface)

    return molstar, _add_mol


def render_mol(
    id: str = "mol-viewer",
    style: Dict = {"height": "100%"},
    focus: str = "",
    file_data: Union[List, Dict] = None,
):
    if not file_data:
        return []
    # residue1 = molstar_helper.get_targets("UNL")
    # return molstar_helper.get_focus([residue1], analyse=True, molecule="ligand0")
    # test = molstar_helper.get_focus([residue1], analyse=True, molecule="ligand0")
    return dash_molstar.MolstarViewer(id=id, data=file_data, style=style)


def get_chain_names(pdb_file):
    from Bio.PDB import PDBParser

    parser = PDBParser()
    structure = parser.get_structure("pdb_structure", pdb_file)
    return [c.id for c in structure.get_chains()]


def render_mol_with_path(
    path: Path,
    id: str = "mol-viewer",
    style: dict = {"height": "100%", "width": "100%"},
):
    if path.exists():
        file_data = None
        if path.suffix == ".pdb":
            targets = []
            for name in get_chain_names(str(path)):
                targets.append(molstar_helper.get_targets(chain=name))

            ag = molstar_helper.create_component("All", targets, "molecular-surface")
            file_data = molstar_helper.parse_molecule(
                str(path),
                component=[ag],
                # name=path.name
            )
        else:
            file_data = molstar_helper.parse_molecule(
                path.read_text(),
                fmt=path.suffix.replace(".", ""),
                # name=path.name
            )

        return render_mol(id=id, file_data=file_data, style=style)
    return None


def render_mol_with_multi_path(
    path: List[Path],
    id: str = "mol-viewer",
    style: Dict = {"height": "100%"},
):
    current_path = [p for p in path if p.exists()]
    current_path = sorted(current_path, key=lambda x: 1 if x.suffix == ".pdb" else 0)
    file_data = []
    for p in current_path:
        if p.suffix == ".pdb" and 0:
            targets = []
            for name in get_chain_names(str(p)):
                targets.append(molstar_helper.get_targets(chain=name))

            ag = molstar_helper.create_component("All", targets, "molecular-surface")
            file_data.append(
                molstar_helper.parse_molecule(
                    str(p),
                    component=[ag],
                    #   name=p.name
                )
            )
        else:
            file_data.append(
                molstar_helper.parse_molecule(
                    p.read_text(),
                    fmt=p.suffix.replace(".", ""),
                    # name=p.name
                )
            )

    if not file_data:
        return None
    return render_mol(id=id, file_data=file_data, style=style)
