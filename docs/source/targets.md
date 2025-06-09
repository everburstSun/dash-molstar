```{toctree}
:maxdepth: 2

   load
   helper
   properties
   callbacks
   targets
   representations
```

# Targets

The `Target` class provides a hierarchical representation and manipulation interface for molecular structures in *dash-molstar*. Together with its related classes (`Chain`, `Residue`, `Atom`, `Boundary`, `Box`, `Sphere`), it allows users to conveniently access and modify chains, residues, atoms, and perform geometric boundary calculations, suitable for molecular visualization, analysis, and structure editing.

Users can easily loop over all the structural elements within one target, and get the boundary of the target as well. The following table illustrates the members in the **Target** class:

| Member     | Type     | Description                                                                                        |
| :--------- | :------- | :------------------------------------------------------------------------------------------------- |
| `valid`    | `bool` | `True` if the Target object contains at least one chain, `False` otherwise.|
| `chains`   | `List[Chain]` | A list of `Chain` objects belonging to this target.|
| `residues` | `List[Residue]` | A flattened list of all valid `Residue` objects from all chains within this target.|
| `atoms`    | `List[Atom]` | A flattened list of all valid `Atom` objects from all residues in all chains within this target|
| `boundary` | `Optional[Boundary]` | A `Boundary` object representing the geometric boundary of all atoms in the target.|

## Quick Start Example

### Basic Usage

The fundamental usage is to parse the structural data returned by dash-molstar. In dash-molstar, `select` and `focus` properties are corresponding to the selected or focused molecular motif. 

The following example will print the selected targets every time the selections have been changed.

```py
import dash_molstar
from dash import Dash, html, Input
from dash_molstar.utils.target import Target
from dash_molstar.utils import molstar_helper

app = Dash(__name__)
app.layout = html.Div(
    dash_molstar.MolstarViewer(
        id='viewer', style={'width': '500px', 'height':'500px'}
    ),
)

@app.callback(Input('viewer', 'select'),
              prevent_initial_call=True)
def display_select(select):
    print("Current selection data:")
    target = Target(select)
    for chain in target.chains:
        print("Chain name:", chain.name, ",Auth name:", chain.auth_name)
        for residue in chain.residues:
            print("  Residue index:", residue.index, ",Residue number:", str(residue.number)+residue.ins_code, ",Name:", residue.name)
            for atom in residue.atoms:
                print("    Atom name:", atom.name, ",x:", atom.x, ",y:", atom.y, ",z:", atom.z)
    print("Number of chains:", len(target))
    print("Number of residues:", len(target.residues))
    print("Number of atoms:", len(target.atoms), end="\n\n")
```

