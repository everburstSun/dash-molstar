# dash-molstar

## Introduction
`dash-molstar` is a Dash component library that integrate [Molstar Viewer](https://github.com/molstar/rcsb-molstar) into Dash framework. Molstar is a modern, web-based software framework for molecular visualization and analysis. With Dash, one can use pure python code to control some basic operations of molstar and easily embed this plugin into their web page.

## Installation

This library can be easily installed with `pip`:

```
pip install dash-molstar
```

## Usage

Import `dash_molstar` and then you can add it to your layout as you did to other components:

```py
import dash_molstar
from dash import Dash, html

app = Dash(__name__)
app.layout = html.Div(
    dash_molstar.MolstarViewer(
        id='viewer', style={'width': '500px', 'height':'500px'}
    ),
)

if __name__ == '__main__':
    app.run_server(debug=True)
```

Clone the repository to your local directory and run the following command to see the demo:

```
python usage.py
```

## Documentation

To see the detailed introduction of parameters and callbacks, check out the [Documentation](https://dash-molstar.readthedocs.io/).