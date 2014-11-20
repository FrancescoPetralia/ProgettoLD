__author__ = 'francesco'

import sys
import argparse
from PyQt4 import QtGui, QtCore
from graphical_user_interface import SetHostsWindow
from graphical_user_interface import HostsConnectionWindow

'''
Questo modulo si occupa dell'esecuzione dell'applicazione.
'''


class Main(QtGui.QMainWindow):
    '''
    Classe Main che eredita da QtGui.QMainWindow.
    '''

    def __init__(self):

        pass


def main():
    '''
    metodo main() della classe Main. In questo metodo viene configurato il parser per poter eseguire l'applicazione
    da terminale. Nello specifico, vengono definiti i parametri -n e -a, usati rispettivamente per configurare il numero
    di nodi su cui parallelizzare l'analisi, e gli indirizzi a cui connettersi in remoto.
    Nel caso in cui questi parametri non vengano specificati dall'utente a runtime, l'applicazione chiederà, tramite
    le apposite finestre grafiche, di specificarli, in modo da continuare la regolare esecuzione del programma.
    :return:
    '''

    hosts_number, addresses, file_path, flag = 0, "", "", 0

    # Configurazione del parser per gli argomenti in input
    parser = argparse.ArgumentParser(description="Valori di avvio: ")
    parser.add_argument("-n", help="Imposta il numero di host su cui eseguire l'analisi.")
    parser.add_argument("-a", help="Imposta gli indirizzi a cui connettersi in remoto.")
    args = parser.parse_args()

    if args.n is not None:
        hosts_number = args.n
        flag += 1

    if args.a is not None:
        addresses = args.a
        flag += 1

    app = QtGui.QApplication(sys.argv)

    if flag > 0:
        hcw = HostsConnectionWindow(0, 1)
        hcw.set_addresses(addresses.split(','))
        hcw.set_hosts_number(hosts_number)
        hcw.show()
        print("Parametri passati: \n" + "- numero di hosts: " + str(hosts_number) + ".\n" +
              "-indirizzi: " + str(addresses.split(',')))
    else:

        w1 = SetHostsWindow()
        w1.show()

    sys.exit(app.exec_())

if __name__ == "__main__":

    main()
