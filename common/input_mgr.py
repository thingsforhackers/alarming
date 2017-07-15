"""
    Handles differences between embedded and devlopment inputs
"""
import pygame
import time




class InputMgr(object):
    """
    Hide differences
    """

    KEY_STATE_UP = "UP"
    KEY_STATE_PRESSED = "PRESSED"
    KEY_STATE_HOLDING = "HOLDING"
    KEY_STATE_HELD = "HELD"

    HOLD_TIME = 2


    def __init__(self):
        """ """
        try:
            import gpiozero
            self._have_gpio = True
            self._cancel_button = gpiozero.Button(18)
            self._toggle_button = gpiozero.Button(12)
        except ImportError:
            self._have_gpio = False
            self._key_states = {}

    def update(self):
        """ """
        if not self._have_gpio:
            now = time.time()
            current_keys_pressed = pygame.key.get_pressed()
            for key, info in self._key_states.items():
                pressed = current_keys_pressed[key]
                if pressed:
                    if info["state"] == self.KEY_STATE_UP:
                        info["state"] = self.KEY_STATE_PRESSED
                        info["time"] = now
                    elif info["state"] == self.KEY_STATE_PRESSED:
                        info["state"] = self.KEY_STATE_HOLDING
                    elif info["state"] == self.KEY_STATE_HOLDING and (info["time"] - now) > self.HOLD_TIME:
                        info["state"] = self.KEY_STATE_HELD
                else:
                    info["state"] = self.KEY_STATE_UP

    def _get_state(self, key):
        """
        """
        state = self._key_states.get(key)
        if state is None:
            state = {"state" : self.KEY_STATE_UP}
            self._key_states[key] = state
        return state

    def is_cancel_pressed(self):
        """ """
        if self._have_gpio:
            return self._cancel_button.is_pressed
        else:
            state = self._get_state(pygame.locals.K_c)
            return state["state"] == self.KEY_STATE_PRESSED

    def is_toggle_pressed(self):
        """ """
        if self._have_gpio:
            return self._toggle_button.is_pressed
        else:
            state = self._get_state(pygame.locals.K_t)
            return state["state"] == self.KEY_STATE_PRESSED
