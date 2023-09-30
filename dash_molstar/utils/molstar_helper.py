from io import IOBase
import os
from urllib.parse import urlparse


def parse_molecule(inp, fmt=None, component=None):
    """
    Parse the molecule for `data` parameter of molstar viewer.

    Parameters
    ----------
    `inp` — str | file-like object
        The file path to molecule or the file content of molecule.

        If `inp` was set to file path, the format can be automatically determined.
        Otherwise the format has to be specified manually.
    `fmt` — str (optional)
        Format of the input molecule. 
        Supported formats include `cif`, `cifcore`, `pdb`, `pdbqt`, `gro`, `xyz`, `mol`, `sdf`, `mol2` (default: `None`)
    `component` — dict | List[dict] (optional)
        Component to be created in molstar. 
        If not specified, molstar will use its default settings. (default: `None`)

        Use helper function `create_component` to generate correct data for this parameter.

    Returns
    -------
    `dict`
        The value for the `data` parameter.

    Raises
    ------
    `RuntimeError`
        If the input format is not supported by molstar viewer, raises RuntimeError.
    """
    # provided a filename as input
    if os.path.isfile(inp):
        # if format is not specified, infer from filename
        if not fmt:
            name, fmt = os.path.splitext(inp)
        with open(inp, 'r') as f:
            data = f.read()
    else:
        # provided a file-like object as input
        if isinstance(inp, IOBase):
            data = inp.read()
        # provided file content as input
        else:
            data = inp
        if type(data) == bytes: data = data.decode()
    if not fmt: raise RuntimeError("The format must be specified if you haven't provided a file name.")
    fmt = fmt.strip('.').lower()
    if fmt not in ["cif", "cifcore", "pdb", "pdbqt", "gro", "xyz", "mol", "sdf", "mol2"]:
        raise RuntimeError(f"The input file format \"{fmt}\" is not supported by molstar.")
    if fmt == 'cif': fmt = 'mmcif'
    if fmt == 'cifcore': fmt = 'cifCore'
    d = {
        "type": 'mol',
        "data": data,
        "format": fmt
    }
    if component: d['component'] = component
    return d

def parse_url(url, fmt=None, component=None, mol=True):
    """
    Parse the URL for `data` parameter of molstar viewer. 
    The url can be either a structure and a molstar state/session file.

    Parameters
    ----------
    `url` — str
        The URL to the molecule.
    `fmt` — str (optional)
        Format of the input molecule. (default: `None`)

        Supported formats of structures include `cif`, `cifcore`, `pdb`, `pdbqt`, `gro`, `xyz`, `mol`, `sdf`, `mol2` 

        Supported formats of states and sessions include `json`, `molj`, `molx`, `zip`
    `component` — dict | List[dict] (optional)
        Component to be created in molstar. 
        If not specified, molstar will use its default settings. (default: `None`)

        Use helper function `create_component` to generate correct data for this parameter.
    `mol` — bool (optional)
        If the url is a structure file, set `mol=True`.
        If the url is a molstar state or session file, set `mol=False`.

    Returns
    -------
    `dict`
        The value for the `data` parameter.
    """
    # try to automatically infer file format
    parsed_url = urlparse(url)
    if not fmt:
        name, fmt = os.path.splitext(parsed_url.path)
    if not fmt:
        raise RuntimeError("The format must be specified if you are not providing static resources.")
    fmt = fmt.strip('.').lower()
    if mol and fmt not in ["cif", "cifcore", "pdb", "pdbqt", "gro", "xyz", "mol", "sdf", "mol2"]:
        raise RuntimeError(f"The input file format \"{fmt}\" is not supported by molstar.")
    if not mol and fmt not in ["json", "molj", "molx", "zip"]:
        raise RuntimeError(f"The input file format \"{fmt}\" is not supported by molstar.")
    if fmt == 'cif': fmt = 'mmcif'
    if fmt == 'cifcore': fmt = 'cifCore'
    d = {
        "type": 'url',
        "urlfor": 'mol' if mol else 'snapshot',
        "data": url,
        "format": fmt
    }
    if component: d['component'] = component
    return d

