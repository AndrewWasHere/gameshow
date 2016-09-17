"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

import pytest

from app import state_machine


def test_state():
    """Test state property and transition_to_state()."""
    m = state_machine.StateMachine()

    assert m.state == state_machine.IdleState.NAME

    for s in [
        state_machine.IdleState,
        state_machine.RegisterState,
        state_machine.TriggeredState
    ]:
        m.transition_to_state(s)

        assert m.state == s.NAME


def test_process():
    """Test process()."""
    mock_idle = mock.MagicMock()
    mock_register = mock.MagicMock()

    m = state_machine.StateMachine()
    for s in [mock_idle, mock_register]:
        m.transition_to_state(s)

        event = 'event'
        parameters = 'parameters'
        m.process(event, parameters)

        assert s.process.called_with(event, parameters)


@pytest.mark.skip(reason='hasattr mock not working as expected.')
def test_get_state_machine():
    """Test get_state_machine()."""
    with mock.patch(
        'app.state_machine.flask.g'
    ):
        with mock.patch('builtins.hasattr', return_value=False):
            m = state_machine.get_state_machine()

        assert isinstance(m, state_machine.StateMachine)

        m = state_machine.get_state_machine()

        assert isinstance(m, state_machine.StateMachine)
