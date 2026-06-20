```{toctree}
:maxdepth: 2

   load
   helper
   shapes
   properties
   callbacks
   targets
   representations
   camera
```

# Helper Functions
Data provided to molstar viewer should be prepared by helper functions.

## Loading molecules

```{eval-rst}
.. py:function:: parse_molecule(inp, fmt=None, component=None, preset={'kind': 'standard'}, matrix=None)
   
   Parse the molecule for the `data` property of the dash-molstar.

   :param inp: The file path to the molecule or the file content of the molecule.
               It can be either a string (file path) or a file-like object.
               If ``inp`` is set to a file path, the format can be automatically determined. 
               Otherwise, the format has to be specified manually.
   :type inp: str | file-like object

   :param fmt: The format of the input molecule. Supported formats include 
               `cif`, `cifcore`, `pdb`, `pdbqt`, `gro`, `xyz`, `mol`, `sdf`, `mol2`, `lammps_data`, `lammps_traj_data`.
               (default: ``None``)
   :type fmt: str, optional

   :param component: Component to be created in molstar. If not specified, molstar
                     will use its default settings. Use the helper function ``create_component()``
                     to generate the correct data for this parameter. (default: ``None``)
   :type component: dict | List[dict], optional

   :param preset: The preset for molstar on how to display the loaded structure file.
                  (default: ``{'kind': 'standard'}``)
   :type preset: dict, optional

   :param matrix: The homogeneous transformation matrix for the molecule. 
                  Only rigid transformations are allowed.
                  (default: ``None``)
   :type matrix: np.ndarray, optional

   :returns: The value for the ``data`` property.
   :rtype: dict

   :raises RuntimeError: If the input format is not supported by molstar viewer.
```

This function takes in the path to a file or the contents of a file-like object as input, along with the format of the molecule (if not automatically determined from the file path) and an optional dictionary or list of dictionaries containing information about the components of the molecule to be created in molstar.

```py
import dash_molstar
from dash import Dash, html
from dash_molstar.helpers import parse_molecule

app = Dash(__name__)
app.layout = html.Div(
   dash_molstar.MolstarViewer(
      id='viewer', style={'width': '500px', 'height':'500px'},
      data=parse_molecule('3u7y.pdb')
   )
)
```

Each time the `data` property was updated with molecules, the canvas will be cleaned before loading any new structures.

```{eval-rst}
.. function:: parse_url(url, fmt=None, component=None, mol=True, preset={'kind': 'standard'}, matrix=None)

   Parse the URL for the `data` property of the molstar viewer. 
   The URL can be either a structure or a molstar state/session file. If a state/session is provided, the `mol` parameter should be set to `False`.

   :param url: The URL to the content to be passed to molstar.
   :type url: str

   :param fmt: The format of the input content. Supported formats for structures include 
               `cif`, `cifcore`, `pdb`, `pdbqt`, `gro`, `xyz`, `mol`, `sdf`, `mol2`, `lammps_data`, `lammps_traj_data`.
               Supported formats for states and sessions include `json`, `molj`, `molx`, `zip`.
               Supported formats for coordinates include `dcd`, `xtc`, `trr`, `nctraj`, "lammpstrj".
               (default: ``None``)
   :type fmt: str, optional

   :param component: Component to be created in molstar. If not specified, molstar will
                     use its default settings. Use the helper function ``create_component()`` to generate the correct data for this parameter. (default: ``None``)
   :type component: dict | List[dict], optional

   :param mol: **DEPRECATED**

   :param preset: The preset for molstar on how to display the loaded structure file.
                  (default: ``{'kind': 'standard'}``)
   :type preset: dict, optional

   :param matrix: The homogeneous transformation matrix for the molecule. 
                  Only rigid transformations are allowed.
                  (default: ``None``)
   :type matrix: np.ndarray, optional

   :returns: The value for the ``data`` property.
   :rtype: dict

``` 

```py
import dash_molstar
from dash import Dash, html
from dash_molstar.helpers import parse_url

app = Dash(__name__)
app.layout = html.Div(
   dash_molstar.MolstarViewer(
      id='viewer', style={'width': '500px', 'height':'500px'},
      data=parse_url('https://files.rcsb.org/download/3U7Y.pdb')
   )
)
```

