__author__ = 'francesco'

import os
#os.environ["PYRO_LOGFILE"] = "../log/pyro.log"
#os.environ["PYRO_LOGLEVEL"] = "DEBUG"
import threading
import socket
import Pyro4
import time
import paramiko
import datetime
import pygal
from PyQt4 import QtGui, QtCore
from name_server import NameServer
from connection import Connection
from file_splitter import FileSplitter
from execution_time_measurement import ExecutionTimeMeasurement
from results_collector import ResultsCollector

'''
Modulo che si occupa della gestione di tutte le finestre grafiche.
'''


class SetHostsWindow(QtGui.QMainWindow):

    '''
    In questa classe viene definita la finestra principale, in cui viene inserito il numero di host su cui
    parallelizzare l'analisi. Viene inoltre definito il menu tramite il quale è possibile selezionare la voce apposita
    per l'apertura del file d'aiuto, e per caricare una configurazione (contenente numero di host, indirizzi, file da
    analizzare) predefinita.
    '''

    def __init__(self):

        super(SetHostsWindow, self).__init__()

        Pyro4.config.HOST = "0.0.0.0"
        # Avvio del Server
        self.ns = NameServer()

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setFixedSize(400, 100)
        self.setWindowTitle("Impostazione numero hosts")
        self.move(400, 250)

        self.menu = QtGui.QMenuBar(self)
        self.menu_analizzatore = QtGui.QMenu("Analizzatore")
        self.menu_analizzatore_help_action = self.menu_analizzatore.addAction("Help")
        self.menu_analizzatore_help_action.triggered.connect(self.show_help)
        self.menu_analizzatore_load_config_file_action = self.menu_analizzatore.addAction("Carica configurazione")
        self.menu_analizzatore_load_config_file_action.triggered.connect(self.load_config_file)
        self.menu.addMenu(self.menu_analizzatore)

        self.label = QtGui.QLabel("Numero di hosts?", self)
        self.label.resize(150, 40)
        self.label.move(150, 10)

        self.textbox = QtGui.QLineEdit(self)
        self.textbox.resize(125, 30)
        self.textbox.move(140, 50)
        self.textbox.returnPressed.connect(self.open_main_window)
        self.textbox.setToolTip("Inserire il numero di host (min = 1, max = 8)")

        #Settaggio dell'espressione regolare che prevede solo numeri (0-9), da 1 fino a massimo 8
        self.regular_expression = QtCore.QRegExp('^[1-8]{1}$')
        self.validator = QtGui.QRegExpValidator(self.regular_expression)
        self.textbox.setValidator(self.validator)

        self.textbox.textChanged.connect(self.textbox_validation)
        self.textbox.textChanged.emit(self.textbox.text())

        self.hcw = None

    def open_main_window(self):
        '''
        Metodo collegato all'evento 'returnPressed' della textbox.
        Istanzio la classe HostConnectionWindow() in modo da fare aprire la finestra di connessione agli host remoti.
        Dopo l'istanziazione, viene richiamato il metodo set_hosts_number(), in modo da passare correttamente,
         all'istanza appena creata, il numero di host inserito nella textbox della finestra principale.
        '''

        self.hcw = HostsConnectionWindow(0, 0)
        self.hcw.set_hosts_number(self.get_hosts_number())
        self.hcw.show()
        self.hide()

    def textbox_validation(self):
        '''
        Metodo che si occupa della validazione dei dati immessi nella textbox.
        In particolare, se il contenuto della textbox non coincide con l'espressione regolare definita nel costruttore
        di questa classe, la textbox resta vuota finché non viene immesso un valore che coincide con essa.
        Inoltre, gestisce il render del background della textbox, sempre in base al match o meno dell'
        espressione regolare (verde per input corretto, rosso per input errato).
        In questo modo è possibile controllare l'esattezza dell'input della text box.
        L'espressione regolare ammette l'inserimento di un solo carattere, compreso tra 1 ed 8.
        '''

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
        '''
        Metodo che ritorna il numero di host inserito dall'utente, o caricato dal file di configurazione predefinito.
        :return: numero di hosts
        '''

        return self.textbox.text()

    def show_help(self):
        '''
        Metodo che permette la visualizzazione del file di help.
        Questo metodo è collegato all'evento 'triggered' del menu item 'Help'
        '''
        os.system('open ../doc/manuale_di_utilizzo.pdf')
        print("\nManuale di utilizzo caricato.")

    def load_config_file(self):
        '''
        Metodo che legge il file di configurazione.
        Questo metodo è collegato all'evento 'triggered' del menu item 'Carica configurazione'
        In particolare, dopo aver letto, riga per riga, il file di
        configurazione, imposto in modo corretto le variabili utili al passaggio dei dati di configurazione appena
        letti dal file.
        '''

        hosts_number, address, file, addresses, file_content = "", "", "", [], []

        try:
            file_path = str(QtGui.QFileDialog.getOpenFileName())


            f = open(file_path, 'r')
            file_content = f.read().splitlines()

            message = []
            message.append("/* File di configurazione, tramite il quale viene caricata una configurazione con un")
            message.append("numero di hosts, indirizzi, e file da analizzare, già predefiniti.")
            message.append("Attenersi a questo formato (numero di hosts, indirizzi, file da analizzare). */")

            cnt = 0
            for count in range(0, len(message)):
                if message[count] == file_content[count]:
                    cnt += 1

            if cnt != 3:
                raise Exception

            hosts_number = file_content[3]

            cnt = 3
            for count in range(0, int(hosts_number)):
                cnt += 1
                addresses.append(file_content[cnt])

            file = file_content[(len(file_content) - 1)]

            f.close()

            print("\nConfigurazione caricata dal file '" + file_path + "' (numero hosts, indirizzi, file):\n"
                  + "Numero di hosts: " + hosts_number + ". \nIndirizzi: " + str(addresses) + ". \nFile: '" + file + "'.")

            self.hcw = HostsConnectionWindow(1, 0)
            self.hcw.set_addresses(addresses)
            self.hcw.set_hosts_number(hosts_number)
            self.hcw.set_file(file)
            self.hcw.show()
            self.hide()

        except Exception as e:
            print("\nNon hai scelto nessun file di configurazione oppure il file non esiste o non è un file di "
                  "configurazione. Riprovare con un file adatto.")

