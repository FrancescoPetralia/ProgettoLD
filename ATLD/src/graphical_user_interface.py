__author__ = 'francesco'

#import os
#os.environ["PYRO_LOGFILE"] = "pyro.log"
#os.environ["PYRO_LOGLEVEL"] = "DEBUG"
import threading
import socket
import getpass
import Pyro4
import time
import os
from PyQt4 import QtGui, QtCore
from main_window import MainWindow
from name_server import NameServer
from connection import Connection
from file_splitter import FileSplitter
from execution_time_measurement import ExecutionTimeMeasurement


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


class HostsConnectionWindow(QtGui.QMainWindow):

    def __init__(self):

        super(HostsConnectionWindow, self).__init__()

        self.host_number = 0
        self.offset_label = 55
        self.offset_textbox = 55
        self.xpositionlabel_a = 40
        self.xpositiontextbox_a = 170
        self.xpositionlabel_p = 430
        self.xpositiontextbox_p = 560
        self.labelheight = 30
        self.labelwidth = 150
        self.textboxheight = 30
        self.textboxwidth = 175

        self.resize(790, 560)
        self.move(250, 85)
        self.setWindowTitle("Connessione hosts")

        self.labellist_addresses = []
        self.textboxlist_addresses = []

        self.labellist_password = []
        self.textboxlist_password = []

        self.button_go_back = QtGui.QPushButton("Indietro", self)
        self.button_go_back.resize(100, 45)
        self.button_go_back.move(552, 500)
        QtCore.QObject.connect(self.button_go_back, QtCore.SIGNAL('clicked()'), self.go_back)

        self.button_proceed = QtGui.QPushButton("Procedi", self)
        self.button_proceed.resize(100, 45)
        self.button_proceed.move(639, 500)
        QtCore.QObject.connect(self.button_proceed, QtCore.SIGNAL('clicked()'), self.on_click_button_connect)

        self.labelhosts = QtGui.QLabel("", self)
        self.labelhosts.resize(300, 30)
        self.labelhosts.move(40, 515)

        self.taw = None
        self.shw = None

    def go_back(self):
        self.hide()
        self.shw = SetHostsWindow()
        self.shw.show()
        # Richiamare il metodo che termina il Name Server

    def set_hosts_number(self, n_addresses):

        self.host_number = n_addresses

        for count in range(0, int(self.host_number)):
            self.labellist_addresses.append(QtGui.QLabel("Indirizzo host " + str(count) + ":", self))
            self.textboxlist_addresses.append(QtGui.QLineEdit(self))
            self.labellist_password.append(QtGui.QLabel("Password host " + str(count) + ":", self))
            self.textboxlist_password.append(QtGui.QLineEdit(self))

            self.textboxlist_password[(len(self.textboxlist_password)) - 1].returnPressed.connect(self.on_click_button_connect)

        for count in range(0, int(self.host_number)):

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

        self.labelhosts.setText("Numero di host su cui parallelizzare l'analisi: " + str(self.host_number) + ".")

    def open_text_analysis_window(self, identifiers, addresses, passwords, hosts):

        self.taw = TextAnalysisWindow(identifiers, addresses, passwords, hosts)
        self.taw.show()
        self.hide()

    def on_click_button_connect(self):

        ids = []
        addrs = []
        pwds = []

        for count in range(0, int(self.host_number)):

            ids.append(count)
            addrs.append(self.textboxlist_addresses[count].text())
            pwds.append(self.textboxlist_password[count].text())

        self.open_text_analysis_window(ids, addrs, pwds, self.host_number)


#=======================================================================================================================


