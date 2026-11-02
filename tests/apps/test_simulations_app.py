import hashlib
import json
from importlib.resources import files

from nomad_simulation_apps.apps import simulations_entry_point

EXPECTED_COLUMN_QUANTITIES = [
    'results.material.chemical_formula_hill',
    'results.method.simulation.program_name',
    'results.method.method_name',
    'results.method.simulation.dft.xc_functional_type',
    'upload_create_time',
    'authors',
    'results.method.simulation.precision.apw_cutoff',
    'results.method.simulation.precision.basis_set',
    'results.method.simulation.precision.k_line_density',
    'results.method.simulation.precision.native_tier',
    'results.method.simulation.precision.planewave_cutoff',
    'results.material.structural_type',
    'results.material.symmetry.crystal_system',
    'results.material.symmetry.space_group_symbol',
    'results.material.symmetry.space_group_number',
    'entry_name',
    'mainfile',
    'comment',
    'references',
    'datasets',
    'published',
]
EXPECTED_SELECTED_COLUMNS = EXPECTED_COLUMN_QUANTITIES[:6]
EXPECTED_MENU_TITLES = [
    'Material',
    'Elements / Formula',
    'Structure / Symmetry',
    'Method',
    'Precision',
    'DFT',
    'TB',
    'GW',
    'BSE',
    'DMFT',
    'Workflow',
    'Molecular dynamics',
    'Geometry Optimization',
    'Properties',
    'Electronic',
    'Vibrational',
    'Mechanical',
    'Author / Origin / Dataset',
    'Visibility / IDs / Schema',
]
EXPECTED_MENU_LEAF_COUNT = 80
EXPECTED_MENU_DIGEST = (
    'c1aa381363bdc2d382bc6201bb3dec85d633bda0a8895077696a65555de97825'
)
EXPECTED_WIDGETS = [
    ('periodic_table', 'results.material.elements'),
    ('terms', 'results.material.symmetry.space_group_symbol'),
    ('terms', 'results.material.structural_type'),
    ('terms', 'results.method.simulation.program_name'),
    ('terms', 'results.material.symmetry.crystal_system'),
]


def _get_menu_quantity(item: dict) -> str | None:
    value = item.get('search_quantity') or item.get('x')
    if isinstance(value, dict):
        return value.get('search_quantity')
    return value


def _get_menu_leaves(items: list[dict]) -> list[tuple[str, str]]:
    leaves = []
    for item in items:
        if item.get('items') is not None:
            leaves.extend(_get_menu_leaves(item['items']))
            continue
        quantity = _get_menu_quantity(item)
        if quantity:
            leaves.append((item['type'], quantity))
    return leaves


def test_simulations_entry_point_identity_and_scope():
    app = simulations_entry_point.app

    assert simulations_entry_point.name == 'Simulations'
    assert app.label == 'Simulations'
    assert app.path == 'calculations'
    assert app.resource == 'entries'
    assert app.category == 'Theory'
    assert app.description == 'Search simulations'
    assert app.filters_locked == {
        'quantities': 'results.method.simulation.program_name'
    }
    assert app.search_quantities.exclude == ['mainfile', 'entry_name', 'combine']


def test_simulations_columns_match_the_core_baseline():
    columns = simulations_entry_point.app.columns

    assert [column.search_quantity for column in columns] == (
        EXPECTED_COLUMN_QUANTITIES
    )
    assert [column.search_quantity for column in columns if column.selected] == (
        EXPECTED_SELECTED_COLUMNS
    )


def test_simulations_menu_matches_the_core_baseline():
    menu = simulations_entry_point.app.menu.model_dump(
        mode='json', exclude_none=True, warnings=False
    )
    leaves = _get_menu_leaves(menu['items'])
    digest = hashlib.sha256(
        json.dumps(leaves, separators=(',', ':')).encode()
    ).hexdigest()

    assert [item.get('title') for item in menu['items']] == EXPECTED_MENU_TITLES
    assert len(leaves) == EXPECTED_MENU_LEAF_COUNT
    assert digest == EXPECTED_MENU_DIGEST


def test_simulations_dashboard_matches_the_core_baseline():
    widgets = simulations_entry_point.app.dashboard.widgets

    assert [(widget.type, widget.search_quantity) for widget in widgets] == (
        EXPECTED_WIDGETS
    )


def test_simulations_config_uses_the_modern_app_schema():
    config_path = files('nomad_simulation_apps.apps').joinpath('simulations_app.json')
    with config_path.open('r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    assert 'filters' not in config
    assert 'filter_menus' not in config
    assert all('quantity' not in column for column in config['columns'])
    assert all(
        widget['type'] != 'periodictable' for widget in config['dashboard']['widgets']
    )
