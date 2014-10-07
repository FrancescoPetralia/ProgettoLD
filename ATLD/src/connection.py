__author__ = 'francesco'

import Pyro4
import paramiko
import socket
import time
from PyQt4 import QtCore, QtGui


class Connection(QtGui.QMainWindow):

    def __init__(self):

        super(Connection, self).__init__()

        self.text_analyzer_name = "Text_Analyzer_"
        self.identifier = None
        self.address = None
        self.password = None
        self.object_pid = None
        #self.port = None

    # Questo metodo ritorna l'indirizzo ip del server
    def get_ip_addr(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ns_ip = str(s.getsockname()[0])
        s.close()
        print(ns_ip)
        return ns_ip

    # Metodo che cerca l'oggetto sul server
    def find_obj(self, identifier, a, p):

        self.identifier = identifier
        self.address = a
        self.password = p

        self.open_server_connection()
        #pyro_obj_address = str(self.open_server_connection())

        time.sleep(5)

        if self.authentication_ok:

            try:
                ns = Pyro4.naming.locateNS()
                uri_text_analyzer = ns.lookup(self.text_analyzer_name + str(self.identifier))
                print(self.text_analyzer_name + " trovato. Il suo uri è: " + uri_text_analyzer)
                self.text_analyzer = Pyro4.Proxy(uri_text_analyzer)

                return True

            except Pyro4.errors.NamingError as e:
                print("Oggetto non trovato, errore: " + str(e))
                self.ssh_connection_close_and_cleanup()

                return False

    def open_server_connection(self):

        print("ID Oggetto: " + str(self.identifier))

        # Istanzio l'oggetto ssh

        ssh_connection = paramiko.SSHClient()

        ssh_connection.load_system_host_keys()

        # Confermo in automatico la connessione ssh, senza input da utente
        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        # Divido la stringa address(utente@hostname) in utente e hostname
        try:
            if str(self.address).__contains__('@'):
                (username, hostname) = self.address.split('@')
                print("User: " + username + ", Host: " + hostname)
                print("Tento la connessione.")
                ssh_connection.connect(str(hostname), username=username, password=str(self.password), timeout=5, allow_agent=False)
                #obj_address = hostname

            else:
                ssh_connection.connect(str(self.address), password=str(self.password), timeout=5, allow_agent=False)
                #obj_address = self.address

            self.authentication_ok = True

            ns_ip = self.get_ip_addr()
            sftp_connection = ssh_connection.open_sftp()
            print("Connessione sftp aperta.")
            print("Trasferisco il " + self.text_analyzer_name + str(self.identifier) + "...")
            sftp_connection.put("text_analyzer.py", "./text_analyzer.py")
            print("Trasferisco Pyro4...")
            sftp_connection.put("Pyro4.zip", "./Pyro4.zip")
            print("Scompatto l'archivio...")
            stdin, stdout, stderr = ssh_connection.exec_command("tar -xzvf Pyro4.zip")
            time.sleep(3)
            # Con "echo $$" ritorno il pid del processo che sto per fare eseguire
            # Con "exec python3 text_analyzer.py" eseguo l'analizzatore testuale, con i parametri -id e -ns_ip
            print("Esecuzione " + self.text_analyzer_name + str(self.identifier) + ":")
            stdin, stdout, stderr = ssh_connection.exec_command("echo $$; exec python3 text_analyzer.py -id {} -nsip {}".format(self.identifier, ns_ip))
            print("'exec python3 text_analyzer.py -id {} -nsip {}'".format(self.identifier, ns_ip))
            # Salvo il PID dell'oggetto
            self.object_pid = int(stdout.readline())
            print("PID del " + self.text_analyzer_name + str(self.identifier) + ": " + str(self.object_pid))
            # Chiudo le connessioni
            ssh_connection.close()
            sftp_connection.close()

            # Ritorno l'indirizzo dell'oggetto
            #print("Indirizzo dell'oggetto: " + str(obj_address))
            #return obj_address

        except (paramiko.AuthenticationException, socket.error) as e:
            self.authentication_ok = False
            ssh_connection.close()
            print("La connessione è fallita, errore: " + str(e))

    # Metodo che provvede alla chiusura della connessione ssh. Questo metodo provvede inoltre all'eliminazione del
    # Text_Analyzer_N, dove N = (1, 2, 3, ...), killandone anche il processo.
    def ssh_connection_close_and_cleanup(self):

        ssh_connection = paramiko.SSHClient()

        ssh_connection.load_system_host_keys()

        ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        try:
            if str(self.address).__contains__('@'):
                (username, hostname) = self.address.split('@')
                ssh_connection.connect(str(hostname), username=username, password=str(self.password), timeout=5, allow_agent=False)
            else:
                ssh_connection.connect(str(self.address), password=str(self.password), timeout=5, allow_agent=False)

            self.host = hostname
            print("Sto killando il PID: " + str(self.object_pid))
            ssh_connection.exec_command("/bin/kill -KILL {}".format(self.object_pid))
            ssh_connection.exec_command("rm -r Pyro4")
            ssh_connection.exec_command("rm -r Pyro4.zip")
            ssh_connection.exec_command("rm text_analyzer.py")
            time.sleep(5)

            ssh_connection.close()

        except(paramiko.AuthenticationException, socket.error) as e:
            ssh_connection.close()
            print("Connessione fallita")
            print("Ritentare l'autenticazione; errore: " + str(e))



