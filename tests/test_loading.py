"""
Molstar loading test scenarios.

Run this file directly and click buttons to verify loading behaviors:
1. Load local PDB/CIF
2. Load remote PDB/CIF
3. Load PDB with custom representation
4. Load PDB with preset
5. Load multiple PDB entries
6. Load PDB with homogeneous transform matrix
"""

import os

import dash_molstar
import numpy as np
from dash import Dash, Input, Output, ctx, html
from dash_molstar.utils import Representation
from dash_molstar.helpers import (
	create_component,
	get_targets,
	parse_molecule,
	parse_url,
)


BASE_DIR = os.path.dirname(__file__)
LOCAL_PDB = os.path.join(BASE_DIR, "3u7y.pdb")
LOCAL_CIF = os.path.join(BASE_DIR, "7u28.cif")

REMOTE_PDB = "https://files.rcsb.org/download/3U7Y.pdb"
REMOTE_CIF = "https://files.rcsb.org/download/7U28.cif"


app = Dash(__name__)
app.layout = html.Div(
	[
		html.H3("Molstar Loading Test"),
		html.Div(
			[
				html.Button("Local: PDB + CIF", id="btn-local", n_clicks=0),
				html.Button("Remote: PDB + CIF", id="btn-remote", n_clicks=0),
				html.Button("PDB + Representation", id="btn-rep", n_clicks=0),
				html.Button("PDB + Preset", id="btn-preset", n_clicks=0),
				html.Button("Multiple PDB", id="btn-multi", n_clicks=0),
				html.Button("PDB + Transform Matrix", id="btn-matrix", n_clicks=0),
			],
			style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "12px"},
		),
		html.Div(id="status", style={"marginBottom": "8px"}),
		dash_molstar.MolstarViewer(
			id="viewer",
			style={"width": "100%", "height": "680px"},
		),
	],
	style={"padding": "12px"},
)


@app.callback(
	Output("viewer", "data"),
	Output("status", "children"),
	Input("btn-local", "n_clicks"),
	Input("btn-remote", "n_clicks"),
	Input("btn-rep", "n_clicks"),
	Input("btn-preset", "n_clicks"),
	Input("btn-multi", "n_clicks"),
	Input("btn-matrix", "n_clicks"),
	prevent_initial_call=True,
)
def run_loading_tests(*yes):
	triggered = ctx.triggered_id

	if triggered == "btn-local":
		data = [
			parse_molecule(LOCAL_PDB),
			parse_molecule(LOCAL_CIF),
		]
		return data, "Loaded local PDB and local CIF."

	if triggered == "btn-remote":
		data = [
			parse_url(REMOTE_PDB),
			parse_url(REMOTE_CIF),
		]
		return data, "Loaded remote PDB and remote CIF."

	if triggered == "btn-rep":
		heavy_chain = get_targets(chain="H")
		surface = Representation("molecular-surface", "uniform")
		surface.set_type_params({"xrayShaded": True, "alpha": 0.8})
		surface.set_color_params({"value": 0x2A9D8F})
		comp = create_component("Heavy chain surface", heavy_chain, surface)
		data = parse_molecule(LOCAL_PDB, component=comp)
		return data, "Loaded PDB with custom component representation."

	if triggered == "btn-preset":
		data = parse_molecule(LOCAL_PDB, preset={"kind": "empty"})
		return data, "Loaded PDB with preset kind='empty'."

	if triggered == "btn-multi":
		data = [
			parse_url("https://files.rcsb.org/download/3U7Y.pdb"),
			parse_url("https://files.rcsb.org/download/1CRN.pdb"),
		]
		return data, "Loaded multiple PDB entries (3U7Y and 1CRN)."

	if triggered == "btn-matrix":
		transform = np.array(
			[
				[1.0, 0.0, 0.0, 30.0],
				[0.0, 1.0, 0.0, 0.0],
				[0.0, 0.0, 1.0, 0.0],
				[0.0, 0.0, 0.0, 1.0],
			]
		)
		data = [
			parse_url("https://files.rcsb.org/download/3U7Y.pdb"),
			parse_url("https://files.rcsb.org/download/1CRN.pdb", matrix=transform),
		]
		return data, "Loaded PDB with homogeneous transform matrix."

	return None, ""


if __name__ == "__main__":
	app.run(debug=True)
