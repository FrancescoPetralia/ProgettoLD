__author__ = 'francesco'

import os
#os.environ["PYRO_LOGFILE"] = "pyro.log"
#os.environ["PYRO_LOGLEVEL"] = "DEBUG"
import threading
import socket
import getpass
import Pyro4
import time
import paramiko
from PyQt4 import QtGui, QtCore
from name_server import NameServer
from connection import Connection
from file_splitter import FileSplitter
from execution_time_measurement import ExecutionTimeMeasurement
from results_collector import ResultsCollector


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
        self.button_go_back.clicked.connect(self.go_back)

        self.button_proceed = QtGui.QPushButton("Procedi", self)
        self.button_proceed.resize(100, 45)
        self.button_proceed.move(639, 500)
        self.button_proceed.clicked.connect(self.on_click_button_proceed)

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
            self.labellist_addresses.append(QtGui.QLabel("Indirizzo Host_" + str(count) + ":", self))
            self.textboxlist_addresses.append(QtGui.QLineEdit(self))
            self.labellist_password.append(QtGui.QLabel("Password Host_" + str(count) + ":", self))
            self.textboxlist_password.append(QtGui.QLineEdit(self))

        self.textboxlist_password[int(self.host_number) - 1].returnPressed.connect(self.on_click_button_proceed)

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

    def password_validation(self, addrs, pwds):

        print("\n")

        ssh_connection = paramiko.SSHClient()
        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        cnt = 0
        for count in range(0, int(self.host_number)):

            try:
                if str(addrs[count]).__contains__('@'):
                    (username, hostname) = str(addrs[count]).split('@')
                    ssh_connection.connect(hostname, username=username, password=pwds[count], timeout=5, allow_agent=False)

                else:
                    ssh_connection.connect(str(addrs[count]), password=str(pwds[count]), timeout=5, allow_agent=False)

                ssh_connection.close()

                cnt = (cnt + 1)
                print("Host " + str(count) + ": credenziali corrette.")

            except (paramiko.AuthenticationException, OSError, socket.gaierror):
                print("Host_" + str(count) + ": credenziali errate.")

        print("\n")

        if cnt == int(self.host_number):
            return True
        else:
            return False

    def open_text_analysis_window(self, identifiers, addresses, passwords, hosts):

        self.taw = TextAnalysisWindow(identifiers, addresses, passwords, hosts)
        self.taw.show()
        self.hide()

    def on_click_button_proceed(self):

        ids = []
        addrs = []
        pwds = []

        for count in range(0, int(self.host_number)):

            ids.append(count)
            addrs.append(self.textboxlist_addresses[count].text())
            pwds.append(self.textboxlist_password[count].text())

        if self.password_validation(addrs, pwds):
            self.open_text_analysis_window(ids, addrs, pwds, self.host_number)
        else:
            pass

#=======================================================================================================================


