"""
Hides handling of MQTT messages
"""
import paho.mqtt.client as mqtt
import common.constants as const


class MQTTInterface(mqtt.Client):
    """
    """

    def __init__(self, my_id):
        """
        Set a few things up
        """
        super(MQTTInterface, self).__init__(client_id=my_id, clean_session=True)

    def _on_msg_test(self, mqttc, obj, msg):
        """
        Handle a reveived message for a suscribed topic
        """
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def start(self):
        """
        Start everything up
        """
        self.connect(const.MQTT_BROKER)
        self.subscribe(const.MQTT_TOPIC_TEST)
        self.message_callback_add(const.MQTT_TOPIC_TEST, self._on_msg_test)
        self.loop_start()

    def stop(self):
        """
        Stop everything
        """
        self.loop_stop()

