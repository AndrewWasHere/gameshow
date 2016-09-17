"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import os

import flask
import pytest

from routes.proctor import proctor


@pytest.fixture
def app():
    d = os.path.dirname(__file__)
    app = flask.Flask(
        __name__,
        static_folder=os.path.join(d, '..', '..', 'static')
    )
    app.register_blueprint(proctor)
    return app.test_client()


def test_control_panel(app):
    """Test /proctor endpoint."""
    response = app.get('/proctor')

    assert response.status_code == 200
    assert response.content_type.startswith('text/html')