"""
Unit tests for common.py
"""
import unittest
import common


class TestAlarm(unittest.TestCase):
    """Test common.Alarm class"""

    def test_creation(self):
        """Test Alam object creation"""
        try:
            _ = common.Alarm([])
        except common.AlarmError as ex:
            pass
        else:
            self.fail("Expected error for non dict arg")

        try:
            cfg = {}
            _ = common.Alarm(cfg)
        except common.AlarmError as ex:
            pass
        else:
            self.fail("Expected error for bad cfg")

if __name__ == "__main__":
    unittest.main()
