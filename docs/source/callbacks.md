```{toctree}
:maxdepth: 2

   load
   helper
   properties
   callbacks
   targets
   representations
```

# Using Callbacks

The MolstarViewer component allows the serveral properties to be controlled by callbacks: `data`, `focus`, `selection`, `hover`, `frame`, `measurement`, `updatefocusonframechange`, and `updateselectiononframechange`. Explainations for these properties can be found at [](properties.md).

Assuming that you have already created a `MolstarViewer` with `id='viewer'` and a button with `id='load_protein'`:

```py
import dash_molstar
from dash import Dash, callback, html, Input, Output
from dash_molstar.utils import molstar_helper

app = Dash(__name__)
app.layout = html.Div(
    dash_molstar.MolstarViewer(
        id='viewer', style={'width': '500px', 'height':'500px'}
    ),
    html.Button(id='load_protein', children="Load Protein"),
)
```

### Property `data`
The `data` property is used to set the data displayed in the viewer. Now let's link the button to molstar with a callback function to load protein into the viewer:

```py
# You can also use @app.callback or @Dash.callback for the decorator here.
@callback(Output('viewer', 'data'), 
          Input('load_protein', 'n_clicks'),
          prevent_initial_call=True)
def display_output(yes):
    data = molstar_helper.parse_molecule('3u7y.pdb')
    return data
```

You can also let molstar to fetch a remote url. Remember to specify the file format if you are not accessing a static file:

```py
@callback(Output('viewer', 'data'), 
          Input('load_protein', 'n_clicks'),
          prevent_initial_call=True)
def display_output(yes):
    data = molstar_helper.parse_url('https://files.rcsb.org/download/3U7Y.pdb')
    # or a CIF file instead
    # data = molstar_helper.parse_url('https://files.rcsb.org/download/3U7Y.cif')
    return data
```

If you wish to load multiple structures, simply return a list of data object:

```py
from rdkit.Chem import AllChem

@callback(Output('viewer', 'data'), 
          Input('load_protein', 'n_clicks'),
          prevent_initial_call=True)
def display_output(yes):
    data = []
    # append "3u7y.pdb" into data
    data.append(molstar_helper.parse_molecule('3u7y.pdb'))
    # append a new molecule Acetophenone to data
    mol = AllChem.MolFromSmiles("CC(C1=CC=CC=C1)=O")
    AllChem.Compute2DCoords(mol)
    PDBBlock = AllChem.MolToPDBBlock(mol)
    # Without a filename to infer format, the format has to be specified manually
    data.append(molstar_helper.parse_molecule(PDBBlock, fmt='pdb'))
    return data
```

:::{seealso}
By default, molstar will create a "polymer" component with cartoon representation for all standard residues. 
To disable this behaviour and customize your representation, see how to control the representation of components, in the [](representations.md) section.
:::

You can use shapes like a Bounding Box to highlight a region on the structure. If you have serval input boxes on your page, you can let the user adjust settings like this:

