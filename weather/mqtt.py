import logging
import json
import paho.mqtt.client as mqtt
from .config import config


class MQTTSender(object):
    _store = None
    _mqtt_client = None
    _mqtt_connected = False

    def __init__(self, store):
        self._store = store
        self._config = config

        self._mqtt_client = mqtt.Client()
        self._mqtt_client.on_connect = self.on_connect
        self._mqtt_client.on_disconnect = self.on_disconnect
        self._mqtt_client.enable_logger(logger=logging)
        self._mqtt_client.username_pw_set(config["mqtt_user"],
                                          config["mqtt_pass"])

        if config["mqtt_ssl"]:
            self._mqtt_client.tls_set()

        self.connect()
        self._mqtt_client.loop_start()

    def connect(self):
        port = 1883
        if self._config["mqtt_ssl"]:
            port = 8883

        self._mqtt_client.connect(self._config["mqtt_host"], port=port)

    def on_connect(self, _client, _userdata, _flags, rc):
        logging.debug("Connection to MQTT broker rc: %s", rc)
        if rc == 0:
            logging.info("Connection to MQTT broker successful")
            self._mqtt_connected = True

    def on_disconnect(self, _client, _userdata,  rc):
        logging.info("Disconnected from MQTT broker rc: %s", rc)
        self._mqtt_connected = False

    def send(self):
        if not self._mqtt_connected:
            logging.info("Delaying send because of MQTT disconnected")
            return

        while True:
            value = self._store.get()
            logging.debug("Popped %r", value)
            if value == "__EMPTY__":
                break

            value["sensor-id"] = self._config["sensor-id"]
            sensor = value["sensor"]
            topic = self.build_topic(["sensor", sensor])
            payload = json.dumps(value)
            logging.debug("Sending %r to %s", payload, topic)
            message_info = self._mqtt_client.publish(topic, payload, qos=0)
            if message_info.rc != mqtt.MQTT_ERR_SUCCESS:
                logging.error("Error while sending message: %s",
                              message_info.rc)
                return

    def build_topic(self, segments):
        root = self._config["mqtt_root_topic"]
        topic = "/".join([root, self._config["sensor-id"]] + segments)

        return topic
