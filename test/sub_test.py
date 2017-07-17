"""
Quick hack
"""

import paho.mqtt.publish as publish
import common.constants as const
import json


msg = {"weekday" :  { "enabled" : True, "time" : "20:00" } }

publish.single(const.MQTT_TOPIC_UPDATE_ALARM, json.dumps(msg), hostname=const.MQTT_BROKER)

