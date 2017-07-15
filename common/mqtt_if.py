"""
Hides handling of MQTT messages
"""
import threading
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

        self._msg_q = []
        self._msg_q_lock = threading.Lock()

    def _add_msg_to_q(self, msg, payload):
        """Add msg and payload to q"""
        with self._msg_q_lock:
            self._msg_q.append((msg, payload))

    def get_msg(self):
        """Return next message (if any) from q"""
        with self._msg_q_lock:
            if len(self._msg_q):
                return self._msg_q.pop(0)
        return None, None

    def _on_msg_update(self, mqttc, obj, msg):
        """ Handle msg update"""
        self._add_msg_to_q(msg.topic.split("/")[1:], msg.payload)

    def start(self):
        """
        Start everything up
        """
        self.connect(const.MQTT_BROKER)
        self.subscribe(const.MQTT_TOPIC_UPDATE)
        self.message_callback_add(const.MQTT_TOPIC_UPDATE, self._on_msg_update)
        self.loop_start()

    def stop(self):
        """
        Stop everything
        """
        self.loop_stop()