#=======================================================================================================================


class HostsConnectionWindow(QtGui.QMainWindow):
    '''
    In questa classe viene definita la finestra di connessione agli hosts remoti.
    All'interno della finestra, sono presenti 2 textbox per host, in base al numero di hosts, nelle quali vengono
    inseriti, rispettivamente, gli indirizzi e le passworda degli hosts remoti a cui connettersi.
    Le textbox sono di base configurate con l'hostname di sistema, ma è comunque consentita la modifica del
    valore da parte dell'utente, in modo da poter inserire l'indirizzo desiderato.
    Questa classe gestisce inoltre il rendering grafico delle textboxes nel caso in cui la connessione agli hosts remoti
    avvenga con successo o meno.
    Al termine del corretto inserimento delle credenziali, si aprirà la finestra di analisi del testo.
    '''

    def __init__(self, flag_conf, flag_terminal):
        '''
        Definizione di tutte le variabili utili alla classe.
        :param flag_conf: questo flag specifica se è stato caricato o meno il file di configurazione, in modo da
        permettere alla finestra l'esecuzione di determinate azioni a seconda del valore del flag.
        :param flag_terminal: questo flag specifica se sono stati inseriti, da parte dell'utente, parametri da
        terminale (-n e -a, rispettivamente per il numero di hosts ed indirizzi degli hosts remoti), in modo da
        permettere alla finestra l'esecuzione di determinate azioni a seconda del valore del flag.
        '''

        super(HostsConnectionWindow, self).__init__()

        if flag_terminal == 1 or flag_conf == 1:
            Pyro4.config.HOST = "0.0.0.0"
            # Avvio del Server
            self.ns = NameServer()

            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        elif flag_terminal == 0:
            pass

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

        self.setFixedSize(790, 560)
        self.move(250, 85)
        self.setWindowTitle("Connessione hosts")

        self.labellist_addresses = []
        self.textboxlist_addresses = []

        self.labellist_password = []
        self.textboxlist_password = []

        self.button_go_back = QtGui.QPushButton("Indietro", self)
        self.button_go_back.resize(100, 45)
        self.button_go_back.move(552, 505)
        self.button_go_back.clicked.connect(self.go_back)
        self.button_go_back.setToolTip("Torna alla finestra precedente e reimposta il numero di host")

        self.button_proceed = QtGui.QPushButton("Procedi", self)
        self.button_proceed.resize(100, 45)
        self.button_proceed.move(639, 505)
        self.button_proceed.clicked.connect(self.on_click_button_proceed)
        self.button_proceed.setToolTip("Prosegui ed apri la finestra di analisi del testo")

        self.labelhosts = QtGui.QLabel("", self)
        self.labelhosts.resize(300, 30)
        self.labelhosts.move(40, 515)

        self.taw = None
        self.shw = None

        self.addresses = []
        self.file_path = None
        self.flag_c = flag_conf
        self.flag_t = flag_terminal

    def go_back(self):
        '''
        Metodo che definisce il comportamento del bottone 'Indietro', usato per riconfigurare il numero di host senza
        dover chiudere l'applicazione.
        Nello specifico, nel momento in cui questo bottone viene cliccato, viene chiusa la finestra corrente, e
        riaperta la finestra principale.
        '''

        self.hide()
        self.shw = SetHostsWindow()
        self.shw.show()
        # Richiamare il metodo che termina il Name Server

    def load_config_file(self, conf_file):
        '''
        Metodo che legge il file di configurazione.
        Questo metodo è collegato all'evento 'triggered' del menu item 'Carica configurazione'
        In particolare, dopo aver letto, riga per riga, il file di
        configurazione, imposto in modo corretto le variabili utili al passaggio dei dati di configurazione appena
        letti dal file.
        '''

        hosts_number, address, file, addresses, file_content = "", "", "", [], []

        try:
            file_path = conf_file

            f = open(file_path, 'r')
            file_content = f.read().splitlines()

            message = []
            message.append("/* File di configurazione, tramite il quale viene caricata una configurazione con un")
            message.append("numero di hosts, indirizzi, e file da analizzare, già predefiniti.")
            message.append("Attenersi a questo formato (numero di hosts, indirizzi, file da analizzare). */")

            cnt = 0
            for count in range(0, len(message)):
                if message[count] == file_content[count]:
                    cnt += 1

            if cnt != 3:
                raise Exception

            hosts_number = file_content[3]

            cnt = 3
            for count in range(0, int(hosts_number)):
                cnt += 1
                addresses.append(file_content[cnt])

            file = file_content[(len(file_content) - 1)]

            f.close()

            print("\nConfigurazione caricata dal file '" + file_path + "' (numero hosts, indirizzi, file):\n"
                  + "Numero di hosts: " + hosts_number + ". \nIndirizzi: " + str(addresses) + ". \nFile: '" + file
                  + "'.")

            self.set_addresses(addresses)
            self.set_hosts_number(hosts_number)
            self.set_file(file)

        except Exception as e:
            print("\nNon hai scelto nessun file di configurazione oppure il file non esiste o non è un file di "
                  "configurazione. Riprovare con un file adatto.")

    def set_file(self, file):
        '''
        Metodo che si occupa del settaggio del file di configurazione, ricevuto dalla finestra principale, e che sarà
        poi passato alla finestra che si occuperà dell'analisi testuale.
        :param file: file di configurazione caricato dall'utente.
        '''

        self.file_path = file

    def set_addresses(self, addr):
        '''
        Metodo che si occupa del settaggio degli indirizzi ricevuti dalla finestra
        principale.
        Gli indirizzi ricevuti possono arrivare solamente nei seguenti modi:
        1) Leggendo il file di configurazione.
        2) Tramite l'apposito parametro -a passato come argomento nel terminale.
        :param addr: lista contenente gli indirizzi degli hosts remoti a cui connettersi.
        '''

        self.addresses = addr

    def set_hosts_number(self, n_addresses):
        '''
        Metodo che si occupa del settaggio delle textbox degli hosts remoti, in base al parametro in ingresso.
        Vengono inoltre gestite le proprietà grafiche delle textboxes, come la posizione, dimensione, tipologia
        (plain text o password) e contenuto.
        :param n_addresses: numero di indirizzi correlati al numero di hosts remoti.
        '''

        self.host_number = n_addresses

        for count in range(0, int(self.host_number)):
            self.labellist_addresses.append(QtGui.QLabel("Indirizzo Host_" + str(count) + ":", self))
            self.textboxlist_addresses.append(QtGui.QLineEdit(self))
            self.labellist_password.append(QtGui.QLabel("Password Host_" + str(count) + ":", self))
            self.textboxlist_password.append(QtGui.QLineEdit(self))

        for count in range(0, int(self.host_number)):

            self.labellist_addresses[count].resize(self.labelwidth, self.labelheight)
            self.labellist_addresses[count].move(self.xpositionlabel_a, (self.offset_label * (count + 1)))

            self.textboxlist_addresses[count].resize(self.textboxwidth, self.textboxheight)
            self.textboxlist_addresses[count].move(self.xpositiontextbox_a, (self.offset_textbox * (count + 1)))
            self.textboxlist_addresses[count].returnPressed.connect(self.on_click_button_proceed)

            if self.flag_c == 1:

                self.textboxlist_addresses[count].setText(self.addresses[count])
            elif self.flag_c == 0:

                if self.flag_t == 1:
                    self.textboxlist_addresses[count].setText(self.addresses[count])
                elif self.flag_t == 0:
                    self.textboxlist_addresses[count].setText("")

            self.labellist_password[count].resize(self.labelwidth, self.labelheight)
            self.labellist_password[count].move(self.xpositionlabel_p, (self.offset_label * (count + 1)))

            self.textboxlist_password[count].setEchoMode(2)
            self.textboxlist_password[count].resize(self.textboxwidth, self.textboxheight)
            self.textboxlist_password[count].move(self.xpositiontextbox_p, (self.offset_textbox * (count + 1)))
            self.textboxlist_password[count].returnPressed.connect(self.on_click_button_proceed)

        self.labelhosts.setText("Numero di host su cui parallelizzare l'analisi: " + str(self.host_number) + ".")

    def password_validation(self, addrs, pwds):
        '''
        Metodo che gestisce la validazione delle credenziali d'accesso.
        Nello specifico, viene effettuata una connessione di prova agli indirizzi specificati, in modo da verificare la
        correttezza delle credenziali d'accesso inserite dall'utente.
        Viene inoltre gestito il rendering grafico delle textboxes sia nel caso in cui la validazione abbia
        avuto successo, sia che la validazione abbia riscontrato degli errori.
        Per aiutare ulteriormente l'utente all'individuzione dell'errore, vengono mostrate nella finestra delle
        finestre di dialog in cui si comunica in quale hosts sono sate riscontrate credenziali daccesso non valide.
        :param addrs: lista contenente gli indirizzi degli hosts remoti.
        :param pwds: lista contenente le passwords degli host remoti.
        :return: True nel caso in cui le credenziali d'accetto siano corrette, False nel caso in cui le credenziali
        d'accesso siano sbagliate.
        '''

        print("\n")

        green_style = 'QLineEdit { border-style: solid; border-width: 2px; border-color: %s }' % '#c4df9b'
        red_style = 'QLineEdit { border-style: solid; border-width: 2px; border-color: %s }' % '#f6989d'

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
                self.textboxlist_addresses[count].setStyleSheet(green_style)
                self.textboxlist_password[count].setStyleSheet(green_style)
                print("Host " + str(count) + ": credenziali corrette.")

            except (paramiko.AuthenticationException, OSError, socket.gaierror):

                self.textboxlist_addresses[count].setStyleSheet(red_style)
                self.textboxlist_password[count].setStyleSheet(red_style)
                self.textboxlist_password[count].setFocus(True)
                print("Host_" + str(count) + ": credenziali errate.")
                QtGui.QMessageBox.about(self, "Credenziali Errate", "Host_" + str(count) + ": credenziali errate.")

        print("\n")

        if cnt == int(self.host_number):
            return True
        else:
            return False

    def open_text_analysis_window(self, identifiers, addresses, passwords, hosts):
        '''
        Metodo che si occupa dell'apertura della finestra di analisi.
        Nello specifico, viene istanziata la classe TextAnalysisWindow, alla quale vengono passati tutti i parametri
        relativi agli hosts remoti a cui connettersi (ids, indirizzi, passwords, numero di hosts).
        :param identifiers: lista contenente l'id ci ciascun host.
        :param addresses: lista contenente l'indirizzo di ciascun host.
        :param passwords: lista contenente la password di ciascun host.
        :param hosts: numero di hosts.
        '''

        if self.flag_c == 0:

            self.taw = TextAnalysisWindow(identifiers, addresses, passwords, hosts, None, 0)
            self.taw.show()
            self.hide()

        elif self.flag_c == 1:

            self.taw = TextAnalysisWindow(identifiers, addresses, passwords, hosts, self.file_path, 1)
            self.taw.show()
            self.hide()

    def on_click_button_proceed(self):
        '''
        Metodo collegato all'evento 'clicked' e 'returnPressed' rispettivamente del bottone 'Procedi' e
        passwords textboxes.
        Quando vengono scatenati questi due eventi, viene aperta la finestra di analisi testuale.
        '''

        ids = []
        addrs = []
        pwds = []

        for count in range(0, int(self.host_number)):

            ids.append(count)
            addrs.append(self.textboxlist_addresses[count].text())
            pwds.append(self.textboxlist_password[count].text())

        if self.password_validation(addrs, pwds):
            self.open_text_analysis_window(ids, addrs, pwds, int(self.host_number))
        else:
            pass

