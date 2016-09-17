"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

import pytest

from app import gameshowdb


def test_player():
    """Test Player object."""
    p = gameshowdb.Player()

    assert p.score == 0
    assert not p.triggered

    d = p.to_dict()

    assert isinstance(d, dict)
    assert d['score'] == 0
    assert not d['triggered']


@pytest.mark.skip(reason='hasattr mock not working as expected')
def test_get_players():
    """Test get_players()."""
    with mock.patch('app.state_machine.flask.g'):
        with mock.patch('builtins.hasattr', return_value=False):
            m = gameshowdb.get_players()

        assert isinstance(m, dict)

        m = gameshowdb.get_players()

        assert isinstance(m, dict)


def test_empty_players():
    """Test reset_gameshowdb()."""
    with mock.patch('app.gameshowdb.flask.g') as mock_global:
        gameshowdb.empty_players()

    assert isinstance(mock_global.gameshowdb, dict)