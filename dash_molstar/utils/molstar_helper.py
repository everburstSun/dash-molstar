from io import StringIO
import os


def parse_molecule(inp, fmt=None):
    # provided a filename as input
    if os.path.isfile(inp):
        # if format if not specified, deduce it from filename
        if not fmt:
            name, fmt = os.path.splitext(inp)
        with open(inp, 'r') as f:
            data = f.read()
    else:
        # provided a file-like object as input
        if isinstance(inp, StringIO):
            data = inp.getvalue()
        else:
            data = inp
        # provided file content as input
    fmt = fmt.strip('.').lower()
    if fmt not in ["cif", "cifcore", "pdb", "pdbqt", "gro", "xyz", "mol", "sdf", "mol2"]:
        RuntimeError("The input file format is not supported by molstar.")
    if fmt == 'cif': fmt = 'mmcif'
    if fmt == 'cifcore': fmt = 'cifCore'
    return {
        "type": 'mol',
        "data": data,
        "format": fmt
    }

def get_cube():
    pass

def get_sphere(center, radius):
    pass

def get_component():
    pass

def get_selection():
    pass

def get_focus():
    pass
