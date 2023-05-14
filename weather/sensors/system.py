import psutil
import logging


class System(object):
    _store = None

    def __init__(self, store=None):
        self._store = store
        logging.info("Sys reporter ready")

    def read(self):
        logging.debug("--- START SYSTEM read ---")
        # Getting % usage of virtual_memory ( 3rd field)
        # print('RAM memory % used:', psutil.virtual_memory()[2])
        ram_pct = psutil.virtual_memory()[2]
        # Getting usage of virtual_memory in GB ( 4th field)
        # print('RAM Used (GB):', psutil.virtual_memory()[3]/1000000000)
        self._store.put_ram_pct("system", ram_pct)
        logging.debug("--- END SYSTEM read ---")