If you would like molstar itself send requests to fetch files, i.e. access your custom APIs, pass url to this function and the return value is for `data` property. If a static file was provided, this function will automatically infer the file format from the url. Otherwise you should specify the format on your own. Currently, only text files are supported. Do not use a gzip archive.

You can also load a molstar state or session file with this function. The input `component` will be ignored. 

```py
import dash_molstar
from dash import Dash, html
from dash_molstar.helpers import parse_url

app = Dash(__name__)
app.layout = html.Div(
   dash_molstar.MolstarViewer(
      id='viewer', style={'width': '500px', 'height':'500px'},
      data=parse_url('https://molstar.org/demos/states/villin-md.molx')
   )
)
```

### preset

The preset argument can help you control the initial behaviour of molstar when it loads a structure. The default value of preset is `{'kind': 'standard'}`. `kind` is also the only mandatory key in this dict. 

Available options for `kind` are: `standard` | `empty` | `alignment` | `validation` | `symmetry` | `feature` | `density` | `membrane` | `feature-density` | `motif` | `nakb` | `glygen`

Other than `kind`, there are three other general keys but optional:

- `assemblyId` (str): The assembly mode to show in the crystal
- `modelIndex` (int): The first frame to show when you load a trajectory
- `plddt` (str): plddt control option, can be `'off'` | `'single-chain'` | `'on'`

An example for `assemblyId`: the main protease of SARS-COVID-2 (PDB ID 6LU7) was resolved as a homodimer, but if you load the protein with the default parameter, only the monomer will be displayed. To show the homodimer, you have to pass the `assemblyId` as well:

```py
data = parse_url(url='https://files.rcsb.org/download/6LU7.pdb', 
                 preset={
                    'kind': 'standard',
                    'assemblyId': '1'
                 })
```

Each type of `kind` may have some additional options relate to it:

#### standard
The default behaviour. There is no additional option for this kind beyond the general ones.

It applies an `'auto'` representation to the structure. If the structure has pLDDT information and is a single chain (or pLDDT is forced 'on'), it will use a pLDDT confidence coloring theme.

#### empty
Disable any display. There is no additional option for this kind beyond the general ones.

When you load a protein into the viewer, it will create a cartoon representation for everything. Sometimes you may want to have sophisticated control for the representation, and the default one should thus be disabled. You can pass `{'kind': 'empty'}` to the preset argument.

#### alignment
This preset is used for superposing multiple structures or parts of structures. It creates a single structure component from transformed substructures using FlexibleStructureFromModel. It applies custom coloring based on the provided colors and targets in the parameters.
- `targets` (List[Target]): Optional. A list of targets to be included in the alignment. Each target can optionally have a transformation matrix.
- `colors` (List[{value: number, targets: List[Target]}]): A list defining how different parts of the aligned structures should be colored. Each entry specifies a color value and the targets that should receive this color.

#### validation
This preset applies the `ValidationReportGeometryQualityPreset`, which is typically used to visualize geometry validation reports (e.g., clashes, bond lengths, angles).
- `colorTheme` (str): Optional. Specifies a color theme to use for the validation report.
- `showClashes` (bool): Optional. If true, explicitly shows clashes.

#### symmetry
This preset is used to display assembly symmetries. In symmetry mode, `assemblyId` also has to be specified.
- `symmetryIndex` (int): Optional. Specifies the index of the symmetry to be displayed.

#### feature
This preset focuses on a specific target within the structure. If the target is not found in the current assembly, it attempts to switch to the model coordinates and re-locate the target.
- `target` (Target): The specific molecular target to focus on.

#### density
This preset initializes volume streaming for electron density maps. It shows a toast message instructing the user on how to interact with the density (click on residue).

There is no additional option for this kind beyond the general ones.

#### feature-density
This combines the functionality of feature and density. It focuses on a specific target feature. It initializes volume streaming around that feature, allowing customization of the radius, hidden channels, and wireframe display for the density.
- `target` (Target): The specific molecular target to focus on and around which density will be shown.
- `radius` (float): Optional. The radius (e.g., in Angstroms) around the target for which to display density. Defaults to 5 if not specified.
- `hiddenChannels` (List[str]): Optional. A list of density map channel names (e.g., '2fo-fc', 'fo-fc(+ve)') that should be initially hidden.
- `wireframe` (bool): Optional. If true, displays the density map as a wireframe. Defaults to true if not specified.

