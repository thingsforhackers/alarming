"""
Hides handling of MQTT messages
"""
import threading
import paho.mqtt.client as mqtt
import common.constants as const


class MQTTInterface(mqtt.Client):
    """
    """

    def __init__(self, my_id, topics):
        """ Set a few things up """
        assert(len(topics))
        super(MQTTInterface, self).__init__(client_id=my_id, clean_session=True)

        self._msg_queues = {}
        self._msg_q_lock = threading.Lock()

        self.connect(const.MQTT_BROKER)
        for topic in topics:
            self.subscribe(topic)

    def _add_msg_to_q(self, topic, payload):
        """Add msg and payload to q"""
        with self._msg_q_lock:
            queue = self._msg_queues.get(topic, [])
            if len(queue) == 0:
                self._msg_queues[topic] = queue
            queue.append(payload)

    def get_msg(self, topic):
        """Return next message (if any) from q"""
        with self._msg_q_lock:
            queue = self._msg_queues.get(topic, [])
            if len(queue):
                return queue.pop(0)
        return None

    def on_message(self, mqttc, obj, msg):
        """ """
        self._add_msg_to_q(msg.topic, msg.payload)

    def start(self):
        """ Start everything up """
        self.loop_start()

    def stop(self):
        """ Stop everything """
        self.loop_stop()

