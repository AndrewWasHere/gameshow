"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause
"""
from unittest import mock

from app import state_machine


def test_process_with_register_event():
    """Test process() with REGISTER event."""
    parent = mock.MagicMock()
    event = state_machine.Events.REGISTER
    parameters = {}

    with mock.patch(
        'app.state_machine.IdleState.process_register_event'
    ) as mock_process:
        state_machine.IdleState.process(parent, event, parameters)

    assert mock_process.called_with(parent)


def test_process_register_event():
    """Test process_register_event."""
    parent = mock.MagicMock()

    with mock.patch(
        'app.state_machine.flask.current_app'
    ) as mock_reset:
        state_machine.IdleState.process_register_event(parent)

    assert mock_reset.clear_players.called
    assert parent.transition_to_state.called_with(state_machine.RegisterState)


def test_process_with_set_score_event():
    """Test process() with SET_SCORE event."""
    parent = mock.MagicMock()
    event = state_machine.Events.SET_SCORE
    name = 'calvin'
    value = 'value'
    parameters = {'name': name, 'value': value}

    with mock.patch(
        'app.state_machine.IdleState.process_set_score_event'
    ) as mock_process:
        state_machine.IdleState.process(parent, event, parameters)

    assert mock_process.called_with(name, value)


def test_process_set_score_event_add():
    """Test process_set_score_event()."""
    name = 'sheldon'
    value = '+1'
    starting_score = 0
    mock_named = mock.MagicMock(score=starting_score)
    mock_players = {name: mock_named}

    with mock.patch(
        'app.state_machine.flask.current_app',
        players=mock_players
    ):
        state_machine.IdleState.process_set_score_event(name, value)

    assert mock_named.score == starting_score + 1


def test_process_set_score_event_subtract():
    """Test process_set_score_event()."""
    name = 'arthur'
    value = '-1'
    starting_score = 0
    mock_named = mock.MagicMock(score=starting_score)
    mock_players = {name: mock_named}

    with mock.patch(
        'app.state_machine.flask.current_app',
        players=mock_players
    ):
        state_machine.IdleState.process_set_score_event(name, value)

    assert mock_named.score == starting_score - 1


def test_process_set_score_event_value():
    """Test process_set_score_event()."""
    name = 'flaco'
    value = '42'
    starting_score = 0
    mock_named = mock.MagicMock(score=starting_score)
    mock_players = {name: mock_named}

    with mock.patch(
        'app.state_machine.flask.current_app',
        players=mock_players
    ):
        state_machine.IdleState.process_set_score_event(name, value)

    assert mock_named.score == int(value)


def test_process_with_triggered_event():
    """Test process() with TRIGGERED event."""
    mock_parent = mock.MagicMock()
    event = state_machine.Events.TRIGGERED
    name = 'hobbes'
    value = 'value'
    parameters = {'name': name, 'value': value}

    with mock.patch(
        'app.state_machine.IdleState.process_triggered_event'
    ) as mock_process:
        state_machine.IdleState.process(mock_parent, event, parameters)

    assert mock_process.called_with(mock_parent, name)


def test_process_triggered_event():
    """Test process_triggered_event()."""
    mock_parent = mock.MagicMock()
    name = 'Joel'
    mock_named = mock.MagicMock(triggered=False)
    mock_players = {name: mock_named}

    with mock.patch(
        'app.state_machine.flask.current_app',
        players=mock_players
    ):
        state_machine.IdleState.process_triggered_event(mock_parent, name)

    assert mock_named.triggered
    assert mock_parent.transition_to_state.called_with(
        state_machine.TriggeredState
    )


def test_process_with_zero_scores_event():
    """Test process() with ZERO SCORES event."""
    mock_parent = mock.MagicMock()
    event = state_machine.Events.ZERO_SCORES
    name = 'suzy'
    value = 'derkins'
    parameters = {'name': name, 'value': value}

    with mock.patch(
        'app.state_machine.IdleState.process_zero_scores_event'
    ) as mock_process:
        state_machine.IdleState.process(mock_parent, event, parameters)

    assert mock_process.called_with()


def test_process_zero_scores_event():
    """Test process_zero_scores_event()"""
    name = 'Walt'
    mock_named = mock.MagicMock(score=42)
    mock_players = {name: mock_named}

    with mock.patch(
        'app.state_machine.flask.current_app',
        players=mock_players
    ):
        state_machine.IdleState.process_zero_scores_event()

    assert mock_named.score == 0


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
            'app.state_machine.IdleState.process_register_event'
        ) as mock_pre, mock.patch(
            'app.state_machine.IdleState.process_set_score_event'
        ) as mock_pss,mock.patch(
            'app.state_machine.IdleState.process_triggered_event'
        ) as mock_pte,mock.patch(
            'app.state_machine.IdleState.process_zero_scores_event'
        ) as mock_pze:
            state_machine.IdleState.process(mock_parent, event, parameters)

        assert not all(
            (mock_pre.called, mock_pss.called, mock_pte.called, mock_pze.called)
        )