#=======================================================================================================================


class TextAnalysisWindow(Connection):
    '''
    Classe che si occupa della gestione della finestra di analisi testuale.
    Eredita dalla classe Connection, in modo da definirne un'istanza e disporre di tutti i metodi necessari per il
    networking con gli host remoti, tramite ssh e sftp, ed il PyRO NameServer.
    In questa finestra è possibile usufruire
    di numerose funzionalità grafiche, tra cui:
    - Selezionare a piacimento un file da analizzare.
    - Salvare l'attuale configurazione.
    - Caricare il file di help.
    - Visualizzare il contenuto del file su cui si desidera effettuare l'analisi tetuale, ed altre informazioni
    relative ad esso.
    - Visualizzare i risultati dell'analisi testuale.
    - Connettersi agli host remoti.
    - Avviare l'analisi.
    - Salvare l'analisi
    - Generare i grafici relativi all'analisi.
    - Ricerca interattiva delle occorrenze di una parola, frase o carattere.
    '''

    def __init__(self, identifiers, addresses, passwords, hosts, file, flag_conf):
        '''
        Definizione di tutte le variabili utili alla classe.
        Questo costruttore riceve dalla finestra precedente tutti i parametri utili all'autenticazione, connessione
        al NameServer (per trovare e far eseguire i PyRO Remote Objects) e alle operazioni relative al file da
        analizzare.
        :param identifiers: lista contenente gli id degli hosts remoti.
        :param addresses: lista contenente gli indirizzi degli hosts remoti.
        :param passwords: lista contenente le passwords degli hosts remoti.
        :param hosts: numero di hosts su cui parallelizzare l'analisi.
        :param file: file da caricare (specificato nel file di configurazione).
        :param flag_conf: flag che determina se è stato selezionato il file di configurazione.
        Se il flag è 0, significa che non è stato caricato nessun file di configurazione, e pertanto l'utente dovrà
        scegliere manualmente, tramite un file chooser, il file testuale da analizzare. Se, invece, il flag assume
        valore uguale a 1, significa che è stato caricato un file di configurazione, e pertanto ilprogramma carichrà
        in automatico il file specificato all'interno del file di configurazione.
        '''

        super(TextAnalysisWindow, self).__init__()

        self.hosts_number = hosts
        self.default_conf_file_path = file
        self.flag_c = flag_conf

        self.setFixedSize(1020, 710)
        self.move(125, 30)
        self.setWindowTitle("Analizzatore Testuale")

        self.menu = QtGui.QMenuBar(self)
        self.menu_analizzatore = QtGui.QMenu("Analizzatore")
        self.menu_analizzatore_help_action = self.menu_analizzatore.addAction("Help")
        self.menu_analizzatore_help_action.triggered.connect(self.show_help)
        self.menu_analizzatore_save_config_file_action = self.menu_analizzatore.addAction("Salva configurazione")
        self.menu_analizzatore_save_config_file_action.setEnabled(False)
        self.menu_analizzatore_save_config_file_action.triggered.connect(self.save_config_file)
        self.menu.addMenu(self.menu_analizzatore)
        self.menu_file = QtGui.QMenu("File")
        self.menu_file_load_file_action = self.menu_file.addAction("Carica File")
        self.menu.addMenu(self.menu_file)
        self.menu_file_load_file_action.triggered.connect(self.load_file)

        self.file_path = ""
        self.file_size_stat_info = None

        self.file_size_label = QtGui.QLabel("Dimensione del file da analizzare: 0 bytes.", self)
        self.file_size_label.resize(500, 20)
        self.file_size_label.move(20, 20)

        self.loaded_file_label = QtGui.QLabel("Contenuto del file da analizzare:", self)
        self.loaded_file_label.resize(450, 20)
        self.loaded_file_label.move(520, 20)

        self.loaded_file_textarea = QtGui.QTextEdit(self)
        self.loaded_file_textarea.resize(470, 550)
        self.loaded_file_textarea.move(520, 50)
        self.loaded_file_textarea.setReadOnly(True)

        self.search_label = QtGui.QLabel("Ricerca nel testo:", self)
        self.search_label.resize(300, 20)
        self.search_label.move(20, 60)
        self.search_label.setToolTip("Ricerca un carattere o una parole nel testo")

        self.search_textbox = QtGui.QLineEdit(self)
        self.search_textbox.resize(200, 30)
        self.search_textbox.move(20, 90)
        self.search_textbox.returnPressed.connect(self.search_and_highlight)

        self.searched_string_occurrences_label = QtGui.QLabel(self)
        self.searched_string_occurrences_label.resize(300, 20)
        self.searched_string_occurrences_label.move(230, 97)

        self.results_label = QtGui.QLabel("Risultato dell'analisi:", self)
        #self.palette = QtGui.QPalette()
        #self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
        #self.results_label.setPalette(self.palette)
        self.results_label.resize(200, 30)
        self.results_label.move(200, 140)

        self.left_separator = QtGui.QFrame(self)
        self.left_separator.setFrameShape(QtGui.QFrame.HLine)
        self.left_separator.setFrameShadow(QtGui.QFrame.Sunken)
        self.left_separator.resize(170, 2)
        self.left_separator.move(20, 150)

        self.right_separator = QtGui.QFrame(self)
        self.right_separator.setFrameShape(QtGui.QFrame.HLine)
        self.right_separator.setFrameShadow(QtGui.QFrame.Sunken)
        self.right_separator.resize(180, 2)
        self.right_separator.move(322, 150)

        self.final_result_textarea = QtGui.QTextEdit(self)
        self.final_result_textarea.resize(483, 420)
        self.final_result_textarea.move(20, 180)
        self.final_result_textarea.setReadOnly(True)

        self.save_final_result_button = QtGui.QPushButton("Salva Risultati", self)
        self.save_final_result_button.resize(253, 65)
        self.save_final_result_button.move(14, 595)
        self.save_final_result_button.clicked.connect(self.save_results)
        self.save_final_result_button.setEnabled(False)
        self.save_final_result_button.setToolTip("Salva i risultati dell'analisi dentro '../res/text_analysis_result.txt'")

        self.generate_graph_button = QtGui.QPushButton("Genera Grafici", self)
        self.generate_graph_button.clicked.connect(self.set_graph_state)
        self.generate_graph_button.resize(254, 65)
        self.generate_graph_button.move(255, 595)
        self.generate_graph_button.setEnabled(False)
        self.generate_graph_button.setToolTip("Genera l'istogramma ed il grafico a torta delle  20 parole e dei "
                                              "20 caratteri più utilizzati, dentro cartella ../res/")

        self.hosts_connection_button = QtGui.QPushButton("Connetti Hosts", self)
        self.hosts_connection_button.resize(247, 65)
        self.hosts_connection_button.move(514, 595)
        self.hosts_connection_button.clicked.connect(self.remote_object_connection)
        self.hosts_connection_button.setEnabled(False)
        self.hosts_connection_button.setToolTip("Connetti gli host locali o remoti")

        self.start_analysis_button = QtGui.QPushButton("Avvia Analisi", self)
        self.start_analysis_button.resize(248, 65)
        self.start_analysis_button.move(748, 595)
        self.start_analysis_button.clicked.connect(self.start_analysis)
        self.start_analysis_button.setEnabled(False)
        self.start_analysis_button.setToolTip("Avvia l'analisi del testo")

        self.button_go_back = QtGui.QPushButton("Indietro", self)
        self.button_go_back.resize(100, 45)
        self.button_go_back.move(4, 665)
        self.button_go_back.clicked.connect(self.go_back)
        self.button_go_back.setToolTip("Torna indietro per riconfigurare gli host locali o remoti")

        self.analysis_time_label = QtGui.QLabel(self)
        self.analysis_time_label.resize(480, 20)
        self.analysis_time_label.move(520, 665)

        self.identifiers = identifiers
        self.addresses = addresses
        self.passwords = passwords

        self.read_text = None

        self.hcw = None
        self.rc = None

        self.results = None
        self.results_number = None

        # Mi serve per controllare gli stati della finestra
        self.window_status = 0

        if self.flag_c == 1:

            self.read_text = self.read_file(self.default_conf_file_path)
            self.loaded_file_textarea.setText(self.read_text)
            self.loaded_file_textarea.setToolTip("Percorso del file: " + self.default_conf_file_path)
            self.file_size_stat_info = os.stat(self.default_conf_file_path)
            self.file_size_label.setText("Dimensione del file da analizzare: " +
                                         str(self.file_size_stat_info.st_size) + " bytes.")
            print("\nFile caricato correttamente.")

            # Se lo split è avvenuto correttamente, abilita la connessione
            if self.split_file():
                self.hosts_connection_button.setEnabled(True)
                self.menu_analizzatore_save_config_file_action.setEnabled(True)
                self.menu_file_load_file_action.setEnabled(False)
        else:
            pass

    def show_help(self):
        '''
        Metodo che permette la visualizzazione del file di help.
        Questo metodo è collegato all'evento 'triggered' del menu item 'Help'
        '''
        os.system('open ../doc/manuale_di_utilizzo.pdf')
        print("\nManuale di utilizzo caricato.")

    def save_config_file(self):
        '''
        Metodo che si occupa del salvataggio, dentro la cartella ../res/ del progetto, della configurazione attuale
        dell'applicazione (numero di hosts, indirizzi degli hosts remoti e file analizzato).
        Il file salvato segue questo tipo di nomenclatura, es.: conf_19112014_135726.conf, ovver conf_ seguito dal
        giorno, mese, anno, seguito da ora, minuti e secondi, seguito dall'estensione .conf.
        Questo per differenziare le configurazioni salvate e permettere all'utente una migliore identificazione di esse.
        '''

        now = datetime.datetime.now()

        d_m_y = "_" + str(now.day) + str(now.month) + str(now.year) + "_"
        h_m_s = str(now.hour) + str(now.minute) + str(now.second)

        file_path = "../conf/conf" + d_m_y + h_m_s + ".conf"

        message = "/* File di configurazione, tramite il quale viene caricata una configurazione con un\nnumero di " \
                  "hosts, indirizzi, e file da analizzare, già predefiniti.\nAttenersi a questo formato " \
                  "(numero di hosts, indirizzi, file da analizzare). */\n"

        try:
            f = open(file_path, 'w')
            f.write(message)
            f.write(str(self.hosts_number) + "\n")
            for elements in self.addresses:
                f.write(elements + "\n")
            f.write(self.file_path)

            print("\nConfigurazione salvata nel file: " + file_path)
            QtGui.QMessageBox.about(self, "Configurazione salvata", "Configurazione salvata nel file: " + file_path)
        except Exception as e:
            print("\nErrore durante il salvataggio della configurazione.")
            QtGui.QMessageBox.about(self, "Errore nel salvataggio",
                                    "Errore durante il salvataggio della configurazione.")

    def go_back(self):
        '''
        Metodo che definisce il comportamento del bottone 'Indietro', usato per tornare alla finestra di connessione
        agli hosts remoti senza dover chiudere l'applicazione.
        Nello specifico, nel momento in cui questo bottone viene cliccato, viene chiusa la finestra corrente, e
        riaperta la finestra di connessione agli hosts remoti.
        Da notare che alla riapertura della finestra di connessione saranno settati gli hostname di sistema.
        '''

        self.hide()
        self.hcw = HostsConnectionWindow(0, 0)
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
        '''
        Metodo che si occupa del caricamento del file su cui si vuole eseguire l'analisi testuale.
        Nello specifico, se flag_c, cioè quello relativo al caricamento o meno del file di configurazione, assume valore
        0, significa che non è stato caricato alcun file di configurazione, per cui sarà data, all'utente, la
        possibilità di scegliere il file da analizzare tramite un file chooser. Altrimenti, il programma imposterà
        automaticamente il file da analizzato, in base a quanto specificato sul file di configurazione.
        '''

        try:

            if self.flag_c == 0:

                self.file_path = str(QtGui.QFileDialog.getOpenFileName())
                self.read_text = self.read_file(self.file_path)
                self.loaded_file_textarea.setText(self.read_text)
                self.loaded_file_textarea.setToolTip("Percorso del file: " + self.file_path)
                self.file_size_stat_info = os.stat(self.file_path)
                self.file_size_label.setText("Dimensione del file da analizzare: " +
                                             str(self.file_size_stat_info.st_size) + " bytes.")
                print("\nFile caricato correttamente.")
            else:
                pass

            # Se lo split è avvenuto correttamente, abilita la connessione
            if self.split_file():
                self.hosts_connection_button.setEnabled(True)
                self.menu_analizzatore_save_config_file_action.setEnabled(True)
                self.menu_file_load_file_action.setEnabled(False)

        except Exception as e:

            print("\nNon è stato selezionato nessun file, oppure il seguente file/directory non esiste.")
            QtGui.QMessageBox.about(self, "Errore durante la selezione del file", "Non è stato selezionato nessun file, "
                                                                                  "oppure il seguente file/directory "
                                                                                  "non esiste.")

    def read_file(self, p1):
        '''
        Metodo che si occupa della lettura su file.
        :param p1: percorso del file da legere.
        :return: Il contenuto letto dal file.
        '''

        #Lettura del file
        in_file = open(p1, "r")
        file = in_file.read()
        in_file.close()
        return file

    def check_before_split(self):
        '''
        Questo metodo esegue un controllo prima di far partire il file splitter, in modo da bilanciare il carico di
        lavoro.
        Nello specifico, conto quante linee contiene il file, e le confronto col numero di hosts su cui si vuole
        eseguire l'analisi. Se le righe contenute nel file sono maggiori o uguali al numero di hosts, non esiste il
        pericolo di un carico di lavoro sbilanciato, mentre se le righe contenute nel file sono minori del numero
        di hosts, quest'ultimo assume lo stesso valore del numero di righe, in modo da bilanciare il carico di lavoro.
        '''

        if self.flag_c == 0:
            pass
        elif self.flag_c == 1:
            self.file_path = self.default_conf_file_path

        f = open(self.file_path, "r")
        file_content = f.read().splitlines()
        f.close()
        total_file_lines = 0
        for elements in range(0, len(file_content)):
            total_file_lines += 1

        if total_file_lines < self.hosts_number:

            self.hosts_number = total_file_lines

            print("Il file ha meno righe rispetto al numero di host a cui collegarsi,\n"
                  "per cui il software imposterà automaticamente il numero di host, in modo da bilanciare il carico\n"
                  "di lavoro.")
            QtGui.QMessageBox.about(self, "Avviso", "Il file ha meno righe rispetto al numero di host a cui collegarsi, "
                                                    "per cui il software imposterà automaticamente il numero di host, "
                                                    "in modo da bilanciare il carico di lavoro.")

    def split_file(self):
        '''
        Metodo che istanzia un oggetto di tipo FileSplitter(), passandogli come parametri il numero di host, ed il file
        da analizzare.
        Una volta avvenuta l'istanziazione dell'oggetto, l'oggetto richiamada il suo metodo split_file_between_hosts()
        che si occuperà dello split del file in tanti file quanti sono gli host.
        :return: True nel caso in cui lo split del file tra gli hosts sia avvenuto con successo.
        '''

        self.check_before_split()

        fs = FileSplitter(self.hosts_number, self.file_path)

        if fs.split_file_between_hosts():
            self.window_status = 1
            return True

    def remote_object_connection(self):
        '''
        Metodo che si occupa di creare una lista di thread che andranno ad eseguire il metodo start_connection().
        Viene inoltre istanziata la classe ResultsCollector, che si occupa del raccoglimento dei risultati dei PyRO
        objects. A ResultsCollector vengono passati i seguenti parametri: text_analyzer, ereditato dalla classe madre
        Connection, che è una lista contenente tutti i PyRO Object trovati sul NameServer, ed il numero di hosts.
        '''

        t = []

        for count in range(0, int(self.hosts_number)):

            t.append(threading.Thread(target=self.start_connection,
                                      args=[self.identifiers[count], self.addresses[count], self.passwords[count]]))
            time.sleep(2)
            t[count].start()
            time.sleep(1)
            self.setWindowTitle("Analizzatore Testuale - " + str(count + 1) + " host collegati.")

        self.window_status = 2
        time.sleep(12)
        self.hosts_connection_button.setEnabled(False)
        self.menu_file_load_file_action.setEnabled(False)
        self.start_analysis_button.setEnabled(True)

        self.rc = ResultsCollector(self.text_analyzer, self.hosts_number)

    def start_connection(self, identifier, address, password):
        '''
        Questo metodo richiama open_server_connection() e  find_remote_object(), ereditati dalla classe Connection(),
        passando gli id, indirizzi e passwords degli host, entrambi appartenenti alla classe, in modo da avviare la
        connessione via ssh agli host remoti, autenticarsi e trasferire i file encessari via sftp.
        :param identifier: lista contenente gli id degli hosts.
        :param address: lista contenente gli indirizzi degli hosts.
        :param password: lista contenente le password degli hosts.
        '''

        self.open_server_connection(identifier, address, password)
        time.sleep(1)
        self.find_remote_object(identifier, address, password)

    def search_and_highlight(self):
        '''
        Metodo che si occupa della ricerca e dell'evidenziazione della stringa ricercata nel testo.
        In particolare, con l'ausilio di una regexp, che è a tutti gli effetti la stringa che si vuole cercare, vengono
        trovate tutte le occorrenze presenti nel testo, evidenziandole.
        Inoltre viene gestito il render della textbox di ricerca nel caso in cui venga trovato un match (il bordo della
        textbox diventa verde), sia nel caso in cui non venga trovato alcun match (il bordo della
        textbox diventa rosso).
        '''

        green_style = 'QLineEdit { border-style: solid; border-width: 2px; border-color: %s }' % '#c4df9b'
        red_style = 'QLineEdit { border-style: solid; border-width: 2px; border-color: %s }' % '#f6989d'

        try:
            string_to_search = self.search_textbox.text()
            print("\nCerco '" + string_to_search + "' nel testo...")

            self.loaded_file_textarea.setText(self.read_text)
            cursor = self.loaded_file_textarea.textCursor()
            text_format = QtGui.QTextCharFormat()
            text_format.setBackground(QtGui.QBrush(QtGui.QColor("#91cbf0")))
            pattern = string_to_search

            if pattern == "":
                print("Non hai inserito niente nel campo di ricerca. ")
                QtGui.QMessageBox.about(self, "Attenzione", "Non hai inserito niente nel campo di ricerca.")
                self.search_textbox.setStyleSheet(red_style)
                raise Exception("Non hai inserito niente nel campo di ricerca.")

            regex = QtCore.QRegExp(pattern)
            pos, cnt = 0, 0
            index = regex.indexIn(self.loaded_file_textarea.toPlainText(), pos)
            while index != -1:
                cnt += 1
                cursor.setPosition(index)
                cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)
                cursor.mergeCharFormat(text_format)
                pos = index + regex.matchedLength()
                index = regex.indexIn(self.loaded_file_textarea.toPlainText(), pos)

            if cnt > 0:
                print("'" + string_to_search + "' è presente nel testo " + str(cnt) + " volte.")
                self.searched_string_occurrences_label.setText(str(cnt) + " occorrenze trovate.")
                self.search_textbox.setStyleSheet(green_style)
            elif cnt == 0:
                print("'" + string_to_search + "' non è presente nel testo.")
                self.searched_string_occurrences_label.setText(str(cnt) + " occorrenze trovate.")
                self.search_textbox.setStyleSheet(red_style)
        except:
            pass

    def start_analysis(self):
        '''
        Questo metodo richiama i metodi della classe FileSplitter che si occupano del raccoglimento dei risultati
        parziali dei PyRO objects e della produzione del risultato finale, che sarà poi visualizzato all'interno
        della finestra.
        '''

        print("\nAnalisi in corso...")

        self.final_result_textarea.clear()
        self.final_result_textarea.setText("Analisi eseguita su " + str(self.hosts_number) + " host.\n")

        try:
            e = ExecutionTimeMeasurement()
            e.start_measurement()

            self.rc.collect_all_results()

            e.finish_measurement()

            self.results = self.rc.get_final_result()

            self.results_number = (len(self.results) - 2)

            for count in range(0, self.results_number):
                self.final_result_textarea.append(self.results[count] + "\n")

            self.analysis_time_label.setText("Tempo impiegato per eseguire l'analisi testuale: "
                                             + str(e.get_measurement_interval()) + " secondi.")
            print("Tempo impiegato per eseguire l'analisi testuale: " + str(e.get_measurement_interval())
                  + " secondi.\n")
            self.save_final_result_button.setEnabled(True)
            self.generate_graph_button.setEnabled(True)
            QtGui.QMessageBox.about(self, "Analisi eseguita con successo", "Analisi eseguita con successo!\n\n"
                                                                           "Nota: alcuni risultati, "
                                                                           "come per esempio il numero di frasi, "
                                                                           "potrebbero variare in base al numero di "
                                                                           "hosts impostati.")

        except Exception as ex:

            if str(ex) == 'list index out of range':
                print("\nLa connessione agli host remoti  è ancora in corso..."
                      "\nPer favore aspetta ancora qualche secondo."
                      "\nSe la connessione impiega più del dovuto, premere 'Indietro' e ritentare la connessione.")
                QtGui.QMessageBox.about(self, "Credenziali Errate",
                                        "\nLa connessione agli host remoti  è ancora in corso..."
                                        "\n\nPer favore aspetta ancora qualche secondo."
                                        "\n\nSe la connessione impiega più del dovuto, premere 'Indietro' e ritentare "
                                        "la connessione.")
            else:
                print("Si è verificato un errore durante l'analisi del file." + str(ex))
                QtGui.QMessageBox.about(self, "Errore analisi", "Si è verificato un errore durante l'analisi del file."
                                                                "\n Premere 'Indietro' e ritentare la connessione.")

    def save_results(self):
        '''
        Metodo che salva il risultato dell'analisi su file.
        '''

        retval, message = self.rc.save()

        if retval:

            QtGui.QMessageBox.about(self, "Info salvataggio", message)
        else:

            QtGui.QMessageBox.about(self, "Errore nel salvataggio del file", message)

    def set_graph_state(self):
        '''
        Metodo che imposta lo stato dei grafici, ovvero, specifica, in base ad un flag, se il grafico da generare è
        quello relativo ai caratteri, oppure quello relativo alle parole, passando la relativa lista.
        '''

        self.generate_graph(self.rc.get_twenty_most_common_chars(), 'c')
        time.sleep(1)
        self.generate_graph(self.rc.get_twenty_most_common_words(), 'w')

    def generate_graph(self, l, fl):
        '''
        Metodo che genera i grafici (istogramma ed a torta) in base ai parametri ricevuti in ingresso.
        :param l: lista contenente i valori da rapresentare graficamente (carattere/occorrenza
        oppure parola/occorrenza)
        :param fl: flag che specifica il tipo di lista (lista dei caratteri o lista delle parole)
        '''

        my_list, flag = l, fl

        now = datetime.datetime.now()

        d_m_y = "_" + str(now.day) + str(now.month) + str(now.year) + "_"
        h_m_s = str(now.hour) + str(now.minute) + str(now.second)

        keys, values = [], []

        bar_chart = pygal.Bar()
        pie_chart = pygal.Pie()

        for key, val in my_list:
            keys.append(key)
            values.append(val)
            bar_chart.add(key, val)
            pie_chart.add(key, val)

        if flag == 'c':

            bar_chart.title = 'Istogramma dei 20 caratteri più utilizzati'
            pie_chart.title = 'Grafico a torta dei 20 caratteri più utilizzati'
            bar_chart.render_to_file('../res/chars_bar_chart' + d_m_y + h_m_s + '.svg')
            pie_chart.render_to_file('../res/chars_pie_chart' + d_m_y + h_m_s + '.svg')
            print('\nIstogramma dei caratteri  generato in: ../res/chars_bar_chart' + d_m_y + h_m_s + '.svg')
            print('Grafico a torta dei caratteri generato in: ../res/chars_bar_chart' + d_m_y + h_m_s + '.svg')
            QtGui.QMessageBox.about(self, "Grafici generati con successo",
                                    '\nIstogramma dei caratteri  generato in: ../res/chars_bar_chart'
                                    + d_m_y + h_m_s + '.svg' +
                                    '\nGrafico a torta dei caratteri generato in: ../res/chars_pie_chart'
                                    + d_m_y + h_m_s + '.svg')

        elif flag == 'w':

            bar_chart.title = 'Istogramma delle 20 parole più utilizzate'
            pie_chart.title = 'Grafico a torta delle 20 parole più utilizzate'
            bar_chart.render_to_file('../res/words_bar_chart' + d_m_y + h_m_s + '.svg')
            pie_chart.render_to_file('../res/words_pie_chart' + d_m_y + h_m_s + '.svg')
            print('\nIstogramma delle parole generato in: ../res/words_bar_chart' + d_m_y + h_m_s + '.svg')
            print('Grafico a torta delle parole generato in: ../res/words_pie_chart' + d_m_y + h_m_s + '.svg')

        paths = []
        paths.append('../res/chars_bar_chart' + d_m_y + h_m_s + '.svg')
        paths.append('../res/chars_pie_chart' + d_m_y + h_m_s + '.svg')
        paths.append('../res/words_bar_chart' + d_m_y + h_m_s + '.svg')
        paths.append('../res/words_pie_chart' + d_m_y + h_m_s + '.svg')

        for elements in paths:
            os.system('open ' + elements)

    def close_pyro_connection(self):
        '''
        Metodo che si occupa della chiusura in modo pulito della connessione con i PyRO objects.
        Nello specifico, viene chiusa la connessione ssh e vengono eliminati i file mandati precedentemente tramite sftp
        che, una volta chiusa la connessione, non servono più.
        Questo metodo viene chiamato alla chiusura della finestra.
        :return: True, nel caso in cui la connessione sia stata chiusa in modo corretto, altrimenti False.
        '''

        print('\nSto chiudendo la connessione con PyRO remote objects...')

        t = []

        for count in range(0, int(self.hosts_number)):
            t.append(threading.Thread(target=self.ssh_connection_close_and_cleanup,
                                      args=[self.identifiers[count], self.addresses[count], self.passwords[count]]))
            t[count].start()
            time.sleep(1)

        print("\nConnessione con i PyRO remote objects terminata.")

        return True

    def delete_local_files(self):
        '''
        Metodo che cancella i file locali temporanei presenti nella cartella ../temp del progetto.
        Questo metodo viene chiamato alla chiusura della finestra.
        '''

        print("\nSto eliminando i file locali...")

        try:
            for count in range(0, int(self.hosts_number)):
                os.remove("../temp/splitted_file_" + str(count) + ".txt")
                print("splitted_file_" + str(count) + ".txt rimosso.")

            print("\nFile locali eliminati con successo.")
        except Exception as e:
            print("\nErrore nell'eliminazione dei file locali." + str(e))

    def closeEvent(self, event):
        '''
        Override del metodo closeEvent della classe QtGui.QMainWindow, che intercetta la chiusura della finestra.
        In questo modo, oltre al comportamento di default di questo metodo, posso aggiungere altre direttive, utili
        al controllo dell'applicazione, migliorando ed estendendo il comportamento di base.
        :param event: Evento intercettato (SIG_INT o SIG_TERM).
        '''

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
