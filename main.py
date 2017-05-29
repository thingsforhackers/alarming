"""
Main module for Alaraming alarm clock project.
This will mange display, track alarm t/o etc.
"""
import os
import sys
import datetime
import pygame
from pygame.locals import *


class AlarmingError(Exception):
    pass


class Alarming(object):
    """
    Main Alarm module
    """
    MAIN_TIME_COLOUR = (255, 255, 255)

    def __init__(self):
        """ """
        self._screen_size = (656, 416) #Match frame buffer
        self._screen = None
        self._screen_flags = pygame.NOFRAME
        self._main_time_char_map = {}

    def _init_pygame(self):
        """Set up a few things in pygame"""

        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "Using DISPLAY={0}".format(disp_no)
            try:
                pygame.display.init()
            except pygame.error as pyg_error:
                raise AlarmingError("Failed to init display driver: {0}".format(pyg_error))
            self._screen_flags |= pygame.NOFRAME
        else:
            print "Using frame buffer"
            # Assume running console mode on piZero
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.putenv('SDL_FBDEV', '/dev/fb0')
            os.putenv('SDL_NOMOUSE', '1')
            try:
                pygame.display.init()
            except pygame.error as pyg_error:
                raise AlarmingError("Failed to init display driver: {0}".format(pyg_error))
            self._screen_size = (pygame.display.Info().current_w,
                                 pygame.display.Info().current_h)
            self._screen_flags |= pygame.FULLSCREEN
        print "Screen Size: {0}".format(self._screen_size)
        self._screen = pygame.display.set_mode(self._screen_size,
                                               self._screen_flags)
        pygame.font.init()
        pygame.mouse.set_visible(False)
        pygame.display.update()

        #Fonts for main time
        self._main_time_font = pygame.font.Font("fonts/VeraMono-Bold.ttf", 192)
        self._main_time_char_map = self._bld_char_map("0123456789: ",
                                                      self._main_time_font,
                                                      self.MAIN_TIME_COLOUR)

        #bgnds
        self._bg = pygame.image.load("bg/zlatan.png")

    def _bld_char_map(self, chars, font, colour):
        """util func"""
        char_map = {}
        for c in chars:
            char_map[c] = (font.render(c, True, colour ), font.size(c))
        return char_map

    def _draw_string(self, text, char_map, x, y):
        """ """
        for c in text:
            surface, size = char_map[c]
            self._screen.blit(surface, (x, y))
            x += size[0]

    def _draw_time(self):
        """Draw main time"""
        ct = datetime.datetime.now()
        ts = "{0:02d}:{1:02d}".format(ct.hour, ct.minute)
        ypos = 416/3 - 241/2
        self._draw_string(ts, self._main_time_char_map, 32, ypos)
        pygame.draw.line(self._screen,
                         self.MAIN_TIME_COLOUR,
                         [32, ypos + 192],
                         [32 + (10 * 60) - (10 * ct.second), ypos + 192],
                         5)

    def _run_loop(self):
        """Run pygame event loop"""
        print "Start loop"
        run = True
        while run:

            #Process events
            for event in pygame.event.get():
                if event.type == pygame.locals.KEYUP:
                    if event.key == pygame.locals.K_q:
                        run = False
                if event.type == pygame.locals.QUIT:
                    run = False

            # Update screen
            # self._screen.fill((0, 0, 0))
            self._screen.blit(self._bg, (0, 0))
            self._draw_time()

            pygame.display.update()

    def start(self):
        """Entry point"""
        self._init_pygame()
        self._run_loop()
        pygame.quit()

if __name__ == "__main__":
    alarming = Alarming()
    sys.exit(alarming.start())

