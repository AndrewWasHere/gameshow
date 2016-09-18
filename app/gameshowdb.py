"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""


class Player:
    """Player data storage."""
    def __init__(self):
        self.score = 0
        self.triggered = False

    def to_dict(self):
        return {'score': self.score, 'triggered': self.triggered}

# global database. Yeah, I know...
# players = {}
players = {'Red_Icosahedron': Player()}


def get_players():
    """Return application instance of players.

    Returns:
        gameshowdb (defaultdict)
    """
    global players
    return players


def empty_players():
    """Reset application instance of gameshowdb."""
    global players
    players = {}
