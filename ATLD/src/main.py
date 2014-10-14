__author__ = 'francesco'

import threading, socket, sys, Pyro4
from PyQt4 import QtGui, QtCore
from main_window import MainWindow
from server import Server
from graphical_user_interface import SetHostsWindow, HostsConnectionWindow


class Main(QtGui.QMainWindow):

    def __init__(self):

        Pyro4.config.HOST = "127.0.0.1"
        pass


def main():
    app = QtGui.QApplication(sys.argv)
    #main = Main()
    #main.show()
    w1 = SetHostsWindow()
    w1.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
