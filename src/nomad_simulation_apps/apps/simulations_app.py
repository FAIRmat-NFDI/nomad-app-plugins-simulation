import json
from importlib.resources import files

from nomad.config.models.ui import App


def _load_simulations_app() -> App:
    config_path = files(__package__).joinpath('simulations_app.json')
    with config_path.open('r', encoding='utf-8') as config_file:
        return App.model_validate(json.load(config_file))


simulations_app = _load_simulations_app()