def get_box(min_xyz=(0,0,0), max_xyz=(1,1,1), radius=0.1, label="Bounding Box", color='red'):
    """
    Generate a bounding box in the viewer with given parameters.

    Parameters
    ----------
    `min_xyz` — tuple (optional)
        Minimum of x, y and z values (default: `(0,0,0)`)
    `max_xyz` — tuple (optional)
        Maximum of x, y and z values (default: `(1,1,1)`)
    `radius` — float (optional)
        Border radius in angstrom (default: `0.1`)
    `label` — str (optional)
        The box label to be shown in the viewer (default: `"Bounding Box"`)
    `color` — str (optional)
        X11 color names (default: `'red'`)
        Avaliable options can be found at [here](https://www.w3.org/TR/css-color-3/#svg-color)

    Returns
    -------
    `dict`
        Dict for the `data` parameter of MolstarViewer

    Raises
    ------
    `ValueError`
        Raised if input coordinates are not 3-dimensional
    """
    if len(min_xyz) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    if len(max_xyz) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    return {
        'type': 'shape',
        'shape': 'box',
        'min': min_xyz,
        'max': max_xyz,
        'radius': radius,
        'label': label,
        'color': color
    }

def get_sphere(center, radius):
    pass

def get_targets(chain, residue=None, auth=False):
    """
    Select residues from a given chain. If no residue was specified, the entire chain will be selected.

    Parameters
    ----------
    `chain` — str
        Name of the target chain
    `residue` — int | List[int] (optional)
        Residue index of the target residues, started from 0. (default: `None`)
    `auth` — bool (optional)
        If a cif file was loaded, set `auth` to `True` to select the authentic chain names and residue numbers (default: `False`)

    Returns
    -------
    `dict`
        Selected residues
    """
    target = {'chain_name': chain, 'auth': auth}
    if residue:
        if type(residue) != list: residue = [residue]
        residues = []
        for res in residue:
            if type(res) == int: residues.append(res)
            elif type(res) == str:
                try:
                    num = eval(res)
                    residues.append(num)
                except SyntaxError:
                    residues.append(res)
        target['residue_numbers'] = residues
    return target

def create_component(label, targets, representation='cartoon'):
    """
    Generate the component information for selected targets.

    Parameters
    ----------
    `label` — str
        Name of the component
    `targets` — dict | List[dict]
        List of targets, whose value should be generated by helper function `get_targets`
    `representation` — str (optional)
        The default representation for this component (default: `'cartoon'`)

        Optional representations include `label`, `line`, `cartoon`,
        `backbone`, `ball-and-stick`, `carbohydrate`,
        `ellipsoid`, `gaussian-surface`, `gaussian-volume`,
        `molecular-surface`, `orientation`, `point`,
        `putty` and `spacefill`

    Returns
    -------
    `dict`
        Component information that can be passed to function `parse_molecule`

    Raises
    ------
    `RuntimeError`
        If specified an invalid representation, raises `RuntimeError`
    """
    r = representation.lower()
    if r not in ["label", "line", "cartoon",
                 "backbone", "ball-and-stick", "carbohydrate",
                 "ellipsoid", "gaussian-surface", "gaussian-volume",
                 "molecular-surface", "orientation", "point",
                 "putty", "spacefill"]: raise RuntimeError(f"Invalid representation type \"{representation}\"!")
    if type(targets) != list: targets = [targets]
    return {
        'label': label,
        'targets': targets,
        'representation': r
    }

def get_selection(targets, select=True, add=False):
    """
    Select specific targets in the molstar viewer.

    Parameters
    ----------
    `targets` — dict | List[dict]
        List of targets, whose value should be generated by helper function `get_targets`
    `select` — bool (optional)
        True for 'select' mode and False for 'hover' mode. (default: `True`)

        If set to True, the targets will be "selected" in the viewer.
        Otherwise they will be highlighted but not selected, as you hover on the structure.
    `add` — bool (optional)
        If set to False, the viewer will clear the selections in corresponding mode before adding new selections.
        Otherwise the new selections will be added to existed ones. (default: `False`)

    Returns
    -------
    `dict`
        Selection data for callbacks.
    """
    if select: mode = 'select'
    else: mode = 'hover'

    if add: modifier = 'add'
    else: modifier = 'set'
    if type(targets) != list: targets = [targets]
    return {
        'targets': targets,
        'mode': mode,
        'modifier': modifier
    }

def get_focus(targets, analyse=False):
    """
    Let the camera focus on the specified targets. If `analyse` were set to true, non-covalent interactions within 5 angstroms will be analyzed.

    Parameters
    ----------
    `targets` — dict | List[dict]
        List of targets, whose value should be generated by helper function `get_targets`
    `analyse` — bool (optional)
        Whether to analyse the non-covalent interactions of targets to its surroundings within 5 angstroms  (default: `False`)

    Returns
    -------
    `dict`
        Focus data for callbacks
    """
    if type(targets) != list: targets = [targets]
    return {
        'targets': targets,
        'analyse': analyse
    }
