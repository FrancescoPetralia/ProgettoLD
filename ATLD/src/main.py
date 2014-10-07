__author__ = 'francesco'

import threading, socket, sys, Pyro4, re
from PyQt4 import QtGui, QtCore
from main_window import MainWindow
from server import Server


class Main(QtGui.QMainWindow):

    def __init__(self):

        super(Main, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        Pyro4.config.HOST = "0.0.0.0"

        self.resize(400, 100)
        self.setWindowTitle("Analizzatore Testuale")
        self.move(400, 250)

        self.label = QtGui.QLabel("Numero di processori?", self)
        self.label.resize(150, 40)
        self.label.move(130, 10)

        self.textbox = QtGui.QLineEdit(self)
        self.textbox.resize(75, 20)
        self.textbox.move(165, 50)
        self.textbox.returnPressed.connect(self.open_main_window)

        #Settaggio dell'espressione regolare che prevede solo numeri (0-9), da 1 fino a massimo 8
        self.regular_expression = QtCore.QRegExp('^[1-8]{1}$')
        self.validator = QtGui.QRegExpValidator(self.regular_expression)
        self.textbox.setValidator(self.validator)

        self.textbox.textChanged.connect(self.textbox_validation)
        self.textbox.textChanged.emit(self.textbox.text())

        self.mw = None
        # Faccio partire il server
        s = Server()
        s.start_ns_loop()

    def open_main_window(self):

        self.mw = MainWindow()
        self.mw.set_hosts_number(self.get_hosts_number())
        self.mw.show()
        self.hide()

    def textbox_validation(self):

        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
             # Green
            color = '#c4df9b'
            print("Correct")
        else:
            # Red
            color = '#f6989d'
            print("Incorrect")

        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def get_hosts_number(self):

        return self.textbox.text()


def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
