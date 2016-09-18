"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

from app import state_machine


def test_process_with_reset_buzzers_event():
    """Test process() with RESET_BUZZERS event."""
    mock_parent = mock.MagicMock()
    name = 'wormwood'
    value = 'math'
    event = state_machine.Events.RESET_BUZZERS
    parameters = {'name': name, 'value': value}

    with mock.patch(
        'app.state_machine.TriggeredState.process_reset_buzzers_event'
    ) as mock_process:
        state_machine.TriggeredState.process(mock_parent, event, parameters)

    assert mock_process.called_with(mock_parent)


def test_process_reset_buzzers_event():
    """Test process_reset_buzzers_event()."""
    mock_parent = mock.MagicMock()
    name = 'Toby'
    mock_named = mock.MagicMock(triggered=True)
    mock_players = {name: mock_named}

    with mock.patch(
        'app.state_machine.flask.current_app',
        players=mock_players
    ):
        state_machine.TriggeredState.process_reset_buzzers_event(mock_parent)

    assert not mock_named.triggered
    assert mock_parent.transition_to_state.called_with(state_machine.IdleState)


def test_process_with_set_score_event():
    """Test process() with SET_SCORE event."""
    mock_parent = mock.MagicMock()
    name = 'wormwood'
    value = 'math'
    event = state_machine.Events.SET_SCORE
    parameters = {'name': name, 'value': value}

    with mock.patch(
        'app.state_machine.IdleState.process_set_score_event'
    ) as mock_process:
        state_machine.TriggeredState.process(mock_parent, event, parameters)

    assert mock_process.called_with(mock_parent)


def test_process_with_zero_scores_event():
    """Test process() with ZERO_SCORES event."""
    mock_parent = mock.MagicMock()
    name = 'wormwood'
    value = 'math'
    event = state_machine.Events.ZERO_SCORES
    parameters = {'name': name, 'value': value}

    with mock.patch(
        'app.state_machine.IdleState.process_zero_scores_event'
    ) as mock_process:
        state_machine.TriggeredState.process(mock_parent, event, parameters)

    assert mock_process.called_with(mock_parent)


def test_process_with_other_events():
    """Test process() with unhandled events."""
    mock_parent = mock.MagicMock()
    name = 'wormwood'
    value = 'math'
    parameters = {'name': name, 'value': value}

    for event in (
        state_machine.Events.PLAY,
        state_machine.Events.TOGGLE_GAMESTATE,
        state_machine.Events.TRIGGERED,
    ):
        with mock.patch(
            'app.state_machine.TriggeredState.process_reset_buzzers_event'
        ) as mock_process:
            state_machine.TriggeredState.process(mock_parent, event, parameters)

        assert not mock_process.called
