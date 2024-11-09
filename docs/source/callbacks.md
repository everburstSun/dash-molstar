```{toctree}
:maxdepth: 2

   load
   parameters
   helper
   callbacks
   representations
```

# Callbacks

The MolstarViewer component allows the `data`, `focus`, and `selection` parameters to be controlled by callbacks.

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
### Parameter `data`
The `data` parameter is used to set the data displayed in the viewer. Now let's link the button to molstar with a callback function to load protein into the viewer:

```py
# You can either use @app.callback or @Dash.callback for the decorator here.
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
See how to control the representation of components, in the [](representations.md) section.
:::

You can use shapes like a Bounding Box to highlight a region on the structure. If you have serval input boxes on your page, you can let the user adjust settings like this:

```py
@callback(Output('viewer', 'data'),
          Input('center_x', 'value'),
          Input('center_y', 'value'),
          Input('center_z', 'value'),
          Input('size_x', 'value'),
          Input('size_y', 'value'),
          Input('size_z', 'value'),
          prevent_initial_call=True)
def updateBox(center_x,center_y,center_z,size_x,size_y,size_z):
    _min = (center_x-size_x/2, center_y-size_y/2, center_z-size_z/2)
    _max = (center_x+size_x/2, center_y+size_y/2, center_z+size_z/2)
    box = molstar_helper.get_box(_min, _max)
    return box
```


### Parameter `focus`

The `focus` parameter allows you to focus the camera on a specific target. This equivalent to right-clicking on a residue in the molstar viewer.

```py
@callback(Output('viewer', 'focus'),
          Input('focus-cdr', 'n_clicks'),
          prevent_initial_call=True)
def focus_CDR(yes):
    CDR = molstar_helper.get_targets(chain="L", residue=[24,25,26,27])
    cdr = molstar_helper.get_focus(CDR)

    return cdr
```

You can choose to analyze the non-covalent interactions around the target by specifing `analyse=True`, which is equivalent to left-clicking on a residue in the molstar viewer.

```py
@callback(Output('viewer', 'focus'),
          Input('focus-cdr', 'n_clicks'),
          prevent_initial_call=True)
def focus_CDR(yes):
    CDR = molstar_helper.get_targets(chain="L", residue=[24,25,26,27])
    cdr = molstar_helper.get_focus(CDR, analyse=True)

    return cdr
```

### Parameter `selection`

This parameter can select the specified targets. It has two mode: the "select" mode and "hover" mode. Switching between the two modes by specifing `select=True`.

Remember to add corresponding buttons to the layout if you are trying the following code.

```py
@callback(Output('viewer', 'selection'),
          Input('select-cdr', 'n_clicks'),
          prevent_initial_call=True)
def select_CDR(yes):
    CDR = molstar_helper.get_targets(chain="L", residue=[24,25,26,27])
    # select by default
    cdr = molstar_helper.get_selection(CDR)

    return cdr
```

```py
@callback(Output('viewer', 'selection'),
          Input('highlight-cdr', 'n_clicks'),
          prevent_initial_call=True)
def highlight_CDR(yes):
    CDR = molstar_helper.get_targets(chain="L", residue=[24,25,26,27])
    # hover mode
    cdr = molstar_helper.get_selection(CDR, select=False)

    return cdr
```

Furthermore, you can combine `selection` and `focus` together. Assuming that we have a `dcc.Graph` object, it has a hover parameter and a click parameter. We can link the `hoverData` of the graph to the `selection` of viewer, and `clickData` to `focus`.

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

@callback(Output('viewer', 'selection'),
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
    if not data: return molstar_helper.get_selection(None, select=select, add=False), focusdata
    residue1 = data['points'][0]['x']
    residue1 = molstar_helper.get_targets(residue1[0], residue1[1:])
    residue2 = data['points'][0]['y']
    residue2 = molstar_helper.get_targets(residue2[0], residue2[1:])
    seldata = molstar_helper.get_selection([residue1, residue2], select=select, add=False)
    if focus: focusdata = molstar_helper.get_focus([residue1, residue2], analyse=True)
    return seldata, focusdata
```