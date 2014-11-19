__author__ = 'francesco'

import sys
import argparse
from PyQt4 import QtGui, QtCore
from graphical_user_interface import SetHostsWindow
from graphical_user_interface import HostsConnectionWindow


class Main(QtGui.QMainWindow):

    def __init__(self):

        pass


def main():

    hosts_number, addresses, file_path, flag = 0, "", "", 0

    # Configurazione del parser per gli argomenti in input
    parser = argparse.ArgumentParser(description="Valori di avvio: ")
    parser.add_argument("-n", help="Imposta il numero di host su cui eseguire l'analisi.")
    parser.add_argument("-a", help="Imposta un indirizzo a cui connettersi in remoto. A questo indirizzo ci si "
                                   "connetterà 'n' volte, in base al valore del parametro -n.")
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
