
def test_importing_alexandria():
    # this will raise an exception if pydantic model validation fails for the app
    from nomad_simulation_apps.apps import alexandria_entry_point

    assert alexandria_entry_point.app.label == 'Alexandria'