```py
import dash_molstar
import dash_bootstrap_components as dbc
from dash import html, callback, Dash, Input, Output
from dash_molstar.utils import molstar_helper

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

content = dbc.Row([
    dbc.Col([
        dash_molstar.MolstarViewer(
            id='viewer',style={'width': 'auto', 'height':'500px'}
        )
    ]),
    dbc.Col([
        html.Strong("Box center:"),
        dbc.InputGroup(
                [
                    dbc.InputGroupText("x"),
                    dbc.Input(value=-1.6, type="number", id='center_x-box'),
                ],
                className="mb-3",
            ),
        dbc.InputGroup(
                [
                    dbc.InputGroupText("y"),
                    dbc.Input(value=-0.8, type="number", id='center_y-box'),
                ],
                className="mb-3",
            ),
        dbc.InputGroup(
                [
                    dbc.InputGroupText("z"),
                    dbc.Input(value=13.7, type="number", id='center_z-box'),
                ],
                className="mb-3",
            ),
    ], width=6),
    dbc.Col([
        html.Strong("Box size:"),
        dbc.InputGroup(
                [
                    dbc.InputGroupText("x"),
                    dbc.Input(value=10.3, type="number", id='size_x-box'),
                ],
                className="mb-3",
            ),
        dbc.InputGroup(
                [
                    dbc.InputGroupText("y"),
                    dbc.Input(value=14.3, type="number", id='size_y-box'),
                ],
                className="mb-3",
            ),
        dbc.InputGroup(
                [
                    dbc.InputGroupText("z"),
                    dbc.Input(value=13.8, type="number", id='size_z-box'),
                ],
                className="mb-3",
            ),
    ], width=6)
])

app.layout = dbc.Container(content)

@callback(Output('viewer', 'data'),
          Input('center_x-box', 'value'),
          Input('center_y-box', 'value'),
          Input('center_z-box', 'value'),
          Input('size_x-box', 'value'),
          Input('size_y-box', 'value'),
          Input('size_z-box', 'value'),
          prevent_initial_call=True)
def updateBox(center_x,center_y,center_z,size_x,size_y,size_z):
    _min = (center_x-size_x/2, center_y-size_y/2, center_z-size_z/2)
    _max = (center_x+size_x/2, center_y+size_y/2, center_z+size_z/2)
    box = molstar_helper.get_box(_min, _max)
    return box
```

Specify which Bounding Box to control by the `label` parameter. The default value is `"Bounding Box"`. If there is no box in the viewer with the given name, a box will be created. Otherwise the existing one get updated.

### Property `focus`

The `focus` property allows you to focus on a specific target. This equivalent to left-clicking on a residue in the molstar viewer. This will analyze the non-covalent interactions around the target. by specifing `analyse=True`

```py
@callback(Output('viewer', 'focus'),
          Input('focus-cdr', 'n_clicks'),
          prevent_initial_call=True)
def focus_CDR(yes):
    CDR = molstar_helper.get_targets(chain="L", residue=[24,25,26,27])
    cdr = molstar_helper.get_focus(CDR, analyse=True)

    return cdr
```

If you wish to get which target that the user is focusing on, you can also retrieve data from this property:

```py
from dash_molstar.utils.target import Target

@callback(Input('viewer', 'focus'),
          prevent_initial_call=True)
def retrieve_focus(focus):
    target = Target(focus)
    print("Target valid:", target.valid)
    print("Number of chains:", len(target))
    for chain in target.chains:
        print("Chain name:", chain.name, ",Auth name:", chain.auth_name)
        for residue in chain.residues:
            print("  Residue index:", residue.index, ",Residue number:", str(residue.number)+residue.ins_code, ",Name:", residue.name)
            for atom in residue.atoms:
                print("    Atom name:", atom.name, ",x:", atom.x, ",y:", atom.y, ",z:", atom.z)
```

:::{seealso}
For a detailed introduction of the **Target** class, see the [](targets.md) section.
:::

You can choose not to analyze the non-covalent interactions by specifing `analyse=False`, which is equivalent to right-clicking on a residue in the molstar viewer. This will only center the camera on the targets. And in this case, the focus property will not produce any output:

```py
@callback(Output('viewer', 'focus'),
          Input('focus-cdr', 'n_clicks'),
          prevent_initial_call=True)
def focus_CDR(yes):
    CDR = molstar_helper.get_targets(chain="L", residue=[24,25,26,27])
    cdr = molstar_helper.get_focus(CDR, analyse=False)

    return cdr
```

Sometimes when you are working on a molecular dynamic trajectory, you can also update the focus data when switch between frames, if you want to get the latest atom coordinates in the stage. In this case, you need to set `updatefocusonframechange=True` for the molstar viewer. You can also control it through a callback.

```py
dash_molstar.MolstarViewer(
    id='viewer',style={'width': 'auto', 'height':'500px'},
    updatefocusonframechange=True
)
```

### Property `hover`

This property can help you highlight some targets on the molecule. Controlling this property is equivalent to hovering your cursor on the molecules in the molstar viewer.

If you have a button on your webpage with the id `'highlight-cdr'`, the following callback will cause some residues to be highlighted when click on the button:

