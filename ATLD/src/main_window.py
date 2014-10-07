__author__ = 'francesco'

import sys, threading

from connection import Connection
from PyQt4 import QtCore, QtGui


class MainWindow(Connection):

    def __init__(self):

        super(MainWindow, self).__init__()

        self.na = 0
        self.offset_label = 60
        self.offset_textbox = 60
        self.xpositionlabel_a = 50
        self.xpositiontextbox_a = 180
        self.xpositionlabel_p = 500
        self.xpositiontextbox_p = 630
        self.labelheight = 30
        self.labelwidth = 150
        self.textboxheight = 30
        self.textboxwidth = 175

        self.resize(900, 620)
        self.move(225, 60)
        self.setWindowTitle("Analizzatore Testuale")

        self.labellist_addresses = []
        self.textboxlist_addresses = []

        self.labellist_password = []
        self.textboxlist_password = []

        self.buttonconnect = QtGui.QPushButton("Connetti", self)
        self.buttonconnect.resize(100, 45)
        self.buttonconnect.move(735, 550)
        # Al click del bottone, faccio partire la connessione al Name Server
        QtCore.QObject.connect(self.buttonconnect, QtCore.SIGNAL('clicked()'), self.on_click_button_connect)

        self.labelhost = QtGui.QLabel("", self)
        self.labelhost.resize(300, 30)
        self.labelhost.move(50, 550)

    def set_hosts_number(self, n_addresses):

        self.na = n_addresses

        for count in range(0, int(self.na)):
            self.labellist_addresses.append(QtGui.QLabel("Indirizzo host:", self))
            self.textboxlist_addresses.append(QtGui.QLineEdit(self))
            self.labellist_password.append(QtGui.QLabel("Password host:", self))
            self.textboxlist_password.append(QtGui.QLineEdit(self))

        for count in range(0, int(self.na)):

            self.labellist_addresses[count].resize(self.labelwidth, self.labelheight)
            self.labellist_addresses[count].move(self.xpositionlabel_a, (self.offset_label * (count + 1)))

            self.textboxlist_addresses[count].resize(self.textboxwidth, self.textboxheight)
            self.textboxlist_addresses[count].move(self.xpositiontextbox_a, (self.offset_textbox * (count + 1)))
            self.textboxlist_addresses[count].setText("francesco@localhost")

            self.labellist_password[count].resize(self.labelwidth, self.labelheight)
            self.labellist_password[count].move(self.xpositionlabel_p, (self.offset_label * (count + 1)))

            self.textboxlist_password[count].setEchoMode(2)
            self.textboxlist_password[count].resize(self.textboxwidth, self.textboxheight)
            self.textboxlist_password[count].move(self.xpositiontextbox_p, (self.offset_textbox * (count + 1)))

        self.labelhost.setText("Numero di host su cui parallelizzare l'analisi: " + str(self.na))

    def on_click_button_connect(self):

        #self.open_server_connection()
        self.find_obj(0, self.textboxlist_addresses[0].text(), self.textboxlist_password[0].text())



