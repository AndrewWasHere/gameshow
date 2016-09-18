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


@proctor.route('/proctor/zeroscores')
def zero_scores():
    """Reset scores."""
    gameshow = flask.current_app
    gameshow.statemachine.process(state_machine.Events.ZERO_SCORES)


@proctor.route('/proctor/register')
def register():
    """Register buzzers."""
    gameshow = flask.current_app
    gameshow.statemachine.process(state_machine.Events.REGISTER)


@proctor.route('/proctor/play')
def play():
    """Play game show."""
    gameshow = flask.current_app
    gameshow.statemachine.process(state_machine.Events.PLAY)
