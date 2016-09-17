"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import os

import flask

from routes.players import players
from routes.proctor import proctor
from routes.scoreboard import scoreboard
from routes.system import system


def make_gameshow():
    d = os.path.dirname(__file__)
    app = flask.Flask(__name__, static_folder=os.path.join(d, '..', 'static'))
    app.register_blueprint(players)
    app.register_blueprint(proctor)
    app.register_blueprint(scoreboard)
    app.register_blueprint(system)

    return app
