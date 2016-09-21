"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause

@startuml

[*] --> Idle

Idle --> Idle : SET SCORE | [update score]
Idle --> Idle : ZERO SCORES | [clear scores]
Idle --> Register : TOGGLE GAMESTATE | [remove teams]
Idle --> Triggered : TRIGGERED | [set triggered]

Register --> Register : TRIGGERED | [register name]
Register --> Idle : TOGGLE GAMESTATE

Triggered --> Idle : RESET BUZZERS | [clear triggered]
Triggered --> Register : TOGGLE GAMESTATE
Triggered --> Triggered : SET SCORE | [update score]
Triggered --> Triggered : ZERO SCORE | [clear scores]

@enduml
"""
import flask

from app.player import Player


class Events:
    RESET_BUZZERS = 'reset buzzers'
    SET_SCORE = 'set score'
    TOGGLE_GAMESTATE = 'toggle gamestate'
    TRIGGERED = 'triggered'
    ZERO_SCORES = 'zero scores'


class IdleState:
    NAME = 'idle state'

    @classmethod
    def process(cls, parent, event, parameters):
        """Process event.

        Args:
            parent (StateMachine)
            event (str)
            parameters (dict)
        """
        if event == Events.TOGGLE_GAMESTATE:
            cls.process_register_event(parent)

        elif event == Events.SET_SCORE:
            cls.process_set_score_event(
                parameters['name'],
                parameters['value']
            )
            pass

        elif event == Events.TRIGGERED:
            cls.process_triggered_event(parent, parameters['name'])

        elif event == Events.ZERO_SCORES:
            cls.process_zero_scores_event()

    @staticmethod
    def process_register_event(parent):
        """Register event handler."""
        gameshow = flask.current_app
        gameshow.clear_players()

        parent.transition_to_state(RegisterState)

    @staticmethod
    def process_set_score_event(name, value):
        """Set player score.

        If value starts with '+', increment the score.
        If value starts with '-', decrement the score.
        Otherwise set the score to the value.

        Args:
            name (str)
            value (str)
        """
        gameshow = flask.current_app
        players = gameshow.players
        if value.startswith('+'):
            players[name].score += int(value[1:])
        elif value.startswith('-'):
            players[name].score -= int(value[1:])
        else:
            players[name].score = int(value)

    @staticmethod
    def process_triggered_event(parent, name):
        gameshow = flask.current_app
        players = gameshow.players
        players[name].triggered = True
        parent.transition_to_state(TriggeredState)

    @staticmethod
    def process_zero_scores_event():
        """Zero scores event handler."""
        gameshow = flask.current_app
        players = gameshow.players
        for p in players:
            players[p].score = 0


class TriggeredState:
    NAME = 'triggered state'

    @classmethod
    def process(cls, parent, event, parameters):
        """Process event.

        Args:
            parent (StateMachine)
            event (str)
            parameters (dict)
        """
        if event == Events.RESET_BUZZERS:
            cls.process_reset_buzzers_event(parent)

        elif event == Events.SET_SCORE:
            IdleState.process_set_score_event(
                parameters['name'],
                parameters['value']
            )

        elif event == Events.TRIGGERED:
            cls.process_triggered_event(parameters['name'])

        elif event == Events.ZERO_SCORES:
            IdleState.process_zero_scores_event()

        elif event == Events.TOGGLE_GAMESTATE:
            IdleState.process_register_event(parent)

    @staticmethod
    def process_reset_buzzers_event(parent):
        """Reset buzzers event handler."""
        gameshow = flask.current_app
        players = gameshow.players
        for p in players:
            players[p].triggered = False
            players[p].notified = False

        parent.transition_to_state(IdleState)

    @staticmethod
    def process_triggered_event(name):
        """Triggered event."""
        gameshow = flask.current_app
        players = gameshow.players
        players[name].notified = True


class RegisterState:
    NAME = 'register'

    @classmethod
    def process(cls, parent, event, parameters):
        """Process event.

        Args:
            parent (StateMachine)
            event (str)
            parameters (dict)
        """
        if event == Events.TOGGLE_GAMESTATE:
            cls.process_play_event(parent)

        elif event == Events.TRIGGERED:
            cls.process_triggered_event(parameters['name'])

    @staticmethod
    def process_play_event(parent):
        """Play event handler."""
        parent.transition_to_state(IdleState)

    @staticmethod
    def process_triggered_event(name):
        """Triggered event handler."""
        gameshow = flask.current_app
        players = gameshow.players
        if name in players:
            raise ValueError('{} already registered.'.format(name))

        players[name] = Player()


class StateMachine:
    """Gameshow state machine."""
    def __init__(self):
        self._state = IdleState

    @property
    def state(self):
        """Current state."""
        return self._state.NAME

    def process(self, event, parameters=None):
        """Process event"""
        self._state.process(self, event, parameters)

    def transition_to_state(self, new_state):
        """Transition to state.

        Args:
            new_state
        """
        self._state = new_state
