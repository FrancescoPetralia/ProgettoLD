__author__ = 'francesco'

import threading, socket, sys, Pyro4
from PyQt4 import QtGui, QtCore
from main_window import MainWindow
from server import Server
from connection import Connection


class SetHostsWindow(QtGui.QMainWindow):

    def __init__(self):

        super(SetHostsWindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        Pyro4.config.HOST = "0.0.0.0"

        self.resize(400, 100)
        self.setWindowTitle("Impostazione numero hosts")
        self.move(400, 250)

        self.label = QtGui.QLabel("Numero di hosts?", self)
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

        self.hcw = None
        # Faccio partire il server
        s = Server()
        s.start_ns_loop()

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
            print("Correct")
        else:
            # Red
            color = '#f6989d'
            print("Incorrect")

        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def get_hosts_number(self):

        return self.textbox.text()


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

    def open_text_analysis_window(self):

        self.taw = TextAnalysisWindow()
        self.taw.show()
        self.hide()

    def on_click_button_connect(self):

        #self.open_server_connection()
        if self.find_obj(0, self.textboxlist_addresses[0].text(), self.textboxlist_password[0].text()):
            print("Metodo .find_obj() eseguito correttamente.")
            self.open_text_analysis_window()
        else:
            print("Errore nell'esecuzione del metodo .find_obj()")
            self.open_text_analysis_window()


class TextAnalysisWindow(QtGui.QMainWindow):

    def __init__(self):

        super(TextAnalysisWindow, self).__init__()

        self.resize(900, 620)
        self.move(225, 60)
        self.setWindowTitle("Analizzatore Testuale")
