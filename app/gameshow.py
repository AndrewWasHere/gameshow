"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import os

import flask

from app.state_machine import StateMachine
from routes.players import players
from routes.proctor import proctor
from routes.scoreboard import scoreboard
from routes.system import system


class GameShow(flask.Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.players = {}
        self.state_machine = StateMachine()

    def clear_players(self):
        self.players = {}


def make_gameshow():
    """Factory function for building a GameShow server."""
    d = os.path.dirname(__file__)
    app = GameShow(__name__, static_folder=os.path.join(d, '..', 'static'))
    app.register_blueprint(players)
    app.register_blueprint(proctor)
    app.register_blueprint(scoreboard)
    app.register_blueprint(system)

    return app