```py
@callback(Output('viewer', 'hover'),
          Input('highlight-cdr', 'n_clicks'),
          prevent_initial_call=True)
def highlight_CDR(yes):
    CDR = molstar_helper.get_targets(chain="L", residue=[24,25,26,27])
    cdr = molstar_helper.get_selection(CDR)

    return cdr
```

### Property `selection`

This property can select the specified targets.

If you have a button on your webpage with the id `'select-cdr'`, the following callback will cause some residues to be selected when click on the button:

```py
@callback(Output('viewer', 'selection'),
          Input('select-cdr', 'n_clicks'),
          prevent_initial_call=True)
def select_CDR(yes):
    CDR = molstar_helper.get_targets(chain="L", residue=[24,25,26,27])
    cdr = molstar_helper.get_selection(CDR)

    return cdr
```

Like `focus`, you can also retrieve data from `selection`. You should use the [](targets.md) class to parse the incoming data:

```py
from dash_molstar.utils.target import Target

@callback(Input('viewer', 'selection'),
          prevent_initial_call=True)
def retrieve_focus(selection):
    target = Target(selection)
    print("Target valid:", target.valid)
    print("Number of chains:", len(target))
    for chain in target.chains:
        print("Chain name:", chain.name, ",Auth name:", chain.auth_name)
        for residue in chain.residues:
            print("  Residue index:", residue.index, ",Residue number:", str(residue.number)+residue.ins_code, ",Name:", residue.name)
            for atom in residue.atoms:
                print("    Atom name:", atom.name, ",x:", atom.x, ",y:", atom.y, ",z:", atom.z)
```

For trajectory, you can also update the selection data when switch between frames. Just set `updateselectiononframechange=True` for the molstar viewer. You can also control it through a callback.

```py
dash_molstar.MolstarViewer(
    id='viewer',style={'width': 'auto', 'height':'500px'},
    updateselectiononframechange=True
)
```