#### membrane
This preset applies the MembraneOrientationPreset to visualize membrane planes. It resets the camera after applying the preset. If membrane calculation fails (e.g., for very small structures), it logs an error and falls back to the `'auto'` representation.

There is no additional option for this kind beyond the general ones.

#### motif
This preset is designed to highlight structural motifs. It attempts to determine the correct assembly ID if not provided.
It uses RcsbSuperpositionRepresentationPreset with selection expressions to highlight the motif, potentially with a specific color and transparency for the rest of the structure.
- `label` (str): Optional. The prefix for component names.
- `targets` (List[Target]): A list of targets that define the motif.
- `color` (number): Optional. A hex value of color to apply to the motif.

#### nakb
This preset applies an `'auto'` representation but specifically uses a `'nakb'` (Nucleic Acid Knowledge Base) coloring theme.

There is no additional option for this kind beyond the general ones. 

#### glygen
This preset is for visualizing glycosylation features.
- `label` (str): Optional. A label for the GlyGen visualization.
- `focus` (Target): The chain to highlight. The target will only be processed at the chain level. **Note**: this `focus` key is not used to focus the camera on the target, but to focus your attention on a chain.
- `glycosylation` (List[Target]): Glycosylations to be highlighted. The targets will only be processed at the chain level.

## Loading trajectories

Dash-molstar allows users to load trajectories into molstar viewer. Simple trajectories (i.e. multi-frame NMR structures) can be loaded with a multi-frame PDB file. The trajectories for molecular dynamic similation can also be loaded. 

A MD trajectory normally has two parts -- the topology and the coordinates. The topology can be parsed with helper function `parse_molecule()` for local files, and the coordinates can be parsed with helper function `parse_coordinate()`. For remote resources, both the topology and the coordinates can be parsed by helper function `parse_url()`.

```{eval-rst}
.. function:: get_trajectory(topology, coordinate)

   Load a trajectory into the molstar viewer.

   :param topology: The topology of the molecule. This is generated using the helper function 
                    ``parse_molecule()`` or ``parse_url()``.
   :type topology: dict

   :param coordinate: The coordinates of the trajectory. This is generated using the helper function 
                      ``parse_coordinate()`` or ``parse_url()``.
   :type coordinate: dict

   :returns: The value for the ``data`` property.
   :rtype: dict

```

To load a trajectory, use the function `get_trajectory()` and supply the return value to `data` property.

```python
import dash_molstar
from dash import Dash, html
from dash_molstar.helpers import parse_molecule, parse_coordinate, get_trajectory

topo = parse_molecule('topo.pdb')
coords = parse_coordinate('coords.xtc')

app = Dash(__name__)
app.layout = html.Div(
   dash_molstar.MolstarViewer(
      id='viewer', style={'width': '500px', 'height':'500px'},
      data=get_trajectory(topo, coords)
   )
)
```

```{eval-rst}
.. function:: parse_coordinate(inp, fmt=None)

   Parse the coordinate file for loading a structure. This method encodes the binary coordinate file into a string with base64, so it is not recommended to load trajectories larger than 10 MB. For larger trajectories, consider passing a URL to molstar.

   :param inp: The file path to the molecule or the file content of the molecule.
               It can be either a string (file path) or a file-like object.
               If ``inp`` is set to a file path, the format can be automatically determined. 
               Otherwise, the format has to be specified manually.
   :type inp: str | file-like object

   :param fmt: The format of the input molecule. Supported formats include 
               `dcd`, `xtc`, `trr`, `nctraj`, `lammpstrj`. (default: ``None``)
   :type fmt: str, optional

   :returns: The value for the ``coordinate`` argument of the helper function ``get_trajectory()``.
   :rtype: dict

   :raises RuntimeError: If the input format is not supported by molstar viewer.

``` 

## Targets

