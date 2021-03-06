"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import json
from unittest import mock

import flask
import pytest

from app import state_machine
from app.gameshow import GameShow
from routes.players import players


@pytest.fixture
def app():
    app = GameShow(__name__)
    app.register_blueprint(players)
    return app.test_client()


def test_serve_players(app):
    """Test /players endpoint."""
    response = app.get('/players')

    assert response.mimetype == 'application/json'
    assert response.status_code == 200

    data = response.get_data(True)
    data = json.loads(data)

    assert isinstance(data, list)


def test_serve_player_id(app):
    """Test /players/<player_id> endpoint."""
    player = 'Harv'
    with mock.patch(
        'routes.players.flask.current_app'
    ) as mock_gameshow:
        response = app.post('/players/{}'.format(player))

    assert mock_gameshow.statemachine.process.called_with(
        state_machine.Events.TRIGGERED,
        {'name': player}
    )
    assert response.status_code == 200


def test_serve_player_id_score_form_data(app):
    """Test /players/<player_id>/score endpoint."""
    player = 'Cheryl'
    score = '42'
    parameters = {'name': player, 'value': score}
    with mock.patch(
        'routes.players.flask.current_app'
    ) as mock_gameshow:
        response = app.post(
            '/players/{}/score'.format(player),
            data={'value': score}
        )

    assert mock_gameshow.statemachine.process.called_with(
        state_machine.Events.SET_SCORE,
        parameters
    )
    assert response.status_code == 200


def test_serve_player_id_score_json(app):
    """Test /players/<player_id>/score endpoint."""
    player = 'Cheryl'
    score = '42'
    parameters = {'name': player, 'value': score}
    with mock.patch(
        'routes.players.flask.current_app'
    ) as mock_gameshow:
        response = app.post(
            '/players/{}/score'.format(player),
            data=json.dumps({'value': score}),
            content_type='application/json'
        )

    assert mock_gameshow.statemachine.process.called_with(
        state_machine.Events.SET_SCORE,
        parameters
    )
    assert response.status_code == 200
