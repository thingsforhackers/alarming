"""
Quick hack
"""

import paho.mqtt.publish as publish
import common.constants as const

publish.single(const.MQTT_TOPIC_TEST, "hello....", hostname=const.MQTT_BROKER)