```{eval-rst}
.. function:: get_targets(chain, residue=None, atom=None, auth=False)

   Select residues from a given chain. If no residue is specified, the entire chain will be selected.

   :param chain: The name of the target chain.
   :type chain: str

   :param residue: Residue index or a list of residue indices of the target. Index corresponds to the structure file.
                   (default: ``None``)
   :type residue: int | List[int], optional

   :param atom: Index of the target atom(s), corresponding to the structure file but started from 0. (default: `None`)
   :type atom: int | List[int] optional

   :param auth: If a CIF file is loaded, set this to ``True`` to select the authentic chain names and residue numbers. 
                (default: ``False``)
   :type auth: bool, optional

   :returns: A dictionary representing the selected residues.
   :rtype: Target

```

To specify a molecular target that you want to interact with, you should always use the `get_targets()` helper function.

This function returns a **Target** instance containing information about the residues to be selected from the specified chain in molstar. If no residue is specified, the entire chain will be selected. Similarly, if no atom is specified, the entire residue will be selected.

:::{seealso}
For a detailed introduction of the **Target** class, see the [](targets.md) section.
:::

```py
from dash_molstar.helpers import get_targets

# select all residues on chain H
ChainL = get_targets(chain="H")

# select some residues on chain L
segment = get_targets(chain="L", residue=[24,25,26,27])

# select residues 1-25 on chain L
segment2 = get_targets(chain="L", residue=list(range(1, 26)))

# select atom index 192
# you have to figure out which residue and chain it belongs to
atom = get_targets(chain="A", residue=25, atom=192)
```

When working with PDBx/mmCIF file formats, there will be two sets of naming and numbering system. One is a human-readable label or identifier for a chain names for residue numbers. The other is an authentic identifier that aligns with the experimental data and reflects the true identity of the chains and residues as determined through rigorous scientific procedures. Switching between the two systems by specifing `auth=True`.

## Components

```{eval-rst}
.. function:: create_component(label, targets, representation=Representation())

   Generate the component information for the selected targets.

   :param label: The name of the component.
   :type label: str

   :param targets: A dictionary or list of dictionaries representing the targets. The values should be generated 
                   by the helper function ``get_targets()``.
   :type targets: Target | List[Target]

   :param representation: The representation(s) for this component. 
                          The default representation is cartoon.
   :type representation: Representation | List[Representation], optional

   :returns: A dictionary containing the component information that can be passed to the ``parse_molecule`` function.
   :rtype: dict

   :raises RuntimeError: If an invalid representation is specified.

``` 

This function generates the component information for the specified targets in molstar. The function takes in the name of the component, a dictionary or list of dictionaries containing the targets (whose value should be generated using the `get_targets()` function), and an optional class instance specifying the default representation for the component (defaulting to **cartoon**).

```py
from dash_molstar.utils import Representation
from dash_molstar.helpers import (
   get_targets, 
   create_component, 
   parse_molecule
)

# first you need a target
ChainL = get_targets(chain="H")

# it is also fine if you have more than one target
segment = get_targets(chain="L", residue=[24,25,26,27])

# create a component to include target ChainL
componentL = create_component("Chain L", ChainL)

# create an other component with more targets and another representation
surface = create_component("Surface", [ChainL, segment], Representation('molecular-surface'))

# pass the components to function parse_molecule()
data = parse_molecule('3u7y.pdb', component=[componentL, surface])
```

If an invalid representation is specified, a RuntimeError is raised.

:::{seealso}
See how to control the representation of components, in the [](representations.md) section.
:::

## Highlighting targets

```{eval-rst}
.. function:: get_selection(targets, select=True, add=False)

   Select specific targets in the molstar viewer.

   :param targets: A dictionary or list of dictionaries representing the targets. The values should be generated 
                   by the helper function `get_targets`.
   :type targets: Target | List[Target]

   :param select: **DEPRECATED**

   :param add: If ``False``, the viewer will clear existing selections before adding the new ones. 
               If ``True``, the new selections will be added to the existing ones. (default: ``False``)
   :type add: bool, optional

   :returns: A dictionary containing the selection data for callbacks.
   :rtype: dict

``` 

