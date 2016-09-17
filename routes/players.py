"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import flask

from app import gameshowdb
from app import state_machine

players = flask.Blueprint('players', __name__)


@players.route('/players')
def serve_players():
    """Serve players endpoint.

    This endpoint is used to get the players, their scores, and states.
    """
    p = {k: v.to_dict() for k, v in gameshowdb.get_players().items()}
    return flask.jsonify(p)


@players.route('/players/<player_id>', methods=['POST'])
def server_player_id(player_id):
    """Serve player ID endpoint.

    This endpoint is used to indicate a buzzer has been triggered.

    Args:
        player_id: Player identifier.
    """
    parameters = {'name': player_id}
    m = state_machine.get_state_machine()
    m.process(state_machine.Events.TRIGGERED, parameters)

    return ''


@players.route('/players/<player_id>/score', methods=['POST'])
def serve_player_id_score(player_id):
    """Serve player ID score endpoint.

    This endpoint is used to modify a player's score.

    Expects a JSON-encoded dict,

    {
        'value': <new_value>
    }

    or form data,

        'value': <new_value>

    where <new_value> is a string that resembles a signed or unsigned integer.
    If the value is signed, new_value is assumed to be a delta (e.g. +1, -1).
    If the value is unsigned, new_value is assumed to be an absolute value
    (e.g. 1, 10, 13) that supersedes the current player's score.

    Args:
        player_id: Player identifier.
    """
    request = flask.request
    parameters = (
        request.get_json()
        if request.json else
        {'value': request.form['value']}
    )
    parameters['name'] = player_id
    m = state_machine.get_state_machine()
    m.process(state_machine.Events.SET_SCORE, parameters)

    return ''
