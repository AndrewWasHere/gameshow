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


def test_process_with_play_event():
    """Test process() with PLAY event."""
    mock_parent = mock.MagicMock()
    name = 'wormwood'
    value = 'math'
    event = state_machine.Events.PLAY
    parameters = {'name': name, 'value': value}

    with mock.patch(
        'app.state_machine.RegisterState.process_play_event'
    ) as mock_process:
        state_machine.RegisterState.process(mock_parent, event, parameters)

    assert mock_process.called_with(mock_parent)


def test_process_play_event():
    """Test process_play_event()."""
    mock_parent = mock.MagicMock()

    state_machine.RegisterState.process_play_event(mock_parent)

    assert mock_parent.transition_to_state.called_with(state_machine.IdleState)


def test_process_with_triggered_event():
    """Test process() with TRIGGERED event."""
    mock_parent = mock.MagicMock()
    name = 'wormwood'
    value = 'math'
    event = state_machine.Events.TRIGGERED
    parameters = {'name': name, 'value': value}

    with mock.patch(
        'app.state_machine.RegisterState.process_triggered_event'
    ) as mock_process:
        state_machine.RegisterState.process(mock_parent, event, parameters)

    assert mock_process.called_with(mock_parent)


def test_process_triggered_event_already_registered():
    """Test process_triggered_event()."""
    name = 'Joules'
    mock_players = {name: None}
    with mock.patch(
        'app.state_machine.get_gameshowdb',
        return_value=mock_players
    ) as mock_get, pytest.raises(ValueError):
        state_machine.RegisterState.process_triggered_event(name)

    assert mock_get.called


def test_process_triggered_event_not_registered():
    """Test process_triggered_event()."""
    name = 'Joules'
    mock_players = {}
    with mock.patch(
        'app.state_machine.get_gameshowdb',
        return_value=mock_players
    ) as mock_get:
        state_machine.RegisterState.process_triggered_event(name)

    assert mock_get.called
    assert name in mock_players


def test_process_with_other_events():
    """Test process() with unhandled events."""
    mock_parent = mock.MagicMock()
    name = 'wormwood'
    value = 'math'
    parameters = {'name': name, 'value': value}

    for event in (
        state_machine.Events.PLAY,
        state_machine.Events.RESET_BUZZERS
    ):
        with mock.patch(
            'app.state_machine.RegisterState.process_play_event'
        ) as mock_play, mock.patch(
            'app.state_machine.RegisterState.process_triggered_event'
        ) as mock_triggered:
            state_machine.RegisterState.process(mock_parent, event, parameters)

        assert not all(
            (mock_play.called, mock_triggered.called)
        )
