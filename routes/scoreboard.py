"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import flask


scoreboard = flask.Blueprint('scoreboard', __name__)


@scoreboard.route('/')
def show_scoreboard():
    """Scoreboard."""
    return flask.current_app.send_static_file('scoreboard.html')