:::{note}
For sending structural data to dash-molstar, the user should use the helper function `get_targets()` to generate *Target* instances. See the [](helper.md#targets) section.
:::

### Search & Modify

Except for looping over all the items, you can also search for specific elements, like chain, residue, or atom.

```py
# Already parsed select data
target = Target(select)

# Find a specific chain, residue, and atom on Target instance
# Returns an invalid instance if not found
chain = target.find_chain(name='A')
if chain.valid: print("Found chain", chain.name)

residue = target.find_residue(chain_name='A', residue_number=1)
if residue.valid: print('Found residue:', residue.name, residue.number)

atom = target.find_atom(chain_name='A', residue_number=1, atom_name='CA')
if atom.valid: print('Found atom:', atom.name)

# Add a new chain
target.add_chain('B')

# Remove chain B
target.remove_chain('B')
# Remove chain A
target.remove_chain(chain)
```

### Getting boundaries

With the `boundary` property, you can get the boundary of the returned target.

```py
# Already parsed select data
target = Target(select)

boundary = target.boundary
print("Boundary box min:", boundary.box.min)
print("Boundary box max:", boundary.box.max)
print("Boundary sphere center:", boundary.sphere.center)
print("Boundary sphere radius:", boundary.sphere.radius)
```

## Class Reference

### Target Class

The `Target` class is the main entry point for interacting with molecular structure data. It encapsulates a collection of chains, which in turn contain residues and atoms. It provides methods for initializing a structure from a dictionary, accessing its components, finding specific elements, modifying the structure, and exporting it back to a dictionary format.

```{eval-rst}
.. py:class:: Target(data: dict = {})

   Initializes a Target object.

   :param data: A dictionary representing the molecular structure. 
                It should be constructed from the data that were retrieved from the molstar viewer.
                If `data` is empty or malformed, an invalid Target object will be created.
   :type data: dict, optional
```

#### Properties

- **`valid`**
  - Type: `bool`
  - Description: Returns `True` if the Target object contains at least one chain, `False` otherwise. Indicates if the target is considered valid and has content.

- **`chains`**
  - Type: `List[Chain]`
  - Description: A list of `Chain` objects belonging to this target. Modifications to this list directly affect the Target's chains.

- **`residues`**
  - Type: `List[Residue]`
  - Description: A list of all valid `Residue` objects from all chains within this target. This is a flattened list.

- **`atoms`**
  - Type: `List[Atom]`
  - Description: A list of all valid `Atom` objects from all residues in all chains within this target. This is a flattened list.

- **`boundary`**
  - Type: `Optional[Boundary]`
  - Description: A `Boundary` object representing the geometric boundary (both a bounding box and a bounding sphere) of all atoms in the target. Calculated on first access. Returns `None` if the target is invalid or contains no atoms with coordinates.

#### Methods

```{eval-rst}
.. py:method:: Target.__len__()

   Returns the number of chains in the Target object.

   :rtype: int
```

```{eval-rst}
.. py:method:: Target.find_chain(name: str) -> Chain

   Finds and returns a `Chain` object by its name.

   :param name: The name of the chain to find.
   :type name: str
   :returns: The `Chain` object if found, otherwise an invalid `Chain` object (where `chain.valid` is `False`).
   :rtype: Chain
```

```{eval-rst}
.. py:method:: Target.find_residue(chain_name: str, residue_number: int, ins_code: str = "") -> Residue

   Finds and returns a `Residue` object within a specified chain by its number and optional insertion code.

   :param chain_name: The name of the chain to search within.
   :type chain_name: str
   :param residue_number: The number of the residue to find.
   :type residue_number: int
   :param ins_code: The insertion code of the residue (optional).
   :type ins_code: str, optional
   :returns: The `Residue` object if found, otherwise an invalid `Residue` object (where `residue.valid` is `False`).
   :rtype: Residue
```

```{eval-rst}
.. py:method:: Target.find_atom(chain_name: str, residue_number: int, atom_name: str, ins_code: str = "") -> Atom

   Finds and returns an `Atom` object within a specified residue of a specified chain.

   :param chain_name: The name of the chain.
   :type chain_name: str
   :param residue_number: The number of the residue.
   :type residue_number: int
   :param atom_name: The name of the atom.
   :type atom_name: str
   :param ins_code: The insertion code of the residue (optional).
   :type ins_code: str, optional
   :returns: The `Atom` object if found, otherwise an invalid `Atom` object (where `atom.valid` is `False`).
   :rtype: Atom
```

```{eval-rst}
.. py:method:: Target.add_chain(chain_name: str, residues: List = [], auth_name: str = '')

   Adds a new chain to the Target object.

   :param chain_name: The name for the new chain.
   :type chain_name: str
   :param residues: A list of residue data dictionaries to initialize the chain with (optional).
   :type residues: List, optional
   :param auth_name: The authentic name for the new chain (optional). If not provided, `chain_name` is used.
   :type auth_name: str, optional
```

```{eval-rst}
.. py:method:: Target.remove_chain(chain_name: Union[str, Chain]) -> bool

   Removes a chain from the Target object, either by its name or by providing the `Chain` object itself.

   :param chain_name: The name of the chain to remove or the `Chain` object to remove.
   :type chain_name: Union[str, Chain]
   :returns: `True` if the chain was successfully removed, `False` otherwise.
   :rtype: bool
```

```{eval-rst}
.. py:method:: Target.to_dict() -> dict

   Exports the current structure of the Target object (including all its chains, residues, and atoms) to a dictionary.

   :returns: A dictionary representation of the Target, suitable for serialization or further processing.
   :rtype: dict
```


### Chain Class

The `Chain` class represents a single chain within a molecular structure, containing a list of residues. It provides methods for accessing and modifying its name, residues, and atoms within those residues.

```{eval-rst}
.. py:class:: Chain(chain_name: str = None, residues: List[dict] = [], auth_name: str = '')

   Initializes a Chain object.

   :param chain_name: The name of the chain (e.g., 'A').
   :type chain_name: str, optional
   :param residues: A list of dictionaries, where each dictionary represents a residue and its atoms.
   :type residues: List[dict], optional
   :param auth_name: The authentic (author-assigned) name of the chain, if different from `chain_name`.
   :type auth_name: str, optional
```

#### Properties

- **`name`**
  - Type: `str`
  - Description: The primary identifier for the chain.
- **`auth_name`**
  - Type: `str`
  - Description: The authentic (author-assigned) name of the chain. Defaults to `name` if not specified.
- **`residues`**
  - Type: `List[Residue]`
  - Description: A list of `Residue` objects belonging to this chain.
- **`atoms`**
  - Type: `List[Atom]`
  - Description: A flattened list of all `Atom` objects from all residues within this chain.
- **`valid`**
  - Type: `bool`
  - Description: Returns `True` if the chain has a `name`, `False` otherwise.

#### Methods

```{eval-rst}
.. py:method:: Chain.__len__()

   Returns the number of residues in the chain.

   :rtype: int
```

```{eval-rst}
.. py:method:: Chain.find_residue(number: int, ins_code: str = "") -> Residue

   Finds and returns a `Residue` object by its number and optional insertion code.

   :param number: The number of the residue to find.
   :type number: int
   :param ins_code: The insertion code of the residue (optional).
   :type ins_code: str, optional
   :returns: The `Residue` object if found, otherwise an invalid `Residue` object.
   :rtype: Residue
```

```{eval-rst}
.. py:method:: Chain.find_atom(residue_number: int, atom_name: str, ins_code: str = "") -> Atom

   Finds and returns an `Atom` object within a specified residue of this chain.

   :param residue_number: The number of the residue.
   :type residue_number: int
   :param atom_name: The name of the atom.
   :type atom_name: str
   :param ins_code: The insertion code of the residue (optional).
   :type ins_code: str, optional
   :returns: The `Atom` object if found, otherwise an invalid `Atom` object.
   :rtype: Atom
```

```{eval-rst}
.. py:method:: Chain.add_residue(index: int, number: int = None, ins_code: str = '', name: str = '', atoms: List[dict] = [])

   Adds a new residue to the chain.

   :param index: The index for the new residue.
   :type index: int
   :param number: The number for the new residue. If None, defaults to `index`.
   :type number: int, optional
   :param ins_code: The insertion code for the new residue.
   :type ins_code: str, optional
   :param name: The name of the new residue (e.g., 'ALA').
   :type name: str, optional
   :param atoms: A list of atom data dictionaries to initialize the residue with.
   :type atoms: List[dict], optional
   :returns: The newly created `Residue` object.
   :rtype: Residue
```

```{eval-rst}
.. py:method:: Chain.remove_residue(number: Union[int, Residue], ins_code: str = '') -> bool

   Removes a residue from the chain, either by its number and insertion code or by providing the `Residue` object itself.

   :param number: The number of the residue to remove or the `Residue` object.
   :type number: Union[int, Residue]
   :param ins_code: The insertion code of the residue (if removing by number).
   :type ins_code: str, optional
   :returns: `True` if the residue was successfully removed, `False` otherwise.
   :rtype: bool
```

### Residue Class

The `Residue` class represents a single residue (e.g., an amino acid or nucleotide) within a chain, containing a list of atoms.

```{eval-rst}
.. py:class:: Residue(index: int = None, number: int = None, ins_code: str = '', name: str = '', atoms: List[dict] = [])

   Initializes a Residue object.

   :param index: The index of the residue within its chain.
   :type index: int, optional
   :param number: The residue number (sequence number). If None, defaults to `index`.
   :type number: int, optional
   :param ins_code: The insertion code for the residue (e.g., 'A').
   :type ins_code: str, optional
   :param name: The name of the residue (e.g., 'GLY', 'A').
   :type name: str, optional
   :param atoms: A list of dictionaries, where each dictionary represents an atom.
   :type atoms: List[dict], optional
```

#### Properties

- **`name`**
  - Type: `str`
  - Description: The name of the residue.
- **`index`**
  - Type: `int`
  - Description: The sequential index of the residue.
- **`number`**
  - Type: `int`
  - Description: The residue number as assigned in the structure file.
- **`ins_code`**
  - Type: `str`
  - Description: The insertion code, used to distinguish residues with the same number.
- **`atoms`**
  - Type: `List[Atom]`
  - Description: A list of `Atom` objects belonging to this residue.
- **`valid`**
  - Type: `bool`
  - Description: Returns `True` if the residue has an `index`, `False` otherwise.

#### Methods

```{eval-rst}
.. py:method:: Residue.__len__()

   Returns the number of atoms in the residue.

   :rtype: int
```

```{eval-rst}
.. py:method:: Residue.find_atom(name: str) -> Atom

   Finds and returns an `Atom` object by its name within this residue.

   :param name: The name of the atom to find (e.g., 'CA').
   :type name: str
   :returns: The `Atom` object if found, otherwise an invalid `Atom` object.
   :rtype: Atom
```

```{eval-rst}
.. py:method:: Residue.add_atom(index: int, name: str = None, x: float = None, y: float = None, z: float = None)

   Adds a new atom to the residue.

   :param index: The index for the new atom.
   :type index: int
   :param name: The name of the new atom (e.g., 'N', 'CA').
   :type name: str, optional
   :param x: The x-coordinate of the new atom.
   :type x: float, optional
   :param y: The y-coordinate of the new atom.
   :type y: float, optional
   :param z: The z-coordinate of the new atom.
   :type z: float, optional
   :returns: The newly created `Atom` object.
   :rtype: Atom
```

```{eval-rst}
.. py:method:: Residue.remove_atom(name: Union[str, Atom]) -> bool

   Removes an atom from the residue, either by its name or by providing the `Atom` object itself.

   :param name: The name of the atom to remove or the `Atom` object.
   :type name: Union[str, Atom]
   :returns: `True` if the atom was successfully removed, `False` otherwise.
   :rtype: bool
```

### Atom Class

The `Atom` class represents a single atom within a residue, storing its properties like name, index, and coordinates.

```{eval-rst}
.. py:class:: Atom(index: int = None, name: str = None, x: float = None, y: float = None, z: float = None)

   Initializes an Atom object.

   :param index: The index of the atom.
   :type index: int, optional
   :param name: The name of the atom (e.g., 'N', 'CA', 'C1').
   :type name: str, optional
   :param x: The x-coordinate of the atom.
   :type x: float, optional
   :param y: The y-coordinate of the atom.
   :type y: float, optional
   :param z: The z-coordinate of the atom.
   :type z: float, optional
```

#### Properties

- **`name`**
  - Type: `str`
  - Description: The name of the atom.
- **`index`**
  - Type: `int`
  - Description: The index of the atom.
- **`x`**
  - Type: `float`
  - Description: The x-coordinate of the atom.
- **`y`**
  - Type: `float`
  - Description: The y-coordinate of the atom.
- **`z`**
  - Type: `float`
  - Description: The z-coordinate of the atom.
- **`valid`**
  - Type: `bool`
  - Description: Returns `True` if the atom has an `index`, `False` otherwise.

### Boundary, Box, and Sphere Classes

These classes are used to define and calculate the geometric boundaries of a set of atoms. The `Target.boundary` property returns a `Boundary` object.

#### Boundary Class

The `Boundary` class calculates and holds the bounding box and bounding sphere for a given set of coordinates.

```{eval-rst}
.. py:class:: Boundary(coords: np.ndarray = None)

   Initializes a Boundary object.

   :param coords: A NumPy array of shape (N, 3) representing N atomic coordinates.
   :type coords: np.ndarray, optional
```

##### Properties

- **`box`**
  - Type: `Optional[Box]`
  - Description: A `Box` object representing the minimal bounding box enclosing all provided coordinates. `None` if no coordinates were provided.
- **`sphere`**
  - Type: `Optional[Sphere]`
  - Description: A `Sphere` object representing the minimal bounding sphere enclosing all provided coordinates. `None` if no coordinates were provided.

#### Box Class

The `Box` class defines an axis-aligned bounding box.

```{eval-rst}
.. py:class:: Box(min_coords: tuple[float, float, float] = None, max_coords: tuple[float, float, float] = None)

   Initializes a Box object.

   :param min_coords: A tuple `(min_x, min_y, min_z)` representing the minimum coordinates of the box.
   :type min_coords: tuple[float, float, float], optional
   :param max_coords: A tuple `(max_x, max_y, max_z)` representing the maximum coordinates of the box.
   :type max_coords: tuple[float, float, float], optional
```

##### Properties

- **`min`**
  - Type: `tuple[float, float, float]`
  - Description: The minimum (x, y, z) coordinates of the box.
- **`max`**
  - Type: `tuple[float, float, float]`
  - Description: The maximum (x, y, z) coordinates of the box.
- **`center`**
  - Type: `tuple[float, float, float]`
  - Description: The center (x, y, z) coordinates of the box.
- **`size`**
  - Type: `tuple[float, float, float]`
  - Description: The dimensions (width, height, depth) of the box.

##### Methods

```{eval-rst}
.. py:method:: Box.to_sphere() -> Sphere

   Calculates and returns a `Sphere` object that minimally encloses this box.

   :returns: The bounding sphere.
   :rtype: Sphere
```

#### Sphere Class

The `Sphere` class defines a sphere by its center and radius.

```{eval-rst}
.. py:class:: Sphere(center: tuple[float, float, float] = None, radius: float = None)

   Initializes a Sphere object.

   :param center: A tuple `(x, y, z)` representing the center of the sphere.
   :type center: tuple[float, float, float], optional
   :param radius: The radius of the sphere.
   :type radius: float, optional
```

##### Properties

- **`center`**
  - Type: `tuple[float, float, float]`
  - Description: The center (x, y, z) coordinates of the sphere.
- **`radius`**
  - Type: `float`
  - Description: The radius of the sphere.

##### Methods

```{eval-rst}
.. py:method:: Sphere.to_box() -> Box

   Calculates and returns an axis-aligned `Box` object that minimally encloses this sphere.

   :returns: The bounding box.
   :rtype: Box
```
