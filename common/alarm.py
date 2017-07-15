"""
Manages alarm times
"""

import os
import logging
import time
import math
import pytoml as toml
import datetime
import pprint
from dateutil.relativedelta import *
from dateutil.rrule import *
import common.constants as const


class AlarmMgr(object):
    """
    Manage alarms
    """

    # Enumerate all alarm modes
    ALARM_MODE_ANY = "any"
    ALARM_MODE_WE_ONLY = "weekend"
    ALARM_MODE_WD_ONLY = "weekday"
    ALARM_MODE_NONE = "none"

    def __init__(self):
        """
        Setup a few things
        """
        self._modes = [self.ALARM_MODE_ANY,
                       self.ALARM_MODE_WE_ONLY,
                       self.ALARM_MODE_WD_ONLY,
                       self.ALARM_MODE_NONE]
        self._mode_idx = 0
        self._cfg = {}
        self._next_alarm = None
        self._last_time = None
        self.load_cfg()
        self.parse_cfg()

    def load_cfg(self):
        """
        Update internal state based on new cfg file
        """
        try:
            with open(const.ALARM_FILE, 'r') as f:
                self._cfg = toml.load(f)
        except FileNotFoundError:
            pass

    def next_mode(self):
        """Move alarm on to next mode"""
        self._mode_idx += 1
        if self._mode_idx == len(self._modes):
            self._mode_idx = 0

        current_mode = self._modes[self._mode_idx]

        if current_mode == self.ALARM_MODE_ANY:
            enable_we = True
            enable_wd = True
        elif current_mode == self.ALARM_MODE_WE_ONLY:
            enable_we = True
            enable_wd = False
        elif current_mode == self.ALARM_MODE_WD_ONLY:
            enable_we = False
            enable_wd = True
        elif current_mode == self.ALARM_MODE_NONE:
            enable_we = False
            enable_wd = False

        self._cfg["weekday"]["enabled"] = enable_wd
        self._cfg["weekend"]["enabled"] = enable_we

        self._save_cfg()
        self.parse_cfg()

    def parse_cfg(self, now=None):
        """
        Parse loaded config

        @parm now: Use this time instead
        @type now: None or datetime.datetime instance
        """
        # Quick bail out for empty config
        if not len(self._cfg):
            return

        # Now check for a new alarm
        if now is None:
            now = datetime.datetime.now()
            now = datetime.datetime(year=now.year,
                                    month=now.month,
                                    day=now.day,
                                    hour=now.hour,
                                    minute=now.minute) #Drop seconds
        else:
            assert isinstance(now, datetime.datetime)
        is_week_day = now.weekday() < 5

        # Now get weekday alarm
        weekday = self._cfg.get("weekday", {})
        wd_enabled = weekday.get("enabled", False)
        if wd_enabled:
            hh, mm = weekday.get("time", "00:00").split(":")
            wd_alarm = now+relativedelta(hour=int(hh), minute=int(mm))
            if wd_alarm <= now or is_week_day == False:
                wd_alarm = rrule(DAILY, byweekday=(MO, TU, WE, TH, FR), dtstart=wd_alarm)[1 if is_week_day else 0]
        else:
            wd_alarm = now+relativedelta(year=2030) #Move it well ahead of time

        # now get weekend alarm
        weekend = self._cfg.get("weekend", {})
        we_enabled = weekend.get("enabled", False)
        if we_enabled:
            hh, mm = weekend.get("time", "00:00").split(":")
            we_alarm = now+relativedelta(hour=int(hh), minute=int(mm))
            if we_alarm <= now or is_week_day == True:
                we_alarm = rrule(DAILY, byweekday=(SA, SU), dtstart=we_alarm)[1 if not is_week_day else 0]
        else:
            we_alarm = now+relativedelta(years=2030)

        if we_alarm < wd_alarm:
            self._next_alarm = we_alarm
        else:
            self._next_alarm = wd_alarm

    def _save_cfg(self):
        """
        Save internal state to file
        """
        with open(const.ALARM_FILE, 'w') as f:
            self._cfg['revision'] = int(math.floor(time.time()))
            toml.dump(self._cfg, f)

    def get_next_alarm(self):
        """
        Get next alarm that will fire
        """
        if self._next_alarm is None or int(self._next_alarm.year) == 2030:
            return None
        else:
            return self._next_alarm

    def has_alarm_fired(self, now=None):
        """Check to see if an alarm has fired"""
        fired = False
        alarm = self.get_next_alarm()
        if alarm:
            if now is None:
                now = datetime.datetime.now()
                now = datetime.datetime(year=now.year,
                                        month=now.month,
                                        day=now.day,
                                        hour=now.hour,
                                        minute=now.minute) #Drop seconds
            if now >= alarm and self._last_time < alarm:
                fired = True
            self._last_time = now
        return fired

