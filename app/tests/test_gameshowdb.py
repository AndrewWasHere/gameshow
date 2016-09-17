"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

from app import gameshowdb


def test_player():
    """Test Player object."""
    p = gameshowdb.Player()

    assert p.score == 0
    assert not p.triggered


# The mock of hasattr isn't working as expected...
# def test_get_gameshowdb():
#     """Test get_gameshowdb()."""
#     with mock.patch(
#         'app.state_machine.flask.g'
#     ):
#         with mock.patch('builtins.hasattr', return_value=False):
#             m = gameshowdb.get_gameshowdb()
#
#         assert isinstance(m, dict)
#
#         m = gameshowdb.get_gameshowdb()
#
#         assert isinstance(m, dict)


def test_reset_gameshowdb():
    """Test reset_gameshowdb()."""
    with mock.patch(
        'app.gameshowdb.flask.g'
    ) as mock_global:
        gameshowdb.reset_gameshowdb()

    assert isinstance(mock_global.gameshowdb, dict)