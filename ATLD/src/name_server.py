__author__ = 'francesco'

#import os
#os.environ["PYRO_LOGFILE"] = "../log/pyro.log"
#os.environ["PYRO_LOGLEVEL"] = "DEBUG"
import threading, socket, sys
import Pyro4

'''
Modulo NameServer
'''


class NameServer():
    '''
    Classe NameServer che gestisce l'avvio del NameServer.
    '''

    def __init__(self):
        '''
        Avvio del loop del NameServer. In questo modo ascolta e serve le richieste in background.
        '''
        self.start_ns_loop()

    def start_ns(self):
        '''
        Questo metodo avvia il NameServer.
        Di default, il NameServer gira su 0.0.0.0:9090, mentre il Broadcast Server gira su 0.0.0.0:9091
        '''

        print("\nSto facendo partire il Name Server...")

        try:

            Pyro4.naming.startNSloop()

        except socket.error:

            print("Il server è già in esecuzione.")
            sys.exit(0)

    def start_ns_loop(self):
        '''
        In questo metodo, l'avvio del NameServer viene messo in un thread a parte.
        Il thread relativo al NameServer è di tipo 'daemon'.
        '''

        ns_thread = threading.Thread(target=self.start_ns, args=[])
        ns_thread.daemon = True
        ns_thread.start()
