__author__ = 'francesco'

#import os
#os.environ["PYRO_LOGFILE"] = "pyro.log"
#os.environ["PYRO_LOGLEVEL"] = "DEBUG"
import Pyro4
import paramiko
import socket
import time
from PyQt4 import QtCore, QtGui


class Connection(QtGui.QMainWindow):

    def __init__(self):

        super(Connection, self).__init__()

        self.text_analyzer_name = "Text_Analyzer_"
        self.text_analyzer = None
        self.object_pid = None

    def start(self, identifier, address, password):

        self.open_server_connection(identifier, address, password)
        self.find_remote_object(identifier, address, password)

    # Questo metodo ritorna l'indirizzo ip del server
    def get_ip_address(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = str(s.getsockname()[0])
        s.close()
        print(ip)
        return ip

    # Metodo che cerca l'oggetto sul server
    def find_remote_object(self, identifier, address, password):

        time.sleep(5)

        #if self.authentication_ok is True:

        try:
            ns = Pyro4.naming.locateNS()
            print("Return del locateNS(): " + str(ns))
            print("Cerco sul server l'oggetto " + self.text_analyzer_name + str(identifier) + "...")
            print(ns.list())
            uri_text_analyzer = ns.lookup(self.text_analyzer_name + str(identifier))
            print(self.text_analyzer_name + " trovato. Il suo uri è: " + uri_text_analyzer)
            self.text_analyzer = Pyro4.Proxy(uri_text_analyzer)
            print("\n")

        except Pyro4.errors.NamingError as e:
            print("Oggetto non trovato, errore: " + str(e))
            print("\n")
            #print("".join(Pyro4.util.getPyroTraceback()))
            #print("\n")
            self.ssh_connection_close_and_cleanup(identifier, address, password)

    def open_server_connection(self, identifier, address, password):

        print("\n")
        print("ID Oggetto: " + str(identifier))

        # Istanzio l'oggetto ssh
        ssh_connection = paramiko.SSHClient()
        # Confermo in automatico la connessione ssh, senza input da utente
        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Divido la stringa address(utente@hostname) in utente e hostname
        try:
            if str(address).__contains__('@'):
                (username, hostname) = str(address).split('@')
                print("User: " + username + ", Host: " + hostname)
                print("Tento la connessione...")
                ssh_connection.connect(hostname, username=username, password=password, timeout=5, allow_agent=False)

            else:
                print("Indirizzo: " + str(address))
                ssh_connection.connect(str(address), password=str(password), timeout=5, allow_agent=False)

            try:
                ns_ip = self.get_ip_address()

            except:
                ns_ip = "127.0.0.1"

            sftp_connection = ssh_connection.open_sftp()
            #(stdin, stdout, stderr) = ssh_connection.exec_command("echo $PATH")
            #print(stdout.readline())
            print("Connessione sftp aperta.")
            print("Trasferisco il " + self.text_analyzer_name + str(identifier) + "...")
            sftp_connection.put("text_analyzer.py", "./text_analyzer.py")
            print("Trasferisco Pyro4...")
            sftp_connection.put("Pyro4.zip", "./Pyro4.zip")
            print("Scompatto l'archivio...")
            (stdin, stdout, stderr) = ssh_connection.exec_command("tar -xzvf Pyro4.zip")
            time.sleep(3)
            # Con "echo $$" ricavo il pid del processo
            # Con "exec python3 text_analyzer.py" eseguo l'analizzatore testuale, con i parametri -id e -ns_ip
            print("Esecuzione " + self.text_analyzer_name + str(identifier) + ":")
            (stdin, stdout, stderr) = ssh_connection.exec_command("echo $$; exec python3 text_analyzer.py -id {} -ns {}".format(identifier, ns_ip), timeout=3, get_pty=True)
            print(stderr.readline())
            # Salvo il PID dell'oggetto
            self.object_pid = int(stdout.readline())
            print("PID del " + self.text_analyzer_name + str(identifier) + ": " + str(self.object_pid))
            # Chiudo le connessioni
            ssh_connection.close()
            sftp_connection.close()

            if stderr.readline() == "":
                print(self.text_analyzer_name + str(identifier) + " connesso.")
            else:
                print(self.text_analyzer_name + str(identifier) + " non connesso.")

        except (paramiko.AuthenticationException, socket.error) as e:
            ssh_connection.close()
            print("La connessione è fallita, errore: " + str(e))
            print(self.text_analyzer_name + str(identifier) + " non connesso.")

    # Metodo che provvede alla chiusura della connessione ssh. Questo metodo provvede inoltre all'eliminazione del
    # Text_Analyzer_N, dove N = (1, 2, 3, ...), killandone anche il processo.
    def ssh_connection_close_and_cleanup(self, identifier, address, password):

        ssh_connection = paramiko.SSHClient()
        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if str(address).__contains__('@'):
                (username, hostname) = str(address).split('@')
                ssh_connection.connect(str(hostname), username=username, password=str(password), timeout=5, allow_agent=False)
            else:
                ssh_connection.connect(str(address), password=str(password), timeout=5, allow_agent=False)

            print("Sto terminando il processo " + str(self.object_pid) + "...")
            ssh_connection.exec_command("/bin/kill -KILL {}".format(self.object_pid))
            print("Terminato.")
            ssh_connection.exec_command("rm -r Pyro4")
            ssh_connection.exec_command("rm -r Pyro4.zip")
            ssh_connection.exec_command("rm text_analyzer.py")
            time.sleep(5)
            print("\n")
            ssh_connection.close()

        except(paramiko.AuthenticationException, socket.error) as e:
            ssh_connection.close()
            print("Connessione fallita")
            print("Ritentare l'autenticazione; errore: " + str(e))
            print("\n")



