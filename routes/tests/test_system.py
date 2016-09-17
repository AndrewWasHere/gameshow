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

from routes.system import system


@pytest.fixture
def app():
    d = os.path.dirname(__file__)
    app = flask.Flask(
        __name__,
        static_folder=os.path.join(d, '..', '..', 'static')
    )
    app.register_blueprint(system)
    return app.test_client()


@pytest.mark.skip
def test_serve_angular(app):
    response = app.get('/node_modules/angular/angular.min.js')

    assert response.status_code == 200

@pytest.mark.skip
def test_serve_javascript(app):
    response = app.get('/js/todo.js')

    assert response.status_code == 200
