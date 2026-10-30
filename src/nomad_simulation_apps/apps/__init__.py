from nomad.config.models.plugins import AppEntryPoint

from nomad_simulation_apps.apps.alexandria_app import alexandria_app
from nomad_simulation_apps.apps.calculations_app import calculations_app

alexandria_entry_point = AppEntryPoint(
    name='Alexandria',
    description='Explore the data of the Alexandria database within NOMAD.',
    app=alexandria_app,
)

calculations_entry_point = AppEntryPoint(
    name='Calculations',
    description='Explore simulation calculations within NOMAD.',
    app=calculations_app,
)
