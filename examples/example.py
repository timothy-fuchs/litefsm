# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2024 Timothy Fuchs
# -----------------------------------------------------------------------------

import time

from litefsm.fsm import FiniteStateMachine


class MicrowaveOvenStateMachine(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__()

        self._event_timestamp: int | None = None
        self._cooking_time: int = 0
        self._is_closed = True
        self._cook_button_pressed = False
        self._beeps_counter = 0

        st_init = self.register_state("ST_INIT", is_initial=True)
        st_opened = self.register_state("ST_OPENED")
        st_closed = self.register_state("ST_CLOSED")
        st_cooking = self.register_state("ST_COOKING")
        st_beeping_done = self.register_state("ST_BEEPING_DONE")
        st_stop = self.register_state("ST_STOP", is_terminal=True)

        @st_init.on_enter
        def on_enter_init(self):
            print("Initializing the microwave oven state machine...")
            self._cooking_time = 0
            self._is_closed = True
            self._cook_button_pressed = False
            self._beeps_counter = 0

        @st_init.on_state
        def on_state_init(self):
            if self._is_closed:
                self.set_state("ST_CLOSED")
            else:
                self.set_state("ST_OPENED")

        @st_opened.on_enter
        def on_enter_opened(_self):
            print("The microwave oven is opened...")

        @st_opened.on_state
        def on_state_opened(self):
            self._cook_button_pressed = False
            if self._is_closed:
                self.set_state("ST_CLOSED")

        @st_opened.on_exit
        def on_exit_opened(_self):
            print("User closes the microwave oven...")

        @st_closed.on_enter
        def on_enter_closed(self):
            print("The microwave oven is closed...")
            self._cook_button_pressed = False

        @st_closed.on_state
        def on_state_closed(self):
            if not self._is_closed:
                self.set_state("ST_OPENED")
            elif self._cook_button_pressed:
                if self._cooking_time > 0:
                    self.set_state("ST_COOKING")
                else:
                    self._cook_button_pressed = False

        @st_closed.on_exit
        def on_exit_closed(self):
            self._cook_button_pressed = False

        @st_cooking.on_enter
        def on_enter_cooking(self):
            print("The microwave oven starts cooking...")
            self._update_timestamp()

        @st_cooking.on_state
        def on_state_cooking(self):
            if not self._is_closed:
                self.set_state("ST_OPENED")
                return
            if self._has_elapsed(1):
                self._update_timestamp()
                self._cooking_time -= 1
                if self._cooking_time <= 0:
                    self._cooking_time = 0
                    self.set_state("ST_BEEPING_DONE")
                    return
                print(f"Cooking... {self._cooking_time} seconds left.")

        @st_cooking.on_exit
        def on_exit_cooking(_self):
            print("Microwave oven stops cooking...")

        @st_beeping_done.on_enter
        def on_enter_beeping_done(_self):
            self._beeps_counter = 0
            self._update_timestamp()

        @st_beeping_done.on_state
        def on_state_beeping_done(self):
            if self._has_elapsed(1):
                self._beeps_counter += 1
                if self._beeps_counter >= 3:
                    self.set_state("ST_STOP")
                self._update_timestamp()
                print("<Beep!>")

        @st_beeping_done.on_exit
        def on_exit_beeping_done(_self):
            self._beeps_counter = 0
            print("Microwave oven stops beeping...")

        @st_stop.on_state
        def on_state_stop(_self):
            print("Microwave oven FSM is in the terminal state...")

    def _get_timestamp(self):
        return int(time.time())

    def _update_timestamp(self):
        self._event_timestamp = self._get_timestamp()

    def _has_elapsed(self, seconds):
        return self._get_timestamp() - self._event_timestamp >= seconds

    def _elapsed_time(self) -> int:
        return self._get_timestamp() - self._event_timestamp

    def open_door(self):
        self._is_closed = False

    def close_door(self):
        self._is_closed = True

    def press_cook_button(self):
        self._cook_button_pressed = True

    def set_cooking_time(self, seconds):
        self._cooking_time = seconds


if __name__ == "__main__":
    fsm = MicrowaveOvenStateMachine()
    fsm.perform_one_step()
    fsm.perform_one_step()
    fsm.perform_one_step()
    fsm.perform_one_step()
    print("User: Opening the door...")
    fsm.open_door()
    fsm.perform_one_step()
    fsm.perform_one_step()
    print("User: Putting a sandwich in the microwave oven...")
    fsm.perform_one_step()
    print("User: Pushing the cook button...(Nothing happens, door is open)")
    fsm.press_cook_button()
    fsm.perform_one_step()
    fsm.perform_one_step()
    print("User: Closing the door...")
    fsm.close_door()
    fsm.perform_one_step()
    fsm.perform_one_step()
    print("User: Pushing the cook button...(Nothing happens, cooking time is not set)")
    fsm.press_cook_button()
    fsm.perform_one_step()
    fsm.perform_one_step()
    print("User: Entering the cooking time...")
    fsm.set_cooking_time(10)
    fsm.perform_one_step()
    fsm.perform_one_step()
    print("User: Pushing the cook button...")
    fsm.press_cook_button()
    timestamp = int(time.time())
    while int(time.time()) - timestamp < 6:
        if not fsm.perform_one_step():
            break
    print("User: Opening the door...")
    fsm.open_door()
    fsm.perform_one_step()
    fsm.perform_one_step()
    print("User: Adding some cheese...")
    timestamp = int(time.time())
    while int(time.time()) - timestamp < 6:
        if not fsm.perform_one_step():
            break
    print("User: Pushing the cook button...(Nothing happens, door is open)")
    fsm.press_cook_button()
    fsm.perform_one_step()
    fsm.perform_one_step()
    print("User: Closing the door...")
    fsm.close_door()
    fsm.perform_one_step()
    fsm.perform_one_step()
    print("User: Pushing the cook button...")
    fsm.press_cook_button()
    while True:
        if not fsm.perform_one_step():
            break
    print("User: Enjoys the meal...")
