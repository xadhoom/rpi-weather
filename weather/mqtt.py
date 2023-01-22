import logging


class MQTTSender(object):
    _store = None

    def __init__(self, store):
        self._store = store

    def send(self):
        while True:
            value = self._store.get()
            logging.debug("Popped %r", value)
            if value == "__EMPTY__":
                break
