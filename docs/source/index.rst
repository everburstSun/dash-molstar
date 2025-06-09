dash-molstar documentation
==========================

**dash-molstar** is a Dash component library that integrates `Molstar Viewer <https://github.com/molstar/rcsb-molstar>`_ into Dash framework. Molstar is a modern, web-based software framework for molecular visualization and analysis. With Dash, one can use pure python code to control some basic operations of molstar and easily embed this plugin into their web page.

Installation
------------

This library can be easily installed with ``pip``:

.. code-block:: bash

   pip install dash-molstar

Or install from the source code:

.. code-block:: bash

   git clone https://github.com/everburstSun/dash-molstar
   cd dash-molstar
   python setup.py build
   python setup.py install

Quick Start
-----------

Import ``dash_molstar`` and then you can add it to your layout as you did to other components:

.. code-block:: python

   import dash_molstar
   from dash import Dash, html
   from dash_molstar.utils import molstar_helper

   app = Dash(__name__)
   app.layout = html.Div(
      dash_molstar.MolstarViewer(
         id='viewer', style={'width': '500px', 'height':'500px'}
      ),
      html.Button(id='load_protein', children="Load Protein")
   )

   if __name__ == '__main__':
      app.run_server(debug=True)

Or if you want the viewer have a default molecule loaded:

.. code-block:: python

   dash_molstar.MolstarViewer(
      data=molstar_helper.parse_molecule('3u7y.pdb'),
      id='viewer', style={'width': '500px', 'height':'500px'}
   )

You can add the following code to load a structure from a local file with callback:

.. code-block:: python

    @app.callback(Output('viewer', 'data'), 
                  Input('load_protein', 'n_clicks'),
                  prevent_initial_call=True)
    def display_output(yes):
        data = molstar_helper.parse_molecule('3u7y.pdb')
        return data

Or from a remote URL:

.. code-block:: python

    @app.callback(Output('viewer', 'data'), 
                  Input('load_protein', 'n_clicks'),
                  prevent_initial_call=True)
    def display_output(yes):
        data = molstar_helper.parse_url('https://files.rcsb.org/download/3U7Y.cif')
        return data


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   load
   helper
   properties
   callbacks
   targets
   representations