This function selects the specified targets in molstar. The function takes in a dictionary or list of dictionaries containing the targets (whose value should be generated using the `get_targets()` function), and an optional boolean arguments `add`, which specify whether the selection should replace the current selection or be added to the canvas (defaulting to `False`).

```py
import dash_molstar
from dash import Dash, html
from dash_molstar.helpers import get_targets, get_selection, parse_molecule

segment = get_targets(chain="L", residue=[24,25,26,27])

# select the target
select = get_selection(segment)

app = Dash(__name__)
app.layout = html.Div(
   dash_molstar.MolstarViewer(
      id='viewer', style={'width': '500px', 'height':'500px'},
      data=parse_molecule('3u7y.pdb'),
      select=select
   )
)
```

```{eval-rst}
.. function:: get_focus(targets, analyse=False)

   Focus the camera on the specified targets. If ``analyse`` is set to ``True``, non-covalent interactions within 5 angstroms will be analyzed.

   :param targets: A dictionary or list of dictionaries representing the targets. The values should be generated 
                   by the helper function ``get_targets()``.
   :type targets: Target | List[Target]

   :param analyse: If ``True``, non-covalent interactions within 5 angstroms of the targets will be analyzed. 
                   (default: ``False``)
   :type analyse: bool, optional

   :returns: A dictionary containing the focus data for callbacks.
   :rtype: dict

``` 

This function generates focus data for callbacks to let the camera focus on the specified targets. 

It takes two parameters: `targets` and `analyse`. `targets` is a dictionary or list of dictionaries containing information about the targets to focus on, which is generated using the `get_targets()` helper function. `analyse` is an optional boolean parameter that is set to `False` by default, and if set to `True`, it enables the analysis of non-covalent interactions within a 5 Angstrom radius of the targets.

```py
import dash_molstar
from dash import Dash, html
from dash_molstar.helpers import get_targets, get_focus, parse_molecule

segment = get_targets(chain="L", residue=[24,25,26,27])

# center camera on the target
focus = get_focus(segment, analyse=False)
# center camera on the target
# and show the interactions of the target with molecules around
analyse = get_focus(segment, analyse=True)

app = Dash(__name__)
app.layout = html.Div(
   dash_molstar.MolstarViewer(
      id='viewer', style={'width': '500px', 'height':'500px'},
      data=parse_molecule('3u7y.pdb'),
      focus=analyse
   )
)
```

## Shapes

For helper function for loading shapes into the viewer, please refer to [](shapes.md) for more details.

## Adding Measurements

```{eval-rst}
.. function:: get_measurement(targets, type='label', options=None, add=False)

   Create a measurement for the specified targets in the viewer.

   :param targets: The targets to be measured. The number of targets must meet the requirements of the specified measurement type. The targets should be generated by the helper function ``get_targets()``.
   :type targets: Target | List[Target]

   :param type: The type of measurement to create. Supported types are ``label``, ``orientation``, ``plane``, ``distance``, ``angle``, and ``dihedral``. For ``label``, ``orientation``, and ``plane``, at least one target should be provided. For ``distance``, ``angle``, and ``dihedral``, 2, 3, and 4 targets are required respectively. (default: ``'label'``)
   :type type: str, optional

   :param options: Additional options for the measurement. (default: ``None``)
   :type options: dict, optional

   :param add: If ``False``, existing measurements will be cleared before adding new ones. If ``True``, the new measurements will be added to the molecule. (default: ``False``)
   :type add: bool, optional

   :returns: The measurement data for callbacks.
   :rtype: dict

   :raises ValueError: If the specified measurement type is not supported or the number of targets does not meet the requirements.
   :raises TypeError: If the targets are not valid ``Target`` objects.
```

The `get_measurement` function allows you to create and display various types of measurements (such as distances, angles) for selected targets in the molstar viewer. This is useful for analyzing spatial relationships and geometric properties within molecular structures.

Parameters for the argument `targets` should be generated by the helper function `get_targets()`. For example, the following code snippet shows how to create measurements of distance, label and dihedral angle.