class TextAnalysisWindow(Connection):

    def __init__(self, identifiers, addresses, passwords, hosts):

        super(TextAnalysisWindow, self).__init__()

        self.hosts_number = hosts

        self.resize(1020, 710)
        self.move(125, 30)
        self.setWindowTitle("Analizzatore Testuale")

        self.loaded_file_label = QtGui.QLabel("Percorso del file da analizzare:", self)
        self.loaded_file_label.resize(450, 20)
        self.loaded_file_label.move(20, 20)

        self.loaded_file_textbox = QtGui.QLineEdit(self)
        self.loaded_file_textbox.resize(450, 30)
        self.loaded_file_textbox.move(20, 50)

        self.load_file_button = QtGui.QPushButton("Carica file", self)
        self.load_file_button.resize(100, 45)
        self.load_file_button.move(14, 90)
        QtCore.QObject.connect(self.load_file_button, QtCore.SIGNAL('clicked()'), self.load_file)

        self.loaded_file_label = QtGui.QLabel("Contenuto del file da analizzare:", self)
        self.loaded_file_label.resize(450, 20)
        self.loaded_file_label.move(520, 20)

        self.loaded_file_textarea = QtGui.QTextEdit(self)
        self.loaded_file_textarea.resize(470, 550)
        self.loaded_file_textarea.move(520, 50)

        self.hosts_connection_button = QtGui.QPushButton("Connetti Hosts", self)
        self.hosts_connection_button.resize(247, 65)
        self.hosts_connection_button.move(514, 595)
        QtCore.QObject.connect(self.hosts_connection_button, QtCore.SIGNAL('clicked()'), self.remote_object_connection)
        self.hosts_connection_button.setEnabled(False)

        self.start_analysis_button = QtGui.QPushButton("Avvia Analisi", self)
        self.start_analysis_button.resize(248, 65)
        self.start_analysis_button.move(748, 595)
        QtCore.QObject.connect(self.start_analysis_button, QtCore.SIGNAL('clicked()'), self.start_analysis)
        self.start_analysis_button.setEnabled(False)

        self.button_go_back = QtGui.QPushButton("Indietro", self)
        self.button_go_back.resize(100, 45)
        self.button_go_back.move(14, 650)
        QtCore.QObject.connect(self.button_go_back, QtCore.SIGNAL('clicked()'), self.go_back)

        self.identifiers = identifiers
        self.addresses = addresses
        self.passwords = passwords

        self.hcw = None
        self.results = None

    def go_back(self):
        self.hide()
        self.hcw = HostsConnectionWindow()
        self.hcw.set_hosts_number(self.hosts_number)
        self.hcw.show()
        # Richiamare il metodo per terminare i pid dei remote objects e l'unregister dal Name Server

    def load_file(self):

        self.loaded_file_textbox.setText(QtGui.QFileDialog.getOpenFileName())
        file_path = self.loaded_file_textbox.text()
        self.loaded_file_textarea.setText(self.read_file(file_path))

        if self.split_file():
            self.hosts_connection_button.setEnabled(True)

    def read_file(self, p1):

        #Lettura del file
        in_file = open(p1, "r")
        file = in_file.read()
        in_file.close()
        return file

    def split_file(self):

        fs = FileSplitter(self.hosts_number, self.loaded_file_textbox.text())

        if fs.split_file_between_hosts():
            return True

    def remote_object_connection(self):

        t = []

        for count in range(0, int(self.hosts_number)):
            t.append(threading.Thread(target=self.start_connection,
                                      args=[self.identifiers[count], self.addresses[count], self.passwords[count]]))
            t[count].start()
            time.sleep(1)

        self.start_analysis_button.setEnabled(True)

    def start_connection(self, identifier, address, password):

        self.open_server_connection(identifier, address, password)
        self.find_remote_object(identifier, address, password)

    def start_analysis(self):

        try:
            e = ExecutionTimeMeasurement()
            e.start_measurement()
            results = self.text_analyzer[0].get_results()
            e.finish_measurement()
            print("Tempo impiegato per eseguire l'analisi testuale: " + str(e.get_measurement_interval()) + " secondi.")
            self.close_pyro_connection()
            self.delete_local_files()
        except Exception as e:
            print("Errore nell'eseguire l'analisi: \n" + str(e))
            self.close_pyro_connection()
            self.delete_local_files()

    def close_pyro_connection(self):
        print("\nSto chiudendo la connessione con PyRO remote objects...")

        t = []

        for count in range(0, int(self.hosts_number)):
            t.append(threading.Thread(target=self.ssh_connection_close_and_cleanup,
                                      args=[self.identifiers[count], self.addresses[count], self.passwords[count]]))
            t[count].start()

        print("\nConnessione con i PyRO remote objects terminata.")

    def delete_local_files(self):
        print("\nSto eliminando i file locali...")

        for count in range(0, int(self.hosts_number)):
            os.remove("../txt/splitted_file_" + str(count) + ".txt")
            print("splitted_file_" + str(count) + ".txt rimosso.")

        print("\nFile locali eliminati con successo.")