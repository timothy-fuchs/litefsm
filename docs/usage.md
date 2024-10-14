# Usage Guide for litefsm

## Getting Started

To get started with `litefsm`, first install it using pip:

```bash
pip install litefsm
```

## Basic Example

Here’s a simple example demonstrating how to use `litefsm` to create a finite state machine.

```python
from litefsm import FiniteStateMachine

class MyFSM(FiniteStateMachine):
    def __init__(self):
        super().__init__()

        # Register states
        state_A = self.register_state("A", is_initial=True)
        state_B = self.register_state("B")
        state_C = self.register_state("C", is_terminal=True)

        @state_A.on_enter
        def on_enter_A(fsm):
            print("Entering State A")

        @state_A.on_state
        def on_state_A(fsm):
            print("In State A")
            fsm.set_state("B")

        @state_B.on_enter
        def on_enter_B(fsm):
            print("Entering State B")

        @state_B.on_state
        def on_state_B(fsm):
            print("In State B")
            fsm.set_state("C")

        @state_C.on_enter
        def on_enter_C(fsm):
            print("Entering State C")

# Create an instance of MyFSM
fsm = MyFSM()

# Perform steps until a terminal state is reached
while fsm.perform_one_step():
    pass
```

## State Callbacks

You can define three types of callbacks for each state:
- **on_enter**: Called when entering the state.
- **on_state**: Called while in the state. This method should be defined to handle state transitions.
- **on_exit**: Called when exiting the state.

Each callback should accept a single parameter, which is the instance of the `FiniteStateMachine`.

For example:
```python
@state.on_enter
def on_enter(fsm):
    # Code to execute when entering the state

@state.on_state
def on_state(fsm):
    # Code to execute while in the state
    fsm.set_state("NextState")

@state.on_exit
def on_exit(fsm):
    # Code to execute when exiting the state
```

## Error Handling

If you attempt to perform actions that are not allowed (e.g., transitioning to an unregistered state), a `FiniteStateMachineError` will be raised. Make sure to handle this exception in your code.

```python
try:
    fsm.set_state("InvalidState")
except FiniteStateMachineError as e:
    print(e)
```

For more advanced usage and customization options, refer to the API documentation below.
