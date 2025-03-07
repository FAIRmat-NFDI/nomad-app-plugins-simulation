from nomad.config.models.plugins import AppEntryPoint

from nomad_simulation_apps.apps.alexandria_app import alexandria_app

alexandria_entry_point = AppEntryPoint(
    name='Alexandria',
    description='Explore the data of the Alexandria database within NOMAD.',
    app=alexandria_app
)
