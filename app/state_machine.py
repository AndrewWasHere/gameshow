"""
Copyright 2016, Andrew Lin
All rights reserved.

This software is licensed under the BSD 3-Clause License.
See LICENSE.txt at the root of the project or
https://opensource.org/licenses/BSD-3-Clause

State Machine ASCII Art:
                                 ZERO_SCORES : clear scores
                                           +--+
                                           |  |
                                           |  V
+----------+   REGISTER : remove teams   +------+
| Register |<----------------------------| Idle |--+ SET_SCORE :
|          |---------------------------->|      |<-+ update score
+----------+   PLAY                      +------+
    |  ^                                   ^  |
    |  |                   RESET_BUZZERS : |  | TRIGGERED :
    +--+                   clear triggered |  | set triggered
 TRIGGERED :                               |  V
 register name                         +-----------+
                       ZERO_SCORES :+--| Triggered |--+ SET_SCORE :
                       clear scores +->|           |<-+ update score
                                       +-----------+
"""
import flask

from app.gameshowdb import get_players, empty_players, Player


class Events:
    PLAY = 'play'
    REGISTER = 'register'
    RESET_BUZZERS = 'reset buzzers'
    SET_SCORE = 'set score'
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
        if event == Events.REGISTER:
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
        empty_players()
        parent.transition_to_state(RegisterState)

    @staticmethod
    def process_set_score_event(name, value):
        """Set player score.

        If value starts with '+', increment the score.
        If value starts with '-', decrement the score.
        Otherwise set the score to the value.

        Args:
            value (str)
        """
        players = get_players()
        if value.startswith('+'):
            players[name].score += int(value[1:])
        elif value.startswith('-'):
            players[name].score -= int(value[1:])
        else:
            players[name].score = int(value)

    @staticmethod
    def process_triggered_event(parent, name):
        players = get_players()
        players[name].triggered = True
        parent.transition_to_state(TriggeredState)

    @staticmethod
    def process_zero_scores_event():
        """Zero scores event handler."""
        players = get_players()
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

        elif event == Events.ZERO_SCORES:
            IdleState.process_zero_scores_event()

    @staticmethod
    def process_reset_buzzers_event(parent):
        """Reset buzzers event handler."""
        players = get_players()
        for p in players:
            players[p].triggered = False

        parent.transition_to_state(IdleState)


class RegisterState:
    NAME = 'register state'

    @classmethod
    def process(cls, parent, event, parameters):
        """Process event.

        Args:
            parent (StateMachine)
            event (str)
            parameters (dict)
        """
        if event == Events.PLAY:
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
        players = get_players()
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

    def process(self, event, parameters):
        """Process event"""
        self._state.process(self, event, parameters)

    def transition_to_state(self, new_state):
        """Transition to state.

        Args:
            new_state
        """
        self._state = new_state


def get_state_machine():
    """Get gameshow state machine"""
    if not hasattr(flask.g, 'gameshow_state'):
        flask.g.gameshow_state = StateMachine()

    return flask.g.gameshow_state