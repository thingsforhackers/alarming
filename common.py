"""
Contains common python code
"""
import os


CONFIG_DIR = "/var/alarming"

ALARM_FILE = os.path.join(CONFIG_DIR, "alarms.toml")
ALARM_LOCK_FILE = os.path.join(CONFIG_DIR, "alarms.toml.lock")
