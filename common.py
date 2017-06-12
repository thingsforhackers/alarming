"""
Contains common python code
"""

import os
import datetime
import time
import filelock
import pytoml as toml


class AlarmMgr2(object):
    """
    """

    def __iit__(self, cfg_base_dir):
        """
        """
        self._alarm_file = os.path.join(cfg_base_dir, "alarms.toml")
        self._alarm_file_lock = filelock.FileLock(os.path.join(cfg_base_dir, "alarms.toml.lock"))


    def load_alarms(self):
        """
        """

class AlarmMgr(object):
    """
    Handles loading/saving tracking and firing of alarms
    """
    week_days = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    week_end_days = ['saturday', 'sunday']

    def __init__(self, cfg_base_dir):
        """
        Setup a few things
        """
        self._alarm_file = os.path.join(cfg_base_dir, "alarms.toml")
        self._alarm_file_lock = filelock.FileLock(os.path.join(cfg_base_dir, "alarms.toml.lock"))
        self._current_rev = 0
        self._config = {}
        self._alarms = []

    def _set_alarms(self, alarms):
        """
        Set alarms from supplied alarms document
        """
        new_alarms = []
        alarm_list = alarms.get("alarms", [])
        for alarm in alarm_list:
            #First validate
            alarm_invalid = False
            hour = alarm.get("hour", 0)
            if hour < 0 or hour > 23:
                alarm_invalid = True
            minute = alarm.get("minute", 0)
            if minute < 0 or minute > 59:
                alarm_invalid = True
            if not alarm_invalid:
                new_alarms.append(alarm)
        if new_alarms:
            self._alarms = new_alarms

    def get_todays_alarms(self, today=None):
        """
        Return a list of alarms that will occur today
        """
        todays_alarms = []
        if today is None:
            today = datetime.date.today()
        day_name = today.strftime("%A").lower()

        for alarm in self._alarms:
            is_today = False
            if not alarm.get('enabled', False):
                continue
            alarm_day = alarm.get('day', 'any')
            if alarm_day == day_name:
                is_today = True
            if alarm_day == "any":
                is_today = True
            if day_name in self.week_end_days and alarm_day == "weekend":
                is_today = True
            if day_name in self.week_days and alarm_day == "weekday":
                is_today = True
            if is_today:
                todays_alarms.append(alarm)
        return sorted(todays_alarms, key=lambda a: a.get('hour'))

    def get_next_alarm(self, when=None):
        """Get next alarm that will fire"""
        if when is None:
            when = datetime.datetime.now()
        for alarm in self._alarms:
            pass

    def _parse_alarms(self):
        """Parse alarm section from config file"""
        alarm_cfg = self._config.get("alarms", [])
        alarms = []

    def load(self):
        """
        Loads or reloads alarms from file
        """
        try:
            with self._alarm_file_lock.acquire(timeout=5):
                with open(self._alarm_file, "r") as f:
                    self._config = toml.load(f)
                    self._parse_alarms()
        except filelock.Timeout:
            print "Unable to lock alarm file"


class AlarmError(Exception):
    """Alarm type errors"""
    pass

class Alarm(object):
    """Represents a active full specified alarm"""

    def __init__(self, cfg, now=None):
        """Init from supplied cfg dictionary """

        if type(cfg) != dict:
            raise AlarmError("cfg needs to be a dictionary, not a {0}".format(type(cfg)))
        if now is None:
            now = datetime.datetime.now()
        current_minute_offset = now.hour * 60 + now.minute

        try:
            self._hour = int(cfg.get('hour'))
            self._minute = int(cfg.get('minute'))
            self._enabled = cfg.get('enabled')
            self._description = cfg.get('description')
            self._
        except (KeyError, TypeError) as ex:
            raise AlarmError("Incorrect alarm cfg: {0}".format(str(ex)))

        # handle setup of day
        alarm_minute_offset = self._hour * 60 + self._minute
        day = cfg.get('day', 'any')

        if day == 'any':
            day == now.day
        elif day == 'weekday':
            if new.weekday() < 5:
                day = new.weekday()
            else:
                day = 0
        elif day == 'weekend':
            if new.weekday() >= 5:
                day = new.weekday()
            else:
                day = 5


if __name__ == "__main__":
    al = AlarmMgr("/home/tfh/.config/alarming")
    al.load()

    # print int(time.mktime(datetime.datetime.now().timetuple()))
