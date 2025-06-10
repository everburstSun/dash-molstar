from io import IOBase
import os
from urllib.parse import urlparse
import base64
from .representations import Representation
from .target import Target


supported_formats = {
    'mol': ["cif", "cifcore", "pdb", "pdbqt", "gro", "xyz", "mol", "sdf", "mol2", "lammps_data", "lammps_traj_data"],
    'snapshot': ["json", "molj", "molx", "zip"],
    'coords': ["dcd", "xtc", "trr", "nctraj", "lammpstrj"],
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
        Supported formats include `cif`, `cifcore`, `pdb`, `pdbqt`, `gro`, `xyz`, `mol`, `sdf`, `mol2`, `lammps_data`, `lammps_traj_data` (default: `None`)
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
    # processing preset
    if 'target' in preset.keys():
        if not isinstance(preset['target'], list): preset['target'] = [preset['target']]
        preset['target'] = [t.to_dict() if isinstance(t, Target) else t for t in preset['target']]
    if 'focus' in preset.keys():
        if not isinstance(preset['focus'], list): preset['focus'] = [preset['focus']]
        preset['focus'] = [t.to_dict() if isinstance(t, Target) else t for t in preset['focus']]
    if 'targets' in preset.keys():
        if not isinstance(preset['targets'], list): preset['targets'] = [preset['targets']]
        preset['targets'] = [t.to_dict() if isinstance(t, Target) else t for t in preset['targets']]
    if 'glycosylation' in preset.keys():
        if not isinstance(preset['glycosylation'], list): preset['glycosylation'] = [preset['glycosylation']]
        preset['glycosylation'] = [t.to_dict() if isinstance(t, Target) else t for t in preset['glycosylation']]
    if 'colors' in preset.keys():
        if not isinstance(preset['colors'], list): preset['colors'] = [preset['colors']]
        for color in preset['colors']:
            if not isinstance(color['targets'], list): color['targets'] = [color['targets']]
            color['targets'] = [t.to_dict() if isinstance(t, Target) else t for t in color['targets']]
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

        Supported formats for structures include `cif`, `cifcore`, `pdb`, `pdbqt`, `gro`, `xyz`, `mol`, `sdf`, `mol2`, `lammps_data`, `lammps_traj_data`

        Supported formats for states and sessions include `json`, `molj`, `molx`, `zip`

        Supported formats for coordinates include `dcd`, `xtc`, `trr`, `nctraj`, `lammpstrj`
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
    # processing preset
    if 'target' in preset.keys():
        if not isinstance(preset['target'], list): preset['target'] = [preset['target']]
        preset['target'] = [t.to_dict() if isinstance(t, Target) else t for t in preset['target']]
    if 'focus' in preset.keys():
        if not isinstance(preset['focus'], list): preset['focus'] = [preset['focus']]
        preset['focus'] = [t.to_dict() if isinstance(t, Target) else t for t in preset['focus']]
    if 'targets' in preset.keys():
        if not isinstance(preset['targets'], list): preset['targets'] = [preset['targets']]
        preset['targets'] = [t.to_dict() if isinstance(t, Target) else t for t in preset['targets']]
    if 'glycosylation' in preset.keys():
        if not isinstance(preset['glycosylation'], list): preset['glycosylation'] = [preset['glycosylation']]
        preset['glycosylation'] = [t.to_dict() if isinstance(t, Target) else t for t in preset['glycosylation']]
    if 'colors' in preset.keys():
        if not isinstance(preset['colors'], list): preset['colors'] = [preset['colors']]
        for color in preset['colors']:
            if not isinstance(color['targets'], list): color['targets'] = [color['targets']]
            color['targets'] = [t.to_dict() if isinstance(t, Target) else t for t in color['targets']]
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
        Supported formats include `dcd`, `xtc`, `trr`, `nctraj`, `lammpstrj` (default: `None`)

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

def get_box(min_xyz=(0,0,0), max_xyz=(1,1,1), radius=0.1, label="Bounding Box", color='red', opacity=1.0):
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
        Transparency of the box. The value is ranging from 0 to 1.0. (default: `1.0`)

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

def get_sphere(center=(0,0,0), radius=1.0, label="Sphere", color='blue', opacity=1.0, detail=6):
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
        Transparency of the box. The value is ranging from 0 to 1.0. (default: `1.0`)
    `detail` — int (optional)
        Controls the subdivision surface of the sphere. The sphere is make of polygons. The higher
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

def get_targets(chain, residue=None, atom=None, auth=False):
    """
    Select residues from a given chain. If no residue was specified, the entire chain will be selected.

    Parameters
    ----------
    `chain` — str
        Name of the target chain
    `residue` — int | List[int] (optional)
        Residue index of the target residues, corresponding to the structure file. (default: `None`)
    `atom` — int | List[int] (optional)
        Index of the target atom(s), corresponding to the structure file but started from 0. (default: `None`)
    `auth` — bool (optional)
        If a cif file was loaded, set `auth` to `True` to select the authentic chain names and residue numbers (default: `False`)

    Returns
    -------
    `Target`
        Selected chains, residues or atoms.
    """
    target = Target()
    target.auth = auth
    target.add_chain(chain)
    if residue is not None:
        if type(residue) != list: residue = [residue]
        for res in residue:
            if type(res) == int: target.chains[-1].add_residue(res)
            elif type(res) == str:
                try:
                    num = eval(res)
                    target.chains[-1].add_residue(num)
                except:
                    num = eval(res[:-1])
                    ins = res[-1]
                    target.chains[-1].add_residue(num, ins_code=ins)
            if atom is not None:
                if type(atom) != list: atom = [atom]
                for a in atom:
                    target.chains[-1].residues[-1].add_atom(a)
    return target

def create_component(label, targets, representation=Representation()):
    """
    Generate the component information for selected targets.

    Parameters
    ----------
    `label` — str
        Name of the component
    `targets` — Target | List[Target]
        List of targets, whose value should be generated by helper function `get_targets`
    `representation` — Representation | List[Representation] (optional)
        The representation(s) for this component (default: cartoon)

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
        'targets': [t.to_dict() if isinstance(t, Target) else t for t in targets],
        'representation': [r.to_dict() if isinstance(r, Representation) else r for r in representation]
    }

def get_selection(targets, select=True, add=False):
    """
    Select specific targets in the molstar viewer. The returned value can be passed to either `selection` or 
    `hover` parameters.

    Parameters
    ----------
    `targets` — Target | List[Target]
        List of targets, whose value should be generated by helper function `get_targets`

    `select`
        DEPRECATED

    `add` — bool (optional)
        If set to False, the viewer will clear the selections in corresponding mode before adding new selections.
        Otherwise the new selections will be added to existed ones. (default: `False`)

    Returns
    -------
    `dict`
        Selection data for callbacks.
    """
    if add: modifier = 'add'
    else: modifier = 'set'
    if type(targets) != list: targets = [targets]
    return {
        'targets': [t.to_dict() if isinstance(t, Target) else t for t in targets],
        'modifier': modifier
    }

def get_focus(targets, analyse=False):
    """
    Let the camera focus on the specified targets. 
    If `analyse` were set to true, non-covalent interactions within 5 angstroms will be analyzed.

    Parameters
    ----------
    `targets` — Target | List[Target]
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
        'targets': [t.to_dict() if isinstance(t, Target) else t for t in targets],
        'analyse': analyse
    }

