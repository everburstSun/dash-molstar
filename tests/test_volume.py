"""
Molstar volume loading test scenarios.

Run this file directly and click buttons to verify volume loading behaviors:
1. Load a remote PDB structure
2. Load a remote volume (CCP4 density map)
3. Load the structure together with its volume

The isovalue dicts follow molstar's `VolumeIsovalueInfo` shape:
`{'type': 'absolute' | 'relative', 'value': float, 'color': int, 'alpha'?: float, 'volumeIndex'?: int}`
"""

import dash_molstar
from dash import Dash, Input, Output, ctx, html
from dash_molstar.helpers import parse_url, get_volume


REMOTE_PDB = "https://files.rcsb.org/download/1TQN.pdb"
REMOTE_VOLUME = "https://maps.rcsb.org/x-ray/1tqn/box/-41.696,-62.869,-43.855/7.288,14.016,20.119?detail=3"


def make_volume():
	# 1tqn.ccp4 is a single binary CCP4 map, so a single relative isosurface is used.
	source = parse_url(REMOTE_VOLUME, fmt='dscif')
	isovalue = [{
        "type": "relative",
        "value": 1.5,
        "color": 0x3362B2,
		"alpha": 0.3
    }, {
        "type": "relative",
        "value": 3,
        "color": 0x33BB33,
        "volumeIndex": 1,
		"alpha": 0.3
    }, {
        "type": "relative",
        "value": -3,
        "color": 0xBB3333,
        "volumeIndex": 1,
		"alpha": 0.3
    }]
	return get_volume(source, isovalues=isovalue, entryId=['2FO-FC', 'FO-FC'], isBinary=True, isLazy=False)


app = Dash(__name__)
app.layout = html.Div(
	[
		html.H3("Molstar Volume Test"),
		html.Div(
			[
				html.Button("Structure only", id="btn-structure", n_clicks=0),
				html.Button("Volume only", id="btn-volume", n_clicks=0),
				html.Button("Structure + Volume", id="btn-both", n_clicks=0),
			],
			style={"display": "flex", "gap": "8px", "flexWrap": "wrap", "marginBottom": "12px"},
		),
		html.Div(id="status", style={"marginBottom": "8px"}),
		dash_molstar.MolstarViewer(
			id="viewer",
			style={"width": "100%", "height": "680px"},
			layout={'showVolumeStreamingControls': True}
		),
	],
	style={"padding": "12px"},
)


@app.callback(
	Output("viewer", "data"),
	Output("status", "children"),
	Input("btn-structure", "n_clicks"),
	Input("btn-volume", "n_clicks"),
	Input("btn-both", "n_clicks"),
	prevent_initial_call=True,
)
def run_volume_tests(*yes):
	triggered = ctx.triggered_id

	if triggered == "btn-structure":
		data = parse_url(REMOTE_PDB)
		return data, "Loaded remote PDB (1TQN)."

	if triggered == "btn-volume":
		data = make_volume()
		return data, "Loaded remote volume (1tqn.ccp4)."

	if triggered == "btn-both":
		data = [
			parse_url(REMOTE_PDB),
			make_volume(),
		]
		return data, "Loaded remote PDB (1TQN) with its volume (1tqn.ccp4)."

	return None, ""


if __name__ == "__main__":
	app.run(debug=True)
