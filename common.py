"""
Contains common python code
"""

import os
import datetime
import filelock
import pytoml as toml


class Alarm(object):
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

    def _get_todays_alarms(self, today=None):
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

    def load(self):
        """
        Loads or reloads alarms from file
        """
        try:
            with self._alarm_file_lock.acquire(timeout=5):
                with open(self._alarm_file, "r") as f:
                    alarms = toml.load(f)
                    if alarms:
                        self._set_alarms(alarms)
        except filelock.Timeout:
            print "Unable to lock alarm file"



if __name__ == "__main__":
    al = Alarm("/home/tfh/.config/alarming")
    al.load()
    print al._get_todays_alarms()