def get_measurement(targets, type='label', options=None, add=False):
    """
    Create a measurement for the specified targets. There are 6 types of measurements supported by molstar, 
    specify them in the `type` parameter.

    Parameters
    ----------
    `targets` — Target | List[Target]
        The targets to be measured. The number of targets must meet the requirements of the specified measurement type. 
        The targets should be generated by helper function `get_targets`.
    `type` — str (optional)
        The 6 supported measurements are: label, orientation, plane, distance, angle, and dihedral. 
        For label, orientation, and plane, at least one target should be provided. For distances, angles, and dihedrals,
         2, 3, and 4 targets are needed respectively. (default: `'label'`)
    `add` — bool (optional)
        If set to False, existing measurements will be cleared before adding new ones.
        Otherwise the new measurements will be added to molecule. (default: `False`)

    Returns
    -------
    `dict`
        The measurement data for callbacks.

    Raises
    ------
    `ValueError`
        If the specified measurement type is not supported or the number of targets does not meet the requirements.
    `TypeError`
        If the targets are not valid `Target` objects, raises `TypeError`.
    """
    if not isinstance(targets, list): targets = [targets]
    minimum_required = {
        'label': 1,
        'orientation': 1,
        'plane': 1,
        'distance': 2,
        'angle': 3,
        'dihedral': 4
    }
    if type not in minimum_required.keys():
        raise ValueError(f"Invalid measurement type \"{type}\". Supported types are {minimum_required.keys()}.")
    if len(targets) < minimum_required[type]:
        raise ValueError(f"At least {minimum_required[type]} required by the measurement \"{type}\", only {len(targets)} provided.")

    for t in range(minimum_required[type]):
        if not isinstance(targets[t], Target) or not targets[t].valid:
            raise TypeError(f"Target {t} is not a valid Target object. Use helper function `get_targets` to generate targets.")
    return {
        'targets': [t.to_dict() if isinstance(t, Target) else t for t in targets],
        'type': type,
        'mode': 'add' if add else 'set',
    }