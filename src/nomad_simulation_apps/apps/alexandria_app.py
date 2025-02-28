import os

import yaml
from nomad.config.models.ui import (
    App,
    Column,
    Dashboard,
    Menu,
    MenuItemHistogram,
    MenuItemOptimade,
    MenuItemPeriodicTable,
    MenuItemTerms,
    MenuSizeEnum,
)

try:
    with open(os.path.join(os.path.dirname(__file__), 
                           'alexandria_dashboard.yaml')) as widget_file:
        widgets = yaml.safe_load(widget_file)
except Exception as e:
    raise RuntimeError(f'Failed to load widgets from YAML file: {e}')


alexandria_app = App(
    label='Alexandria',
    path='alexandria',
    category='Theory',
    description='Search the Alexandria database',
    readme='''This page presents the data of the [Alexandria database](https://alexandria.icams.rub.de/). The search results at the bottom of this page contain only the final relaxed geometries. The results of the structure relaxation can be found by clicking on the VASP mainfiles in the "FILES" tab of each entry.  
    **Please note** that the upload of the data is currently ongoing and therefore not all data are available. ''',  # noqa: E501
    columns=[
        Column(
            label='Formula',
            quantity='results.material.chemical_formula_hill',
            selected=True
        ),
        Column(
            label='Space group',
            quantity='results.material.symmetry.space_group_number',
            selected=True
        ),
        Column(
            label='XC functional',
            quantity='results.method.simulation.dft.xc_functional_names',
            selected=True
        ),
        Column(
            label='Band gap',
            quantity='min(results.properties.electronic.band_gap[*].value)', #jmes path
            selected=True
        )
    ],
    filters_locked = {
        "datasets.dataset_name": [
            "Alexandria PBE",
            "Alexandria PBEsol"
            ],
        "entry_type": [
            "VASP DFT SinglePoint"
            ]
    },
    menu=Menu(
        items=[
            Menu(
                size=MenuSizeEnum.XXL,
                title='Elements / Formula',
                items=[
                    MenuItemPeriodicTable(
                        search_quantity='results.material.elements',
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_hill',
                        width=6,
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_iupac',
                        width=6,
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_reduced',
                        width=6,
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_anonymous',
                        width=6,
                        options=0,
                    ),
                    MenuItemHistogram(
                        x='results.material.n_elements',
                    ),
                ]
            ),
            Menu(
                title = 'Structure / Symmetry',
                items=[
                    MenuItemTerms(
                        search_quantity='results.material.symmetry.bravais_lattice',
                        n_columns=2,
                        show_input=False,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.symmetry.crystal_system',
                        n_columns=2,
                        show_input=False,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.symmetry.space_group_symbol',
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.symmetry.structure_name',
                        options=5,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.symmetry.strukturbericht_designation',
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.symmetry.point_group',
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.symmetry.hall_symbol',
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.symmetry.prototype_aflow_id',
                        options=0,
                    ),
                ]
            ),
            Menu(
                title = 'Method',
                items=[
                    MenuItemTerms(
                        search_quantity='results.method.simulation.program_version',
                        options=5,
                        show_input=False,
                    ),
                    MenuItemHistogram(
                        x='results.method.simulation.precision.k_line_density',
                    ),
                    MenuItemTerms(
                        search_quantity='results.method.simulation.precision.native_tier',
                        options=2,
                    ),
                    MenuItemTerms(
                        search_quantity='results.method.simulation.dft.xc_functional_type',
                        show_input=False,
                    ),
                    MenuItemTerms(
                        search_quantity='results.method.simulation.dft.xc_functional_names',
                    ),
                    MenuItemHistogram(
                        x='results.method.simulation.dft.hubbard_kanamori_model.u_effective',
                    ),
                ]
            ),
            Menu(
                title='Band gap',
                items=[
                    MenuItemHistogram(
                        x='results.properties.electronic.band_gap.value',
                        scale='log',
                        autorange=True,
                        n_bins=30,
                        show_input=True
                    ),
                ]
            ),
            Menu(
                title = 'IDs',
                items=[
                    MenuItemTerms(
                        search_quantity='entry_id',
                        options=0,
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.material_id',
                        options=0,
                    ),                    
                ]
            ),
            Menu(
                title = 'Optimade',
                items=[MenuItemOptimade()]
            ),
        ]
        ),
    dashboard=Dashboard.parse_obj(widgets),
)