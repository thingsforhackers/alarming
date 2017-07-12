"""
Manages alarm times
"""

import os
import logging
import time
import math
import filelock
import pytoml as toml
import datetime
from dateutil.relativedelta import *
from dateutil.rrule import *
import common


class AlarmMgr(object):
    """
    Manage alarms
    """

    def __init__(self):
        """
        Setup a few things
        """
        self._alarm_file_lock = filelock.FileLock(common.ALARM_LOCK_FILE)
        self._cfg = {}
        self._next_alarm = None


    def _update_cfg(self, new_cfg, now=None):
        """
        Update internal state based on new cfg file
        """
        self._cfg = new_cfg

        if now is None:
            now = datetime.datetime.now()
            now = datetime.datetime(year=now.year,
                                    month=now.month,
                                    day=now.day,
                                    hour=now.hour,
                                    minute=now.minute) #Drop seconds
        is_week_day = now.weekday() < 5

        # Now get weekday alarm
        wd_parts = self._cfg.get('weekday', '-:00:00').split(':')
        wd_enabled = True if wd_parts[0] == '+' else False
        if wd_enabled:
            wd_alarm = now+relativedelta(hour=int(wd_parts[1]), minute=int(wd_parts[2]))
            if wd_alarm < now or is_week_day == False:
                wd_alarm = rrule(DAILY, byweekday=(MO, TU, WE, TH, FR), dtstart=wd_alarm)[1]
        else:
            wd_alarm = now+relativedelta(year=2030) #Move it well ahead of time

        # now get weekend alarm
        we_parts = self._cfg.get('weekend', '-:00:00').split(':')
        we_enabled = True if we_parts[0] == '+' else False
        if we_enabled:
            we_alarm = now+relativedelta(hour=int(we_parts[1]), minute=int(we_parts[2]))
            if we_alarm < now or is_week_day == True:
                we_alarm = rrule(DAILY, byweekday=(SA, SU), dtstart=we_alarm)[0]
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
        try:
            with self._alarm_file_lock.acquire(timeout=10):
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

    def check_for_cfg_update(self):
        """
        Check if an update of the internal alarm is needed
        """
        try:
            with self._alarm_file_lock.acquire(timeout=5):
                with open(common.ALARM_FILE, 'r') as f:
                    new_cfg = toml.load(f)
                    new_rev = new_cfg.get('revision', 1)
                    old_rev = self._cfg.get('revision', 0)
                    if new_rev > old_rev:
                        logging.info("Update cfg old rev:{0}, new rev:{1}".format(old_rev, new_rev))
                        self._update_cfg(new_cfg)
        except FileNotFoundError:
            pass
        except filelock.Timeout:
            logging.error("Timeout reading cfg file")


if __name__ == '__main__':
    if 0:
        logging.basicConfig(filename="/tmp/alarm.log", level=logging.INFO)
        logging.info("Alarm started")
        am = AlarmMgr()
        am.check_for_cfg_update()
        am._save_cfg()

    am = AlarmMgr()

    cfg = {
        "weekday" : "-:06:30",
    }

