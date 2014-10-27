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
        self.text_analyzer = []
        self.object_pid = []

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

        try:
            ns = Pyro4.naming.locateNS()
            #print("Return del locateNS(): " + str(ns))
            print("\n")
            print("Cerco sul server l'oggetto " + self.text_analyzer_name + str(identifier) + "...")
            #print(ns.list())
            uri_text_analyzer = ns.lookup(self.text_analyzer_name + str(identifier))
            print(self.text_analyzer_name + str(identifier) + " trovato.\nIl suo uri è: " + str(uri_text_analyzer))
            self.text_analyzer.append(Pyro4.Proxy(uri_text_analyzer))
            print("\n")

        except Pyro4.errors.NamingError as e:
            print("Oggetto non trovato, errore: " + str(e))
            #print("".join(Pyro4.util.getPyroTraceback()))
            #print("\n")
            self.ssh_connection_close_and_cleanup(identifier, address, password)

    # Apertura della connessione ssh e sftp
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
            print("Trasferisco il file splitted_file_" + str(identifier) + ".txt")
            sftp_connection.put("../txt/splitted_file_" + str(identifier) + ".txt", "./splitted_file_" + str(identifier) + ".txt")
            print("Trasferisco il " + self.text_analyzer_name + str(identifier) + "...")
            sftp_connection.put("text_analyzer.py", "./text_analyzer.py")
            print("Trasferisco Pyro4...")
            sftp_connection.put("Pyro4.zip", "./Pyro4.zip")
            print("Scompatto l'archivio...")
            stdin, stdout, stderr = ssh_connection.exec_command("tar -xzvf Pyro4.zip")
            time.sleep(3)
            # Con "echo $$" ricavo il pid del processo
            # Con "exec python3 text_analyzer.py" eseguo l'analizzatore testuale, con i parametri -id e -ns_ip
            print("Esecuzione " + self.text_analyzer_name + str(identifier) + "...")
            print("\n")
            python_3_path = "/Library/Frameworks/Python.framework/Versions/3.4/bin/python3"
            command = "echo $$; " + python_3_path + " text_analyzer.py -id {} -ns {}"
            stdin, stdout, stderr = ssh_connection.exec_command(command.format(identifier, ns_ip), timeout=3, get_pty=True)
            #print(command.format(identifier, ns_ip))

            try:
                print(stderr.readline())
            except socket.error:
                pass

            # Salvo il PID dell'oggetto
            self.object_pid.append(int(stdout.readline()))
            print("\nPID del " + self.text_analyzer_name + str(identifier) + ": " + str(self.object_pid[identifier]))
            # Chiudo le connessioni
            ssh_connection.close()
            sftp_connection.close()

            print(self.text_analyzer_name + str(identifier) + " connesso.")

        except paramiko.AuthenticationException as e:
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

            print("\nSto terminando il processo " + str(self.object_pid[identifier]) + "...")
            ssh_connection.exec_command("/bin/kill -KILL {}".format(self.object_pid[identifier]))
            print("\nTerminato.")
            ssh_connection.exec_command("rm -r Pyro4")
            ssh_connection.exec_command("rm -r Pyro4.zip")
            ssh_connection.exec_command("rm text_analyzer.py")
            ssh_connection.exec_command("rm splitted_file_*")
            time.sleep(5)

            ssh_connection.close()

        except(paramiko.AuthenticationException, socket.error) as e:
            ssh_connection.close()
            print("Connessione fallita")
            print("Ritentare l'autenticazione; errore: " + str(e))



