"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

import pytest

from app import player


def test_player():
    """Test Player object."""
    p = player.Player()

    assert p.score == 0
    assert not p.triggered

    d = p.to_dict()

    assert isinstance(d, dict)
    assert d['score'] == 0
    assert not d['triggered']
