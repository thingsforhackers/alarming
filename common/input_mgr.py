"""
    Handles differences between embedded and devlopment inputs
"""
import pygame




class InputMgr(object):
    """
    Hide differences
    """

    def __init__(self):
        """ """
        try:
            import gpiozero
            self._have_gpio = True
            self._cancel_button = gpiozero.Button(12)
        except ImportError:
            self._have_gpio = False

    def is_cancel_pressed(self):
        """ """
        if self._have_gpio:
            return self._cancel_button.is_pressed
        else:
            pressed = pygame.key.get_pressed()
            return pressed[pygame.locals.K_c]
