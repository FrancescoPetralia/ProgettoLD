__author__ = 'francesco'

import os
os.environ["PYRO_LOGFILE"] = "pyro.log"
os.environ["PYRO_LOGLEVEL"] = "DEBUG"
import threading
import socket
import getpass
import Pyro4
import queue
import time
from PyQt4 import QtGui, QtCore
from main_window import MainWindow
from name_server import NameServer
from connection import Connection


class SetHostsWindow(QtGui.QMainWindow):

    def __init__(self):

        super(SetHostsWindow, self).__init__()
        Pyro4.config.HOST = "0.0.0.0"
        # Avvio del Server
        self.ns = NameServer()

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.resize(400, 100)
        self.setWindowTitle("Impostazione numero hosts")
        self.move(400, 250)

        self.label = QtGui.QLabel("Numero di hosts?", self)
        self.label.resize(150, 40)
        self.label.move(150, 10)

        self.textbox = QtGui.QLineEdit(self)
        self.textbox.resize(125, 30)
        self.textbox.move(140, 50)
        self.textbox.returnPressed.connect(self.open_main_window)

        #Settaggio dell'espressione regolare che prevede solo numeri (0-9), da 1 fino a massimo 8
        self.regular_expression = QtCore.QRegExp('^[1-8]{1}$')
        self.validator = QtGui.QRegExpValidator(self.regular_expression)
        self.textbox.setValidator(self.validator)

        self.textbox.textChanged.connect(self.textbox_validation)
        self.textbox.textChanged.emit(self.textbox.text())

        self.hcw = None
        # Faccio partire il server
        #s = Server()
        #s.start_ns_loop()

    def open_main_window(self):

        self.hcw = HostsConnectionWindow()
        self.hcw.set_hosts_number(self.get_hosts_number())
        self.hcw.show()
        self.hide()

    def textbox_validation(self):

        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QtGui.QValidator.Acceptable:
             # Green
            color = '#c4df9b'
            #print("Correct")
        else:
            # Red
            color = '#f6989d'
            #print("Incorrect")

        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def get_hosts_number(self):

        return self.textbox.text()

#=======================================================================================================================


class HostsConnectionWindow(Connection):

    def __init__(self):

        super(HostsConnectionWindow, self).__init__()

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
        self.setWindowTitle("Connessione hosts")

        self.identifiers = []

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

        self.taw = None

    def set_hosts_number(self, n_addresses):

        self.na = n_addresses

        for count in range(0, int(self.na)):
            self.identifiers.append(None)
            self.identifiers[count] = count

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
            self.textboxlist_addresses[count].setText(getpass.getuser() + "@" + socket.gethostname() + ".local")

            self.labellist_password[count].resize(self.labelwidth, self.labelheight)
            self.labellist_password[count].move(self.xpositionlabel_p, (self.offset_label * (count + 1)))

            self.textboxlist_password[count].setEchoMode(2)
            self.textboxlist_password[count].resize(self.textboxwidth, self.textboxheight)
            self.textboxlist_password[count].move(self.xpositiontextbox_p, (self.offset_textbox * (count + 1)))

        self.labelhost.setText("Numero di host su cui parallelizzare l'analisi: " + str(self.na))

    def open_text_analysis_window(self, identifiers, addresses, passwords):

        self.taw = TextAnalysisWindow(identifiers, addresses, passwords)
        self.taw.show()
        self.hide()

    def on_click_button_connect(self):

        t = []
        q = queue.Queue()

        idn = [self.na]
        addr = [self.na]
        psw = [self.na]

        for count in range(0, int(self.na)):
            t.append(
                threading.Thread(target=self.open_server_connection,
                                 args=[str(count), self.textboxlist_addresses[count].text(),
                                       self.textboxlist_password[count].text(), q]))
            idn[count] = str(count)
            addr[count] = self.textboxlist_addresses[count].text()
            psw[count] = self.textboxlist_password[count].text()
            t[count].start()
            time.sleep(1)
            t_ret_val = q.get()
            print(t_ret_val)
            print("\n")

        self.open_text_analysis_window(idn, addr, psw)


#=======================================================================================================================


class TextAnalysisWindow(Connection):

    def __init__(self, identifiers, addresses, passwords):

        super(TextAnalysisWindow, self).__init__()

        self.resize(1000, 680)
        self.move(125, 60)
        self.setWindowTitle("Analizzatore Testuale")

        self.loaded_file_textbox = QtGui.QLineEdit(self)
        self.loaded_file_textbox.resize(450, 30)
        self.loaded_file_textbox.move(20, 20)

        self.load_file_button = QtGui.QPushButton("Carica file", self)
        self.load_file_button.resize(100, 45)
        self.load_file_button.move(13, 70)

        QtCore.QObject.connect(self.load_file_button, QtCore.SIGNAL('clicked()'), self.load_file)

        self.loaded_file_textarea = QtGui.QTextEdit(self)
        self.loaded_file_textarea.resize(450, 550)
        self.loaded_file_textarea.move(520, 20)

        self.start_analysis_button = QtGui.QPushButton("Avvia Analisi", self)
        self.start_analysis_button.resize(250, 65)
        self.start_analysis_button.move(630, 600)

        self.identifiers = identifiers
        self.addresses = addresses
        self.passwords = passwords

        QtCore.QObject.connect(self.start_analysis_button, QtCore.SIGNAL('clicked()'), self.start_analysis)

    def load_file(self):

        self.loaded_file_textbox.setText(QtGui.QFileDialog.getOpenFileName())
        file_path = self.loaded_file_textbox.text()
        self.loaded_file_textarea.setText(self.read_file(file_path))

    def read_file(self, p1):
        #lettura del file
        in_file = open(p1, "r")
        file = in_file.read()
        in_file.close()
        return file

    def start_analysis(self):

        t = []
        q = queue.Queue()

        for count in range(0, int(self.na)):
            t.append(
                threading.Thread(target=self.find_obj,
                                 args=[self.identifiers[count], self.addresses[count],
                                       self.passwords[count], q]))
            t[count].start()
            time.sleep(1)
            t_ret_val = q.get()
            print(t_ret_val)
            print("\n")
