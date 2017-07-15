"""
Contains common python code
"""
import os

APP_NAME = "Alarming"

CONFIG_DIR = "/var/alarming"

ALARM_FILE = os.path.join(CONFIG_DIR, "alarms.toml")
ALARM_LOCK_FILE = os.path.join(CONFIG_DIR, "alarms.toml.lock")


SERVER_STATIC_DIR = os.environ.get("ALARM_STATIC_DIR",
                                   os.path.join(os.getcwd(), "assets", "static"))

MQTT_CLIENT_ID = "id-cej-alarm"

MQTT_TOPIC_TEST = "cej-alarm/test"

MQTT_BROKER = "192.168.1.151"
