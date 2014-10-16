__author__ = 'francesco'

import os
os.environ["PYRO_LOGFILE"] = "pyro.log"
os.environ["PYRO_LOGLEVEL"] = "DEBUG"
import threading, socket, sys
import Pyro4


class NameServer():

    def __init__(self):
        self.start_ns_loop()

    def start_ns(self):

        print("Sto facendo partire il Name Server...")

        try:

            Pyro4.naming.startNSloop()

        except socket.error:

            print("Il server è già in esecuzione.")
            sys.exit(0)

    def start_ns_loop(self):

        ns_thread = threading.Thread(target=self.start_ns, args=[])
        ns_thread.daemon = True
        ns_thread.start()
