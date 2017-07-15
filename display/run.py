"""
Main module for Alaraming alarm clock project.
This will mange display, track alarm t/o etc.
"""
import os
import sys
import datetime
import string
import logging
import pygame
from pygame.locals import *
import common.constants as const
import common.alarm as alarm
import common.input_mgr as input_mgr
import common.mqtt_if as mqtt_if


class AlarmingError(Exception):
    pass


class Alarming(object):
    """
    Main Alarm module
    """
    MAIN_TIME_COLOUR = (255, 255, 255)
    CLEAR_COLOUR = (0, 0, 0)

    MODE_NORMAL = "normal"
    MODE_ALARM = "alarm"

    def __init__(self):
        """ """
        self._screen_size = (656, 416) #Match frame buffer
        self._screen = None
        self._screen_flags = pygame.NOFRAME
        self._main_time_char_map = {}
        if not os.path.isdir(const.CONFIG_DIR):
            raise AlarmingError("Fatal: {0} does not exist".format(const.CONFIG_DIR))
        self._am = alarm.AlarmMgr()
        self._mode = self.MODE_NORMAL
        self._input = input_mgr.InputMgr()
        self._mqtt_if = mqtt_if.MQTTInterface(my_id=const.MQTT_CLIENT_ID)

    def _init_pygame(self):
        """Set up a few things in pygame"""

        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print("Using DISPLAY={0}".format(disp_no))
            try:
                pygame.display.init()
            except pygame.error as pyg_error:
                raise AlarmingError("Failed to init display driver: {0}".format(pyg_error))
            self._screen_flags |= pygame.NOFRAME
        else:
            print("Using frame buffer")
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
        print("Screen Size: {0}".format(self._screen_size))
        self._screen = pygame.display.set_mode(self._screen_size,
                                               self._screen_flags)
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        pygame.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        pygame.display.update()

        #Fonts for main time
        self._main_time_font = pygame.font.Font("assets/fonts/VeraMono-Bold.ttf", 192)
        self._main_time_char_map = self._bld_char_map("0123456789: ",
                                                      self._main_time_font,
                                                      self.MAIN_TIME_COLOUR)
        #Secondary font
        self._med_font = pygame.font.Font("assets/fonts/VeraMono.ttf", 24)
        self._med_char_map = self._bld_char_map(string.printable,
                                                self._med_font,
                                                self.MAIN_TIME_COLOUR)
        #bgnds
        self._bg = pygame.image.load("assets/bg/zlatan.png")

        #on screen icons
        self._alarm_icon = pygame.image.load("assets/gfx/alarm.png")

        self._alarm_snd = pygame.mixer.Sound("assets/audio/Alarm-tone.ogg")

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

    def _draw_date(self):
        """Draw current date"""
        cdate = datetime.date.today()
        suf = lambda n: "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10,"th"))
        self._draw_string(cdate.strftime("%A {0} %B %Y".format(suf(cdate.day))), self._med_char_map, 0, 0)

    def _draw_alarm(self):
        """Draw current alarm"""
        alarm = self._am.get_next_alarm()
        if alarm:
            self._screen.blit(self._alarm_icon, (32, 250))
            self._draw_string(alarm.strftime("%a @ %H:%M"), self._med_char_map, 32, 310)

    def _run_loop(self):
        """Run pygame event loop"""
        print("Start loop")
        run = True
        while run:

            #Process events
            for event in pygame.event.get():
                if event.type == pygame.locals.KEYUP:
                    if event.key == pygame.locals.K_q:
                        run = False
                if event.type == pygame.locals.QUIT:
                    run = False

            if self._mode == self.MODE_NORMAL:
                self._screen.blit(self._bg, (0, 0))
                self._draw_date()
                self._draw_time()
                self._draw_alarm()
                if self._am.has_alarm_fired():
                    print("Alarm has fired!!!")
                    self._mode = self.MODE_ALARM
                    alarm_cancel = False
                    self._alarm_snd.play(loops=-1)
            else:
                self._screen.fill(self.CLEAR_COLOUR)
                if self._input.is_cancel_pressed():
                    self._alarm_snd.stop()
                    self._mode = self.MODE_NORMAL
                    self._am._update_cfg()


            pygame.display.update()

    def start(self):
        """Entry point"""
        logging.basicConfig(filename="/tmp/alarming.log", level=logging.INFO)
        logging.info("Alarm started")
        self._init_pygame()
        self._mqtt_if.start()
        self._run_loop()
        self._mqtt_if.stop()
        pygame.quit()

if __name__ == "__main__":
    alarming = Alarming()
    sys.exit(alarming.start())

