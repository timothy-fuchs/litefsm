
# LiteFSM

LiteFSM is a lightweight Python library for implementing finite state machines (FSMs). It is simple to use and extend, making it suitable for various applications that require state management.

## Features

- Register and manage states with optional entry, execution, and exit behaviours.
- Define terminal states for FSMs with automatic transitions.
- Handle state transitions with custom logic.
- Simple API for building, running, and managing FSMs.

## Installation

To install LiteFSM, simply clone the repository and use it in your project:

```bash
git clone https://github.com/yourusername/litefsm.git
```

## Usage

### Creating an FSM

1. Define the states and their transitions using the `register_state` method.
2. Implement a mandatory `on_state` callback and optional `on_enter` and `on_exit` callbacks for each state.

```python
from litefsm import FiniteStateMachine

class MyFSM(FiniteStateMachine):
    def __init__(self):
        super().__init__()
        self._setup_states()

    def _setup_states(self):
        idle = self.register_state("Idle", is_initial=True)
        processing = self.register_state("Processing")
        completed = self.register_state("Completed", is_terminal=True)

        # Register state behaviours
        @idle.on_enter
        def on_idle_enter(fsm):
            print("Entering Idle state.")

        @idle.on_state
        def on_idle(fsm):
            print("Currently Idle.")
            fsm.set_state("Processing")  # Transition to Processing

        @processing.on_enter
        def on_processing_enter(fsm):
            print("Starting Processing.")

        @processing.on_state
        def on_processing(fsm):
            print("Processing data...")
            fsm.set_state("Completed")  # Transition to Completed

        @completed.on_enter
        def on_completed_enter(fsm):
            print("Process completed.")
```

### Running the FSM

```python
fsm = MyFSM()
while fsm.perform_one_step():
    pass  # This runs the FSM until it reaches a terminal state
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
