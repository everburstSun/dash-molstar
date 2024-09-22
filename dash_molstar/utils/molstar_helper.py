from io import IOBase
import os
from urllib.parse import urlparse
import base64
from .representations import Representation


supported_formats = {
    'mol': ["cif", "cifcore", "pdb", "pdbqt", "gro", "xyz", "mol", "sdf", "mol2"],
    'snapshot': ["json", "molj", "molx", "zip"],
    'coords': ["dcd", "xtc", "trr", "nctraj"]
}

def parse_molecule(inp, fmt=None, component=None, preset={'kind': 'standard'}):
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
    `preset` — dict (optional)
        The preset for molstar of how to display the loaded structure file.

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
    if not fmt: raise RuntimeError("The format must be specified if you didn't provide a file name.")
    fmt = fmt.strip('.').lower()
    if fmt not in supported_formats['mol']:
        raise RuntimeError(f"The input molecule file format \"{fmt}\" is not supported by molstar.")
    if fmt == 'cif': fmt = 'mmcif'
    if fmt == 'cifcore': fmt = 'cifCore'
    d = {
        "type": 'mol',
        "data": data,
        "format": fmt,
        "preset": preset
    }
    if component: d['component'] = component
    return d

def parse_url(url, fmt=None, component=None, mol=True, preset={'kind': 'standard'}):
    """
    Parse the URL for `data` parameter of molstar viewer. 
    The url can be either a structure or a molstar state/session file. If a state/session
    was provided, the `mol` parameter should be set to `False`.

    Parameters
    ----------
    `url` — str
        The URL to the content to be passed to molstar.
    `fmt` — str (optional)
        Format of the input content. (default: `None`)

        Supported formats for structures include `cif`, `cifcore`, `pdb`, `pdbqt`, `gro`, `xyz`, `mol`, `sdf`, `mol2` 

        Supported formats for states and sessions include `json`, `molj`, `molx`, `zip`

        Supported formats for coordinates include `dcd`, `xtc`, `trr`, `nctraj`
    `component` — dict | List[dict] (optional)
        Component to be created in molstar. 
        If not specified, molstar will use its default settings. (default: `None`)

        Use helper function `create_component` to generate correct data for this parameter.
    `mol` — DEPRECATED
    `preset` — dict (optional)
        The preset for molstar of how to display the loaded structure file.

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
    # check whether the format is in supported list and specify the url type
    fmt = fmt.strip('.').lower()
    for type, formats in supported_formats.items():
        if fmt in formats:
            urlfor = type
            break
    else:
        raise RuntimeError(f"The input file format \"{fmt}\" is not supported by molstar.")
    if fmt == 'cif': fmt = 'mmcif'
    if fmt == 'cifcore': fmt = 'cifCore'
    d = {
        "type": 'url',
        "urlfor": urlfor,
        "data": url,
        "format": fmt,
        "preset": preset
    }
    if component: d['component'] = component
    return d

def parse_coordinate(inp, fmt=None):
    """
    Parse the coordinate file for loading a structure. This method encode the binary coordinate file
    into string with base64, so it is not recommended if you are about load a trajectory that is larger
    than 10 MB. For loading biger trajectories, try passing a url to molstar.

    Parameters
    ----------
    `inp` — str | file-like object
        The file path to molecule or the file content of molecule.

        If `inp` was set to file path, the format can be automatically determined.
        Otherwise the format has to be specified manually.
    `fmt` — str (optional)
        Format of the input molecule. 
        Supported formats include `dcd`, `xtc`, `trr`, `nctraj` (default: `None`)

    Returns
    -------
    `dict`
        The value for the `coordinate` parameter of helper function `get_trajectory()`.

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
        with open(inp, 'rb') as f:
            data = f.read()
    else:
        # provided a file-like object as input
        if isinstance(inp, IOBase):
            data = inp.read()
        # provided file content as input
        else:
            data = inp
    assert type(data) == bytes
    if not fmt: raise RuntimeError("The format must be specified if you didn't provide a file name.")
    fmt = fmt.strip('.').lower()
    if fmt not in supported_formats['coords']:
        raise RuntimeError(f"The input coordinate file format \"{fmt}\" is not supported by molstar.")
    return {
        'type': 'coord',
        "format": fmt,
        "data": base64.b64encode(data).decode('utf-8')
    }

