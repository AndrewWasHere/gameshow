"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
import flask


class Player:
    """Player data storage."""
    def __init__(self):
        self.score = 0
        self.triggered = False


def get_gameshowdb():
    """Return application instance of gameshowdb.

    Returns:
        gameshowdb (defaultdict)
    """
    if not hasattr(flask.g, 'gameshowdb'):
        flask.g.gameshowdb = {}

    return flask.g.gameshowdb


def reset_gameshowdb():
    """Reset application instance of gameshowdb."""
    flask.g.gameshowdb = {}
