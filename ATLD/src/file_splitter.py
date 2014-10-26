__author__ = 'francesco'
from numpy import arange


class FileSplitter():

    def __init__(self, hosts_number, file_to_split):

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

        # Calcolo quante righe ha il file originario
        for elements in range(0, len(self.read_file(self.file_to_split))):
            self.total_file_lines = (self.total_file_lines + 1)

        print("\nRighe totali: " + str(self.total_file_lines))

        # Calcolo del quoziente e del resto per distribuire il carico di lavoro in modo che sia bilanciato.
        q, r = (divmod(self.total_file_lines, int(self.hosts_number)))

        print("\n")
        # Al primo host distribuisco le righe in avanzo (resto della divisione)
        for count in range(0, self.hosts_number):
            if count == 0:
                self.lines_per_host.append((q + r))
                print("Righe host_" + str(count) + ": " + str(self.lines_per_host[count]))
            else:
                self.lines_per_host.append(q)
                print("Righe host_" + str(count) + ": " + str(self.lines_per_host[count]))

        print("\n")

        # Split del file
        n = -1
        for count in range(0, self.hosts_number):
            print("\n")
            self.lower_index = (n + 1)
            self.upper_index = self.lower_index + (self.lines_per_host[count])
            for elements in range(self.lower_index, self.upper_index):
                self.splitted_text_assigned_to_hosts[count].append(self.file_content[elements])
                print("elements: " + str(elements))
                self.write_file(self.splitted_file_name + str(count), self.splitted_text_assigned_to_hosts[count])
                n = elements
        tot = n
        tot = (tot + 1)
        #print("\nRighe totali: " + tot)

        # Controllo che lo split del file sia avvenuto correttamente
        if tot == self.total_file_lines:
            print("\nSplit del file avvenuto correttamente.")
            return True
        else:
            print("\nErrore nello split del file.")
            return False

    def read_file(self, file):
        f = open(file, "r")
        self.file_content = f.read().splitlines()
        #print("\nTesto del file:\n" + str(self.file_content))
        f.close()
        return self.file_content

    def write_file(self, file_name, interval):
        f = open("../txt/" + file_name + ".txt", 'w')
        for elements in interval:
            f.write(elements + "\n")
        f.close()