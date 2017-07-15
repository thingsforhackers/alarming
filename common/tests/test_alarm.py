"""
Unit test Alarm module
"""
import datetime
import unittest
import common.alarm as alarm


class TestAlarm(unittest.TestCase):
    """
    Tests for Alarm module
    """

    def _test_init(self):
        """
        Test basic init
        """
        am = alarm.AlarmMgr()
        self.assertIsNotNone(am)


    def test_alarm_fired(self):
        """ Simple """
        am = alarm.AlarmMgr()

        now = datetime.datetime.now()

        print(now)

if __name__ == '__main__':
    unittest.main()
