"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import flask

from app import state_machine

proctor = flask.Blueprint('proctor', __name__)


@proctor.route('/proctor')
def control_panel():
    """Proctor control panel."""
    return flask.current_app.send_static_file('proctor.html')


@proctor.route('/proctor/zeroscores', methods=['POST'])
def zero_scores():
    """Reset scores."""
    gameshow = flask.current_app
    gameshow.state_machine.process(state_machine.Events.ZERO_SCORES)
    return ''


@proctor.route('/proctor/resetbuzzers', methods=['POST'])
def reset_buzzers():
    """Reset play buzzers."""
    gameshow = flask.current_app
    gameshow.state_machine.process(state_machine.Events.RESET_BUZZERS)
    return ''


@proctor.route('/proctor/gamestate', methods=['GET', 'POST'])
def toggle_gamestate():
    """Toggle between register buzzers and play."""
    gameshow = flask.current_app
    request = flask.request
    if request.method == 'POST':
        gameshow.state_machine.process(state_machine.Events.TOGGLE_GAMESTATE)

    return flask.jsonify({'state': gameshow.state_machine.state})
