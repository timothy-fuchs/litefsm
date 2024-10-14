import unittest
from litefsm.fsm import FiniteStateMachine, FiniteStateMachineError


class TestFiniteStateMachine(FiniteStateMachine):
    """A concrete implementation of FiniteStateMachine for testing."""

    def __init__(self):
        super().__init__()


class TestFiniteStateMachineSuite(unittest.TestCase):
    def setUp(self):
        """Set up a simple FSM with 3 states."""
        self.fsm = TestFiniteStateMachine()

        # Register states
        self.state_A = self.fsm.register_state("A", is_initial=True)
        self.state_B = self.fsm.register_state("B")
        self.state_C = self.fsm.register_state("C", is_terminal=True)

        # Set state behavior for A
        @self.state_A.on_enter
        def on_enter_A(fsm):
            print("Entering State A")

        @self.state_A.on_state
        def on_state_A(fsm):
            print("In State A")
            fsm.set_state("B")

        @self.state_A.on_exit
        def on_exit_A(fsm):
            print("Exiting State A")

        # Set state behavior for B
        @self.state_B.on_enter
        def on_enter_B(fsm):
            print("Entering State B")

        @self.state_B.on_state
        def on_state_B(fsm):
            print("In State B")
            fsm.set_state("C")

        @self.state_B.on_exit
        def on_exit_B(fsm):
            print("Exiting State B")

        # Set state behavior for C (terminal state)
        @self.state_C.on_enter
        def on_enter_C(fsm):
            print("Entering State C")

        @self.state_C.on_state
        def on_state_C(fsm):
            print("In State C (Terminal)")

    def test_initial_state(self):
        """Test that the FSM starts in the initial state."""
        self.assertEqual(self.fsm._current_state, "A")

    def test_state_transitions(self):
        """Test that the FSM transitions between states correctly."""
        self.fsm.perform_one_step()  # A -> B
        self.assertEqual(self.fsm._current_state, "B")
        self.fsm.perform_one_step()  # B -> C
        self.assertEqual(self.fsm._current_state, "C")

    def test_terminal_state(self):
        """Test that the FSM correctly identifies when it's in a terminal state."""
        self.fsm.perform_one_step()  # A -> B
        self.fsm.perform_one_step()  # B -> C
        is_terminal = not self.fsm.perform_one_step()  # C is terminal
        self.assertTrue(is_terminal)

    def test_invalid_state_transition(self):
        """Test handling of transitions to an unregistered state."""
        with self.assertRaises(FiniteStateMachineError):
            self.fsm.set_state("InvalidState")

    def test_duplicate_initial_state(self):
        """Test that registering more than one initial state raises an error."""
        with self.assertRaises(FiniteStateMachineError):
            self.fsm.register_state("D", is_initial=True)

    def test_no_state_registered(self):
        """Test that executing a step with no states registered raises an error."""
        fsm_empty = TestFiniteStateMachine()
        with self.assertRaises(FiniteStateMachineError):
            fsm_empty.perform_one_step()

    def test_no_state_set(self):
        """Test that trying to perform a step without a current state raises an error."""
        fsm_empty = TestFiniteStateMachine()
        fsm_empty.register_state("A")
        with self.assertRaises(FiniteStateMachineError):
            fsm_empty.perform_one_step()

    def test_unhandled_on_state(self):
        """Test that missing 'on_state' callback raises an error."""
        self.state_B._on_state = None  # Remove on_state callback for B
        with self.assertRaises(FiniteStateMachineError):
            self.fsm.perform_one_step()  # A -> B
            self.fsm.perform_one_step()  # B should raise an error due to missing on_state


if __name__ == "__main__":
    unittest.main()
