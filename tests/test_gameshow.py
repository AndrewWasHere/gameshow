"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import pytest

from app.gameshow import make_gameshow


@pytest.fixture
def app():
    """The whole gameshow app."""
    a = make_gameshow()
    return a.test_client()


def test_scoreboard(app):
    """Test / endpoint."""
    response = app.get('/')

    assert response.status_code == 200
    assert response.content_type.startswith('text/html')


def test_proctor(app):
    """Test /proctor endpoint."""
    response = app.get('/proctor')

    assert response.status_code == 200
    assert response.content_type.startswith('text/html')


def test_players(app):
    """Test /players endpoint."""