```py
from dash_molstar.helpers import get_targets, get_measurement

# Select two residues for distance measurement
residue1 = get_targets(chain="A", residue=10)
residue2 = get_targets(chain="A", residue=20)

# Create a distance measurement
distance = get_measurement([residue1, residue2], type='distance')

# Add a label to residues
label1 = get_measurement(residue1, type='label')
label2 = get_measurement(residue2, type='label')

# Add phi and psi angles (both require 4 targets)
dihedral_atoms = [
   get_targets(chain="A", residue=24, atom=186),
   get_targets(chain="A", residue=25, atom=192),
   get_targets(chain="A", residue=25, atom=193),
   get_targets(chain="A", residue=25, atom=194),
   get_targets(chain="A", residue=26, atom=202),
]
phi = get_measurement(dihedral_atoms[0:-1], 'dihedral'),
psi = get_measurement(dihedral_atoms[1:], 'dihedral')
```

The measurement instances can be served to the `measurement` property of dash-molstar. If you want to create more than one measurements at a time, return them as a list. 

By default, the existing measurements in the molstar viewer will be cleared before adding new ones. If you wish to keep them, you can specify `add=True`.

```py
phi = get_measurement(dihedral_atoms[0:-1], 'dihedral', add=True)
```

If you have provided multiple measurements as a list, the plugin will only check the `add` parameter of the first element in the list.

## Camera

For deteiled camera control, please refer to [](camera.md) for more details.

## Screenshot

The screenshot feature lets you programmatically capture the current view of the molstar viewer and download it as an image file. To trigger a screenshot from a callback, return the value of `get_screenshot()` to the `screenshot` property of the viewer.

```{eval-rst}
.. function:: get_screenshot(filename, params, crop=None)

   Prepare a screenshot request for the molstar viewer.

   :param filename: The name of the image file to be downloaded (without extension).
   :type filename: str

   :param params: The screenshot configuration. Should be a ``Screenshot`` instance.
   :type params: Screenshot

   :param crop: Override the cropping region. Ignored if not provided; the crop defined
                in ``params`` will be used instead. See the ``crop`` parameter of
                ``Screenshot`` for the expected format. (default: ``None``)
   :type crop: dict, optional

   :returns: The screenshot data to be returned from a Dash callback to the ``screenshot`` property.
   :rtype: dict
```

To customize the screenshot, you will need to pass a `Screenshot` instance to the `params` argument of `get_screenshot()`. The `Screenshot` class has several parameters that allow you to control the resolution, background transparency, axes overlay, illumination settings, and cropping of the screenshot.

```{eval-rst}
.. class:: Screenshot(resolution=named_params('ultra-hd'), transparent=False, axes=named_params('off'), illumination=None, crop=None)

   Configuration object for taking a screenshot.

   :param resolution: The output image resolution.
   :type resolution: dict

   :param transparent: If ``True``, the background of the screenshot will be transparent.
                       (default: ``False``)
   :type transparent: bool, optional

   :param axes: Whether to overlay coordinate axes on the screenshot.
                (default: ``named_params('off')``)
   :type axes: dict

   :param illumination: Advanced illumination settings for the screenshot render.
                        (default: ``None``)
   :type illumination: dict, optional

   :param crop: Crop the screenshot to a sub-region of the image. Autocrop is enabled by default.
                (default: ``None``)
   :type crop: dict, optional
```

