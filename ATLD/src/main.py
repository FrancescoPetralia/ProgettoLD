__author__ = 'francesco'

import sys
from PyQt4 import QtGui, QtCore
from graphical_user_interface import SetHostsWindow


class Main(QtGui.QMainWindow):

    def __init__(self):
        pass


def main():
    app = QtGui.QApplication(sys.argv)
    w1 = SetHostsWindow()
    w1.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
