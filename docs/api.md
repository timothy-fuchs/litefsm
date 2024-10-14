# API Reference for litefsm

## FiniteStateMachine

The `FiniteStateMachine` class is the base class for implementing finite state machines.

### Methods

#### `__init__(self)`
Initializes a new instance of the `FiniteStateMachine` class.

#### `register_state(self, state_name: str, is_terminal: bool = False, is_initial: bool = False) -> _State`
Registers a new state with the FSM.

- **Parameters**:
  - `state_name`: The name of the state.
  - `is_terminal`: If `True`, the state is terminal and cannot transition to another state.
  - `is_initial`: If `True`, this state will be the initial state of the FSM.

- **Returns**: The `_State` object for further configuration.

#### `set_state(self, state_name: str) -> None`
Sets the current state of the state machine.

- **Parameters**:
  - `state_name`: The name of the state to set as the current state.

- **Raises**: `FiniteStateMachineError` if the state is not registered.

#### `perform_one_step(self) -> bool`
Advances the state machine by one step.

- **Returns**: `True` if the state machine is not in a terminal state after performing this step, `False` otherwise.

- **Raises**: `FiniteStateMachineError` if no current state is set.

## _State Class

The `_State` class represents a single state in the FSM.

### Methods

#### `on_enter(self, func: Callable[["FiniteStateMachine"], None]) -> Callable`
Registers a callback to be called when entering the state.

#### `on_state(self, func: Callable[["FiniteStateMachine"], None]) -> Callable`
Registers a callback to be called while in the state.

#### `on_exit(self, func: Callable[["FiniteStateMachine"], None]) -> Callable`
Registers a callback to be called when exiting the state.

### Properties

#### `is_terminal`
Returns `True` if the state is terminal, `False` otherwise.

#### `name`
Returns the name of the state.
