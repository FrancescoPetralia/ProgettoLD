__author__ = 'francesco'

'''
Modulo che gestisce tutti i metodi per dividere il file da analizzare in base al numero di hosts.
'''


class FileSplitter():
    '''
    La classe FileSplitter gestisce i metodi di divisione del file in base al numero di hosts.
    In particolare, vengono creati 'n' file a partire dal file originario.
    '''

    def __init__(self, hosts_number, file_to_split):
        '''

        :param hosts_number: numero di hosts.
        :param file_to_split: percorso del file da dividere.
        '''

        self.hosts_number = int(hosts_number)
        self.file_to_split = file_to_split
        self.file_content = None
        self.total_file_lines = 0
        self.lines_per_host = []
        self.splitted_text_assigned_to_hosts = [[] for x in range(self.hosts_number)]
        self.splitted_file_name = "splitted_file_"
        self.lower_index = None
        self.upper_index = None

    def split_file_between_hosts(self):
        '''
        Metodo che gestisce la divisione del file in 'n' files più piccoli.
        In base al numero di hosts, vengono creati dei file temporanei denominati nel seguente modo:
        supponendo di avere 3 host, avrò i seguenti file temporanei, es.:
        splitted_file_0, splitted_file_1, splitted_file_2.
        :return: True in caso di successo, False in caso di fallimento.
        '''

        # Calcolo quante righe ha il file originario
        for elements in range(0, len(self.read_file(self.file_to_split))):
            self.total_file_lines = (self.total_file_lines + 1)

        print("\nRighe totali da analizzare: " + str(self.total_file_lines))
        print("\nSplit del file in corso...")

        # Calcolo del quoziente e del resto per distribuire il carico di lavoro in modo che sia bilanciato.
        q, r = (divmod(self.total_file_lines, int(self.hosts_number)))

        print("\n")
        # Al primo host distribuisco le righe in avanzo (resto della divisione)
        for count in range(0, self.hosts_number):
            if count == 0:
                self.lines_per_host.append((q + r))
                print("Righe assegnate all'host_" + str(count) + ": " + str(self.lines_per_host[count]))
            else:
                self.lines_per_host.append(q)
                print("Righe assegnate all'host_" + str(count) + ": " + str(self.lines_per_host[count]))

        print("\n")

        # Split del file
        n = -1
        for count in range(0, self.hosts_number):
            self.lower_index = (n + 1)
            self.upper_index = self.lower_index + (self.lines_per_host[count])
            print("[" + str(self.lower_index) + ", " + str(self.upper_index) + "]")
            for elements in range(self.lower_index, self.upper_index):
                self.splitted_text_assigned_to_hosts[count].append(self.file_content[elements])
                n = elements
        tot = n
        tot += 1

        for count in range(0, self.hosts_number):
            f = open("../temp/" + self.splitted_file_name + str(count) + ".txt", 'w')
            for elements in self.splitted_text_assigned_to_hosts[count]:
                f.write(elements + "\n")
            f.close()

        # Controllo che lo split del file sia avvenuto correttamente
        if tot == self.total_file_lines:
            print("\nSplit del file avvenuto correttamente.")
            return True
        else:
            print("\nErrore nello split del file.")
            return False

    def read_file(self, file):
        '''
        Metodo che legge il contenuto del file.
        :param file: file da dividere.
        :return: contenuto del file.
        '''
        f = open(file, "r")
        self.file_content = f.read().splitlines()
        #print("\nTesto del file:\n" + str(self.file_content))
        f.close()
        return self.file_content