Furthermore, you can combine `hover` and `focus` together. Assuming that we have a `dcc.Graph` object, it has a hover property and a click property. We can link the `hoverData` of the graph to the `hover` of viewer, and `clickData` to `focus`. (You can also find the following code snippet in the github [repository](https://github.com/everburstSun/dash-molstar/blob/main/usage.py))

```py
import dash_molstar
from dash import Dash, callback, html, Input, Output, dcc, ctx
from dash_molstar.utils import molstar_helper
import dash
import pandas as pd
import plotly.express as px

app = Dash(__name__)
df = pd.read_json("H_G_interaction.json")
app.layout = html.Div(
    dash_molstar.MolstarViewer(
        id='viewer', style={'width': '500px', 'height':'500px'}
    ),
    html.Button(id='load_protein', children="Load Protein"),
    dcc.Graph(id='figure', clear_on_unhover=True, figure=px.imshow(df, labels=dict(color="energy"), color_continuous_scale='Blues_r',range_color=[-80, 0], text_auto=True)),
)

@callback(Output('viewer', 'data'), 
          Input('load_protein', 'n_clicks'),
          prevent_initial_call=True)
def display_output(yes):
    data = molstar_helper.parse_molecule('3u7y.pdb')
    return data

@callback(Output('viewer', 'hover'),
          Output('viewer', 'focus'),
          Input('figure', 'hoverData'),
          Input('figure', 'clickData'),
          prevent_initial_call=True)
def mouse_event(hoverData, clickData):
    focusdata = dash.no_update
    if ctx.triggered_prop_ids.get('figure.hoverData'):
        data = hoverData
        select = False
        focus = False
    else:
        data = clickData
        select = True
        focus = True
    if not data: return molstar_helper.get_selection(None, add=False), focusdata
    residue1 = data['points'][0]['x']
    residue1 = molstar_helper.get_targets(residue1[0], residue1[1:])
    residue2 = data['points'][0]['y']
    residue2 = molstar_helper.get_targets(residue2[0], residue2[1:])
    seldata = molstar_helper.get_selection([residue1, residue2], add=False)
    if focus: focusdata = molstar_helper.get_focus([residue1, residue2], analyse=True)
    return seldata, focusdata
```

### Property `measurement`

This property is used to add measurements into the viewer.

There are 6 measurement types in total in molstar viewer: `label`, `orientation`, `plane`, `distance`, `angle` and `dihedral`. Users can use the helper function `get_measurement` to create one or more measurements for the loaded structure.

```py
from dash_molstar.utils import molstar_helper
from dash import callback, Input, Output

@callback(Output('viewer', 'measurement'),
          Input('add_measurement', 'n_clicks'),
          prevent_initial_call=True)
def add_measurement(yes):
    distance_atoms = [
        molstar_helper.get_targets("A", 24, 187),
        molstar_helper.get_targets("A", 28, 220),
    ]
    measurement = molstar_helper.get_measurement(distance_atoms, 'distance')
    return measurement
```

:::{seealso}
The definition of function ``get_measurement`` in the [](helper.md#adding-measurements) section.
:::

Each type of measurement requires certain numbers of targets, listed in the following table:

| Type | Targets |
|--------:|--------:|
| label | 1 |
| distance | 2 |
| angle | 3 |
| dihedral | 4 |
| orientation | >= 1 |
| plane | >= 1 |

### Property `frame`

The `frame` property allows you to control and monitor the currently displayed frame of a molecular trajectory. It is a 0-indexed integer, meaning the first frame is `0`, the second is `1`, and so on.

You can use this property as either an `Output` to set the current frame (e.g., using a slider), or as an `Input` to retrieve the current frame number from the viewer (e.g., if the user changes frames using the viewer's built-in controls).

The example below demonstrates how to use a `dcc.Slider` to allow the user to select a frame, and display the current frame number (1-based for user-friendliness) by listening to changes in the `frame` property. Since it doesn't need to communicate with the server, the example code uses clientside callbacks for the conversion.

```py
import os
import dash_molstar
import dash_bootstrap_components as dbc
from dash import html, callback, Dash, clientside_callback, dcc, Input, Output
from dash_molstar.utils import molstar_helper
from dash_molstar.utils.representations import Representation

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

content = dbc.Row([
    html.H1("Load Trajectory"),
    dbc.Col([
        dash_molstar.MolstarViewer(
            id='viewer',style={'width': 'auto', 'height':'500px'}
        )
    ]),
    dbc.Col([
        html.Button(id='load_traj', children="Load Trajectory", className="btn btn-primary", style={'padding': '5px', 'margin': '5px'}),
        html.Br(),
        html.Span([html.Label("Current Frame Number: ", style={'margin': '10px 10px 50px 5px'}), html.Strong(id='frame_number')]),
        html.Br(),
        html.Label("Select Frame", style={'margin': '5px 0 5px 5px'}),
        dcc.Slider(1, 10, 1, value=1, id='frame_select',updatemode='drag'),
    ])
])

@callback(Output('viewer', 'data'), 
          Input('load_traj', 'n_clicks'),
          prevent_initial_call=True)
def load_traj(yes):
    chainA = molstar_helper.get_targets(chain="A")

    cartoon = Representation('cartoon', 'secondary-structure', 'uniform')
    surface = Representation('gaussian-surface', 'uniform', 'physical')
    surface.set_type_params({'radiusOffset': 0.3, 'ignoreHydrogens': True, 'alpha': 0.1})
    surface.set_color_params({'value': 0x009CE0})
    polymer = molstar_helper.create_component("polymer", chainA, [cartoon, surface])

    topo = molstar_helper.parse_molecule(os.path.join('tests', 'Villin.gro'), component=polymer, preset={'kind': 'empty'})
    coords = molstar_helper.parse_coordinate(os.path.join('tests', 'Villin.trr'))

    data = molstar_helper.get_trajectory(topo, coords)
    return data

clientside_callback(
    """
    function (value) {
        return value-1; // 0-based index for the frame
    }
    """,
    Output('viewer', 'frame'), 
    Input('frame_select', 'value'),
    prevent_initial_call=True
)

clientside_callback(
    """
    function (value) {
        return value+1; // 1-based index for the frame
    }
    """,
    Output('frame_number', 'children'),
    Input('viewer', 'frame'),
    prevent_initial_call=True
)
```