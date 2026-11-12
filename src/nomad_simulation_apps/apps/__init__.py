from nomad.config.models.plugins import AppEntryPoint

from nomad_simulation_apps.apps.alexandria_app import alexandria_app
from nomad_simulation_apps.apps.simulations_app import simulations_app

alexandria_entry_point = AppEntryPoint(
    name='Alexandria',
    description='Explore the data of the Alexandria database within NOMAD.',
    app=alexandria_app,
)

simulations_entry_point = AppEntryPoint(
    name='Simulations',
    description='Explore simulations within NOMAD.',
    app=simulations_app,
)
