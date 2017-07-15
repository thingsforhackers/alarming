"""
Quick hack
"""

import paho.mqtt.publish as publish
import common.constants as const
import json


msg = {"weekend" :  { "enabled" : False, "time" : "19:45" } }

publish.single(const.MQTT_TOPIC_UPDATE, json.dumps(msg), hostname=const.MQTT_BROKER)

