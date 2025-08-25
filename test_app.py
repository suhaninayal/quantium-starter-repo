# test_app.py
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()  # ensure chromedriver is available

import pytest
from dash.testing.application_runners import import_app

def get_all_ids(layout):
    """Recursively collect all component IDs from Dash layout."""
    ids = set()
    if hasattr(layout, "id") and layout.id:
        ids.add(layout.id)
    if hasattr(layout, "children") and layout.children:
        children = layout.children
        if isinstance(children, list):
            for child in children:
                ids.update(get_all_ids(child))
        else:
            ids.update(get_all_ids(children))
    return ids

def test_all_components_present(dash_duo):
    """Check if all components with IDs are rendered."""
    app = import_app("app")  # replace "app" with your app file name
    dash_duo.start_server(app)

    all_ids = get_all_ids(app.layout)

    for comp_id in all_ids:
        element = dash_duo.wait_for_element(f"#{comp_id}")
        assert element is not None, f"Component with id '{comp_id}' not found"
