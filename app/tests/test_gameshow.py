"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from app.gameshow import GameShow, make_gameshow
from app.state_machine import StateMachine


def test_gameshow():
    """Test GameShow."""
    app = GameShow(__name__)
    assert isinstance(app.players, dict)
    assert not app.players
    assert isinstance(app.state_machine, StateMachine)


def test_clear_players():
    """Test clear_players()."""
    app = GameShow(__name__)
    app.players['foo'] = 'bar'
    app.clear_players()

    assert isinstance(app.players, dict)
    assert not app.players


def test_make_gameshow():
    """Test gameshow factory."""
    app = make_gameshow()

    assert isinstance(app, GameShow)
