__author__ = 'francesco'

import threading, socket, sys
import Pyro4


class Server():

    def start_ns(self):

        print("Sto facendo partire il Name Server...")

        try:

            Pyro4.naming.startNSloop()

        except socket.error:

            print("Il server è già in esecuzione.")
            sys.exit(0)

    def start_ns_loop(self):

        ns_thread = threading.Thread(target=self.start_ns, args=[])
        #ns_thread.daemon = True
        ns_thread.setDaemon(True)
        ns_thread.start()
