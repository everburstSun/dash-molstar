"""
Molstar volume loading test scenarios.

Run this file directly and click the buttons to verify volume loading. The volume and structure files
come from the NGL viewer test data (https://github.com/nglviewer/ngl/tree/master/data), so an internet
connection is required. Loading failures are logged to the browser console.

The isovalue dicts follow molstar's `VolumeIsovalueInfo` shape:
`{'type': 'absolute' | 'relative', 'value': float, 'color': int, 'alpha'?: float, 'volumeIndex'?: int}`
"""

import dash_molstar
from dash import Dash, Input, Output, ctx, html
from dash_molstar.helpers import parse_url, get_volume


NGL_DATA = "https://raw.githubusercontent.com/nglviewer/ngl/master/data"
RCSB_PDB = "https://files.rcsb.org/download/1TQN.pdb"
RCSB_VOLUME = "https://maps.rcsb.org/x-ray/1tqn/box/-41.696,-62.869,-43.855/7.288,14.016,20.119?detail=3"
BLUE, GREEN, RED = 0x3362B2, 0x33BB33, 0xBB3333


def from_ngl(name):
	return parse_url(f"{NGL_DATA}/{name}")


def iso(value, color, kind='relative', alpha=0.5, **extra):
	return {'type': kind, 'value': value, 'color': color, 'alpha': alpha, **extra}


def xray_maps():
	# 2Fo-Fc map at 1.5 sigma, Fo-Fc difference map at +/-3 sigma
	return [
		from_ngl('1lee.pdb'),
		get_volume(from_ngl('1lee.ccp4'), iso(1.5, BLUE, alpha=0.3), entryId='1LEE 2Fo-Fc'),
		get_volume(from_ngl('1lee_diff.ccp4'), [iso(3, GREEN), iso(-3, RED)], entryId='1LEE Fo-Fc'),
	]


def apbs_potential(name):
	# APBS potentials are in kT/e
	return [
		from_ngl('1crn.pdb'),
		get_volume(from_ngl(name), [iso(1, BLUE, kind='absolute', alpha=0.4), iso(-1, RED, kind='absolute', alpha=0.4)]),
	]


def density_server_maps():
	# the RCSB volume server returns the 2Fo-Fc and Fo-Fc maps as two data blocks
	source = parse_url(RCSB_VOLUME, fmt='dscif')
	isovalues = [iso(1.5, BLUE, alpha=0.3), iso(3, GREEN, alpha=0.3, volumeIndex=1), iso(-3, RED, alpha=0.3, volumeIndex=1)]
	return [parse_url(RCSB_PDB), get_volume(source, isovalues, entryId=['2FO-FC', 'FO-FC'])]


SCENARIOS = {
	# CCP4 / MRC / MAP
	'ccp4': ("1LEE 2Fo-Fc + Fo-Fc (.ccp4)", xray_maps),
	'mrc': ("betaGal (.mrc), default visuals", lambda: get_volume(from_ngl('betaGal.mrc'))),
	'map-gz': ("EMD-2682 cryo-EM (.map.gz), EMDB contour level", lambda: get_volume(from_ngl('emd_2682.map.gz'), entryId='EMD-2682')),
	'ccp4-mode0': ("3PQR int8 map (mode 0 .ccp4)", lambda: [from_ngl('3pqr.pdb'), get_volume(from_ngl('3pqr-mode0.ccp4'), iso(1.5, BLUE, alpha=0.3))]),
	# DSN6 / BRIX
	'dsn6': ("3STR 2Fo-Fc (.dsn6)", lambda: [from_ngl('3str.cif'), get_volume(from_ngl('3str-2fofc.dsn6'), iso(1.5, BLUE, alpha=0.3))]),
	'brix': ("3STR 2Fo-Fc (.brix)", lambda: [from_ngl('3str.cif'), get_volume(from_ngl('3str-2fofc.brix'), iso(1.5, GREEN, alpha=0.3))]),
	# Cube
	'cube-water': ("Water orbital (.cube), default visuals", lambda: get_volume(from_ngl('water.cube'))),
	'cube-benzene': ("Benzene HOMO (.cube), +/- isovalues", lambda: get_volume(
		from_ngl('benzene-homo.cube'), [iso(0.03, BLUE, kind='absolute', alpha=0.6), iso(-0.03, RED, kind='absolute', alpha=0.6)])),
	'cub': ("3EK3 2Fo-Fc with atoms (.cub)", lambda: get_volume(from_ngl('3ek3-2fofc.cub'), iso(1.5, BLUE, alpha=0.3))),
	# DX / DXBIN
	'dx': ("ESP (.dx), default visuals", lambda: [from_ngl('esp.mol'), get_volume(from_ngl('esp.dx'))]),
	'dx-gz': ("1CRN APBS potential (.dx.gz)", lambda: apbs_potential('1crn_apbs_pot.dx.gz')),
	'dxbin': ("1CRN APBS potential (.dxbin)", lambda: apbs_potential('1crn_apbs_pot.dxbin')),
	# DensityServer CIF, lazy loading and error handling
	'dscif': ("1TQN DensityServer CIF, 2 maps", density_server_maps),
	'lazy': ("1LEE lazy, load it from the Volume panel", lambda: [
		from_ngl('1lee.pdb'), get_volume(from_ngl('1lee.ccp4'), iso(1.5, BLUE, alpha=0.3), isLazy=True)]),
	'bad-index': ("volumeIndex out of range (console error expected)", lambda: get_volume(
		from_ngl('1lee_diff.ccp4'), iso(3, GREEN, volumeIndex=1))),
}


app = Dash(__name__)
app.layout = html.Div(
	[
		html.H3("Molstar Volume Test"),
		html.Div(
			[html.Button(label, id=f"btn-{key}", n_clicks=0) for key, (label, _) in SCENARIOS.items()],
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
	output=[Output("viewer", "data"), Output("status", "children")],
	inputs=[Input(f"btn-{key}", "n_clicks") for key in SCENARIOS],
	prevent_initial_call=True,
)
def run_volume_tests(*yes):
	label, make_data = SCENARIOS[ctx.triggered_id.removeprefix('btn-')]
	return make_data(), f"Loaded: {label}. Loading failures are logged to the browser console."


if __name__ == "__main__":
	app.run(debug=True)