def get_trajectory(topology, coordinate):
    """
    Load a trajectory into molstar viewer.

    Parameters
    ----------
    `topology` — dict
        The topology of molecule. Generated with helper function `parse_molecule()` or `parse_url()`
    `coordinate` — dict
        The coordinates of the trajectory. Generated with helper function `parse_coordinate()` or `parse_url()`

    Returns
    -------
    `dict`
        The value for the `data` parameter.
    """
    return {
        'type': 'traj',
        'topo': topology,
        'coords': coordinate
    }

def get_box(min_xyz=(0,0,0), max_xyz=(1,1,1), radius=0.1, label="Bounding Box", color='red', opacity=1):
    """
    Generate a bounding box in the viewer with given parameters.

    Parameters
    ----------
    `min_xyz` — tuple (optional)
        Minimum of x, y and z values (default: `(0,0,0)`)
    `max_xyz` — tuple (optional)
        Maximum of x, y and z values (default: `(1,1,1)`)
    `radius` — float (optional)
        Edge radius in angstrom (default: `0.1`)
    `label` — str (optional)
        The box label to be shown in the viewer (default: `"Bounding Box"`)
    `color` — str (optional)
        X11 color names (default: `'red'`)
        Avaliable options can be found at [here](https://www.w3.org/TR/css-color-3/#svg-color)
    `opacity` — float (optional)
        Transparency of the box. The value is ranging from 0 to 1. (default: `1`)

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
        'color': color,
        'alpha': opacity
    }

def get_sphere(center=(0,0,0), radius=1, label="Sphere", color='blue', opacity=1, detail=6):
    """
    Generate a sphere in the viewer with given parameters.

    Parameters
    ----------
    `center` — tuple (optional)
        Center of the sphere (default: `(0,0,0)`)
    `radius` — float (optional)
        Sphere radius in angstrom (default: `0.1`)
    `label` — str (optional)
        The sphere label to be shown in the viewer (default: `"Sphere"`)
    `color` — str (optional)
        X11 color names (default: `'blue'`)
        Avaliable options can be found at [here](https://www.w3.org/TR/css-color-3/#svg-color)
    `opacity` — int (optional)
        Transparency of the box. The value is ranging from 0 to 1. (default: `1`)
    `detail` — int (optional)
        Controls the roundness of the sphere. The sphere is make of polygons. The higher
        the value, the more it looks like a fine sphere. But also requires longer time to
        render. The recommended value is 6.

    Returns
    -------
    `dict`
        Dict for the `data` parameter of MolstarViewer

    Raises
    ------
    `ValueError`
        Raised if input coordinates are not 3-dimensional
    """
    if len(center) != 3: raise ValueError("Coordinates must be 3-dimensional!")
    return {
        'type': 'shape',
        'shape': 'sphere',
        'center': center,
        'radius': radius,
        'label': label,
        'color': color,
        'alpha': opacity,
        'detail': detail
    }

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
    if residue is not None:
        if type(residue) != list: residue = [residue]
        residues = []
        for res in residue:
            if type(res) == int: residues.append(res)
            elif type(res) == str:
                try:
                    num = eval(res)
                    residues.append(num)
                except:
                    pass
        target['residue_numbers'] = residues
    return target

def create_component(label, targets, representation=Representation()):
    """
    Generate the component information for selected targets.

    Parameters
    ----------
    `label` — str
        Name of the component
    `targets` — dict | List[dict]
        List of targets, whose value should be generated by helper function `get_targets`
    `representation` — Representation | List[Representation] (optional)
        The representation(s) for this component (default: `cartoon`)

    Returns
    -------
    `dict`
        Component information that can be passed to function `parse_molecule`

    Raises
    ------
    `RuntimeError`
        If specified an invalid representation, raises `RuntimeError`
    """
    if type(targets) != list: targets = [targets]
    if type(representation) != list: representation = [representation]
    return {
        'label': label,
        'targets': targets,
        'representation': [r.to_dict() if type(r)!=dict else r for r in representation]
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