:::{seealso}
NamedParams is a molstar defined data type. See how to generate a correct NamedParams, in the [NamedParams](#NamedParams) section.
:::

The argument `resolution` and `axes` are expected to be in the form of a `NamedParams` object. Available options for them are listed below.

The basic usage wires a button to a callback that returns a screenshot request:

```py
import dash_molstar
from dash import Dash, html, Input, Output
from dash_molstar.helpers import parse_molecule, get_screenshot
from dash_molstar.utils import named_params, Screenshot

app = Dash(__name__)
app.layout = html.Div([
    dash_molstar.MolstarViewer(
        id='viewer', style={'width': '800px', 'height': '600px'},
        data=parse_molecule('3u7y.pdb')
    ),
    html.Button("Download Screenshot", id='download-btn'),
])

@app.callback(
    Output("viewer", "screenshot"),
    Input("download-btn", "n_clicks"),
    prevent_initial_call=True
)
def download_screenshot(n_clicks):
    params = Screenshot()  # ultra-hd, opaque background, no axes overlay
    return get_screenshot(filename='my_structure', params=params)
```

### Resolution

Molstar allows you to choose from several preset resolutions or specify custom dimensions for the output image.

- **resolution** (NamedParams) – resolution preset for the screenshot. Available options include:
    - *viewport* (None as NamedParams) – Match the current viewer size.
    - *hd* (None as NamedParams) – 1280 × 720.
    - *full-hd* (None as NamedParams) – 1920 × 1080.
    - *ultra-hd* (None as NamedParams) – 3840 × 2160.
    - *custom* (dict as NamedParams) – User-defined.
      - *width* (int) – Width of the output image in pixels.
      - *height* (int) – Height of the output image in pixels.

Some use cases for different resolution settings:

```py
from dash_molstar.utils import named_params

# Ultra HD (3840x2160)
params = Screenshot(resolution=named_params('ultra-hd'))

# Custom dimensions
params = Screenshot(resolution=named_params('custom', {'width': 4096, 'height': 4096}))

# Match the current viewer canvas size
params = Screenshot(resolution=named_params('viewport'))
```

### Transparent background

Set `transparent=True` to export the image with a transparent background (PNG only):

```py
params = Screenshot(
    resolution=named_params('ultra-hd'),
    transparent=True,
)
```

### Axes overlay

Use `axes=named_params('on', params)` to include a coordinate axes indicator in the screenshot. If you would like to show axes on the screenshot, the `default_axes_params` dict provides sensible defaults for the axes appearance:

```py
from dash_molstar.helpers import Screenshot
from dash_molstar.utils import named_params, default_axes_params

# Show axes with default appearance
params = Screenshot(
    resolution=named_params('ultra-hd'),
    axes=named_params('on', default_axes_params),
)

# Hide axes (default)
params = Screenshot(
    axes=named_params('off'),
)
```

The `default_axes_params` dict and its keys:

| Key | Default | Description |
|---|---|---|
| `alpha` | `0.51` | Opacity of the axes |
| `colorX` | `0xFF0000` | Color of the X axis |
| `colorY` | `0x00FF00` | Color of the Y axis |
| `colorZ` | `0x0000FF` | Color of the Z axis |
| `scale` | `0.33` | Overall size scale of the axes widget |
| `location` | `'bottom-left'` | Position on screen |
| `locationOffsetX` | `0` | Horizontal offset from the anchor |
| `locationOffsetY` | `0` | Vertical offset from the anchor |
| `originColor` | `0x808080` | Color of the origin sphere |
| `radiusScale` | `0.075` | Radius of the axis cylinders |
| `showPlanes` | `True` | Whether to show the XY/XZ/YZ planes |
| `planeColorXY` | `0x808080` | Color of the XY plane |
| `planeColorXZ` | `0x808080` | Color of the XZ plane |
| `planeColorYZ` | `0x808080` | Color of the YZ plane |
| `showLabels` | `False` | Whether to show axis labels |
| `labelX` | `'X'` | Label text for X axis |
| `labelY` | `'Y'` | Label text for Y axis |
| `labelZ` | `'Z'` | Label text for Z axis |
| `labelColorX` | `0x808080` | Label color for X axis |
| `labelColorY` | `0x808080` | Label color for Y axis |
| `labelColorZ` | `0x808080` | Label color for Z axis |
| `labelOpacity` | `1` | Label opacity |
| `labelScale` | `0.25` | Label size scale |

### Cropping

Use the `crop` parameter to capture only a sub-region of the image. All values are fractions (0.0–1.0) relative to the full image dimensions:

```py
# Capture the center quarter of the image
params = Screenshot(
    resolution=named_params('ultra-hd'),
    crop={'x': 0.25, 'y': 0.25, 'width': 0.5, 'height': 0.5}
)
```

### Saving and loading configurations

A `Screenshot` instance can be serialized to JSON so you can reuse configurations:

```py
# Save configuration to a file
params = Screenshot(
    resolution=named_params('ultra-hd'),
    transparent=True,
    axes=named_params('off'),
)
params.save_config('my_screenshot_config')  # saves as my_screenshot_config.json

# Load it back in another session
params = Screenshot.from_config('my_screenshot_config.json')
```