class TextAnalysisWindow(Connection):

    def __init__(self, identifiers, addresses, passwords, hosts):

        super(TextAnalysisWindow, self).__init__()

        self.hosts_number = hosts

        self.resize(1020, 710)
        self.move(125, 30)
        self.setWindowTitle("Analizzatore Testuale")

        self.menu = QtGui.QMenuBar(self)
        self.menu_file = QtGui.QMenu("File")
        self.menu_file_action = self.menu_file.addAction("Carica File")
        self.menu.addMenu(self.menu_file)
        self.menu_file_action.triggered.connect(self.load_file)

        self.loaded_file_label = QtGui.QLabel("Percorso del file da analizzare:", self)
        self.loaded_file_label.resize(450, 20)
        self.loaded_file_label.move(20, 20)

        self.loaded_file_textbox = QtGui.QLineEdit(self)
        self.loaded_file_textbox.resize(450, 30)
        self.loaded_file_textbox.move(20, 50)
        self.loaded_file_textbox.setReadOnly(True)

        self.loaded_file_label = QtGui.QLabel("Contenuto del file da analizzare:", self)
        self.loaded_file_label.resize(450, 20)
        self.loaded_file_label.move(520, 20)

        self.loaded_file_textarea = QtGui.QTextEdit(self)
        self.loaded_file_textarea.resize(470, 550)
        self.loaded_file_textarea.move(520, 50)
        self.loaded_file_textarea.setReadOnly(True)

        self.search_label = QtGui.QLabel("Ricerca nel testo:", self)
        self.search_label.resize(450, 20)
        self.search_label.move(20, 100)

        self.search_textbox = QtGui.QLineEdit(self)
        self.search_textbox.resize(350, 30)
        self.search_textbox.move(20, 130)
        self.search_textbox.returnPressed.connect(self.search)

        self.results_label = QtGui.QLabel("Risultati dell'analisi:", self)
        self.results_label.resize(200, 30)
        self.results_label.move(200, 180)

        self.left_separator = QtGui.QFrame(self)
        self.left_separator.setFrameShape(QtGui.QFrame.HLine)
        self.left_separator.setFrameShadow(QtGui.QFrame.Sunken)
        self.left_separator.resize(170, 2)
        self.left_separator.move(20, 190)

        self.right_separator = QtGui.QFrame(self)
        self.right_separator.setFrameShape(QtGui.QFrame.HLine)
        self.right_separator.setFrameShadow(QtGui.QFrame.Sunken)
        self.right_separator.resize(180, 2)
        self.right_separator.move(322, 190)

        self.final_result_labels = []
        self.x_position = 20
        self.offset = 30

        self.hosts_connection_button = QtGui.QPushButton("Connetti Hosts", self)
        self.hosts_connection_button.resize(247, 65)
        self.hosts_connection_button.move(514, 595)
        self.hosts_connection_button.clicked.connect(self.remote_object_connection)
        self.hosts_connection_button.setEnabled(False)

        self.start_analysis_button = QtGui.QPushButton("Avvia Analisi", self)
        self.start_analysis_button.resize(248, 65)
        self.start_analysis_button.move(748, 595)
        self.start_analysis_button.clicked.connect(self.start_analysis)
        self.start_analysis_button.setEnabled(False)

        self.button_go_back = QtGui.QPushButton("Indietro", self)
        self.button_go_back.resize(100, 45)
        self.button_go_back.move(14, 655)
        self.button_go_back.clicked.connect(self.go_back)

        self.analysis_time_label = QtGui.QLabel(self)
        self.analysis_time_label.resize(480, 20)
        self.analysis_time_label.move(520, 665)

        self.identifiers = identifiers
        self.addresses = addresses
        self.passwords = passwords

        self.hcw = None

        # Mi serve per controllare gli stati della finestra
        self.window_status = 0

    def go_back(self):
        self.hide()
        self.hcw = HostsConnectionWindow()
        self.hcw.set_hosts_number(self.hosts_number)
        self.hcw.show()

        if self.window_status == 2:
            if self.close_pyro_connection():
                self.delete_local_files()
            else:
                self.delete_local_files()
        elif self.window_status == 1:
                self.delete_local_files()
        elif self.window_status == 0:
                pass

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
            self.window_status = 1
            return True

    def remote_object_connection(self):

        t = []

        for count in range(0, int(self.hosts_number)):
            t.append(threading.Thread(target=self.start_connection,
                                      args=[self.identifiers[count], self.addresses[count], self.passwords[count]]))
            time.sleep(1)
            t[count].start()
            time.sleep(1)

        self.window_status = 2
        time.sleep(10)
        self.start_analysis_button.setEnabled(True)

    def start_connection(self, identifier, address, password):

        self.open_server_connection(identifier, address, password)
        self.find_remote_object(identifier, address, password)

    def search(self):
        pass

    def set_final_result_labels(self, labels_number, results):

        for count in range(0, labels_number):
            self.final_result_labels.append(QtGui.QLabel(self))

        for count in range(0, labels_number):
            self.final_result_labels[count].resize(300, 30)
            self.final_result_labels[count].move(self.x_position, (190 + (self.offset * (count + 1))))
            self.final_result_labels[count].setText(results[count])
            self.final_result_labels[count].show()

    def start_analysis(self):

        try:
            e = ExecutionTimeMeasurement()
            e.start_measurement()

            rc = ResultsCollector(self.text_analyzer, self.hosts_number)
            rc.collect_all_results()

            e.finish_measurement()

            results = rc.get_final_result()
            labels_number = len(results)

            self.set_final_result_labels(labels_number, results)

            self.analysis_time_label.setText("Tempo impiegato per eseguire l'analisi testuale: " + str(e.get_measurement_interval()) + " secondi.")
            print("Tempo impiegato per eseguire l'analisi testuale: " + str(e.get_measurement_interval()) + " secondi.")

        except Exception as e:
            print("Errore nell'eseguire l'analisi: \n" + str(e))

    def close_pyro_connection(self):
        print("\nSto chiudendo la connessione con PyRO remote objects...")

        t = []

        for count in range(0, int(self.hosts_number)):
            t.append(threading.Thread(target=self.ssh_connection_close_and_cleanup,
                                      args=[self.identifiers[count], self.addresses[count], self.passwords[count]]))
            t[count].start()
            time.sleep(1)

        print("\nConnessione con i PyRO remote objects terminata.")

        return True

    def delete_local_files(self):
        print("\nSto eliminando i file locali...")

        for count in range(0, int(self.hosts_number)):
            os.remove("../txt/splitted_file_" + str(count) + ".txt")
            print("splitted_file_" + str(count) + ".txt rimosso.")

        print("\nFile locali eliminati con successo.")

    # Override di closeEvent della classe QtGui.QtMainWindow per intercettare la chiusura della finestra
    def closeEvent(self, event):

        QtGui.QMainWindow.closeEvent(self, event)

        if self.window_status == 2:
            if self.close_pyro_connection():
                self.delete_local_files()
            else:
                self.delete_local_files()
        elif self.window_status == 1:
                self.delete_local_files()
        elif self.window_status == 0:
                pass