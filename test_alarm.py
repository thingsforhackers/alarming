"""
Unit test Alarm module
"""

import unittest
import alarm


class TestAlarm(unittest.TestCase):
    """
    Tests for Alarm module
    """

    def test1(self):
        """
        """
        am = alarm.AlarmMgr("/tmp")

        cfg = {
            'weekend' : '+:08:47',
            'weekday' : '+:06:45',
        }
        am._update_cfg(cfg)
        print am._next_alarm


if __name__ == '__main__':
    unittest.main()
