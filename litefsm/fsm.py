# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2024 Timothy Fuchs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------


from abc import ABC
from typing import Callable


class _State:
    def __init__(self, name: str, is_terminal: bool):
        self._name = name
        self._on_enter: Callable[["FiniteStateMachine"], None] | None = None
        self._on_state: Callable[["FiniteStateMachine"], None] | None = None
        self._on_exit: Callable[["FiniteStateMachine"], None] | None = None
        self._is_terminal = is_terminal

    @property
    def is_terminal(self) -> bool:
        return self._is_terminal

    @property
    def name(self):
        return self._name

    # Method to register on_enter
    def on_enter(self, func: Callable[["FiniteStateMachine"], None]) -> Callable:
        self._on_enter = func
        return func

    # Method to register on_state
    def on_state(self, func: Callable[["FiniteStateMachine"], None]) -> Callable:
        self._on_state = func
        return func

    # Method to register on_exit
    def on_exit(self, func: Callable[["FiniteStateMachine"], None]) -> Callable:
        self._on_exit = func
        return func

    def perform_on_enter(self, fsm: "FiniteStateMachine"):
        if self._on_enter:
            self._on_enter(fsm)

    def perform_on_state(self, fsm: "FiniteStateMachine"):
        if not self._on_state:
            raise FiniteStateMachineError(
                f"State '{self._name}' does not have a mandatory 'on_state()' method."
            )
        self._on_state(fsm)

    def perform_on_exit(self, fsm: "FiniteStateMachine"):
        if self._on_exit:
            self._on_exit(fsm)


class FiniteStateMachineError(Exception):
    pass


class FiniteStateMachine(ABC):
    """Base class for a finite state machine."""

    def __init__(self):
        self._states = {}
        self._current_state = None
        self._state_changed = False

    def register_state(
        self, state_name: str, is_terminal: bool = False, is_initial=False
    ) -> _State:
        """Register a state with the FSM.
        Return the _State object for further configuration"""
        state = _State(state_name, is_terminal)
        self._states[state_name] = state
        if is_initial:
            if self._current_state is not None:
                raise FiniteStateMachineError("Initial state already set.")
            self.set_state(state_name)
        return state

    def _execute_state(self, state_name: str):
        state = self._states.get(state_name)
        if not state:
            raise FiniteStateMachineError(f"State '{state_name}' is not registered.")
        if self._state_changed:
            state.perform_on_enter(self)
            self._state_changed = False
        if not self._state_changed:
            state.perform_on_state(self)
        if self._state_changed:
            state.perform_on_exit(self)
        return not state.is_terminal

    def set_state(self, state_name: str) -> None:
        """Sets the current state of the state machine."""
        if state_name not in self._states:
            raise FiniteStateMachineError(f"State '{state_name}' is not registered.")
        self._current_state = state_name
        self._state_changed = True

    def perform_one_step(self) -> bool:
        """Advances the state machine by one step.
        Returns True if the state machine is not in a terminal state
        after performing this step, False otherwise."""
        if not self._current_state:
            raise FiniteStateMachineError("No current state set.")
        return self._execute_state(self._current_state)
