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

    def __init__(self):
        """
        Setup a few things
        """
        self._cfg = {}
        self._next_alarm = None
        self.load_cfg()

    def load_cfg(self, now=None):
        """
        Update internal state based on new cfg file
        """
        try:
            with open(const.ALARM_FILE, 'r') as f:
                self._cfg = toml.load(f)
        except FileNotFoundError:
            return

        # Now check for a new alarm
        if now is None:
            now = datetime.datetime.now()
            now = datetime.datetime(year=now.year,
                                    month=now.month,
                                    day=now.day,
                                    hour=now.hour,
                                    minute=now.minute+1) #Drop seconds
        is_week_day = now.weekday() < 5

        # Now get weekday alarm
        weekday = self._cfg.get("weekday", {})
        wd_enabled = weekday.get("enabled", False)
        if wd_enabled:
            hh, mm = weekday.get("time", "00:00").split(":")
            wd_alarm = now+relativedelta(hour=int(hh), minute=int(mm))
            if wd_alarm < now or is_week_day == False:
                wd_alarm = rrule(DAILY, byweekday=(MO, TU, WE, TH, FR), dtstart=wd_alarm)[1]
        else:
            wd_alarm = now+relativedelta(year=2030) #Move it well ahead of time

        # now get weekend alarm
        weekend = self._cfg.get("weekend", {})
        we_enabled = weekend.get("enabled", False)
        if we_enabled:
            hh, mm = weekend.get("time", "00:00").split(":")
            we_alarm = now+relativedelta(hour=int(hh), minute=int(mm))
            if we_alarm < now or is_week_day == True:
                we_alarm = rrule(DAILY, byweekday=(SA, SU), dtstart=we_alarm)[0]
        else:
            we_alarm = now+relativedelta(years=2030)

        if we_alarm < wd_alarm:
            self._next_alarm = we_alarm
        else:
            self._next_alarm = wd_alarm
        pprint.pprint(self._cfg)

    def _save_cfg(self):
        """
        Save internal state to file
        """
        try:
            with self._alarm_file_lock.acquire(timeout=self.FILE_LOCK_TO):
                with open(common.ALARM_FILE, 'w') as f:
                    self._cfg['revision'] = int(math.floor(time.time()))
                    toml.dump(self._cfg, f)
        except filelock.Timeout:
            logging.error("Timeout writing cfg file")

    def get_next_alarm(self):
        """
        Get next alarm that will fire
        """
        if self._next_alarm is None or int(self._next_alarm.year) == 2030:
            return None
        else:
            return self._next_alarm

    def has_alarm_fired(self):
        """Check to see if an alarm has fired"""
        alarm = self.get_next_alarm()
        if alarm:
            now = datetime.datetime.now()
            if alarm <= now:
                self._next_alarm = None
                print(now)
                return True
            else:
                return False
        else:
            return False
