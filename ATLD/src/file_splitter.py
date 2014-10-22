__author__ = 'francesco'
from numpy import arange


class FileSplitter():

    def __init__(self, hosts_number, file_to_split):

        self.hosts_number = hosts_number
        self.file_to_split = file_to_split
        self.file_text = None
        self.total_file_lines = None
        self.lines_per_host = []

    def split_file_between_hosts(self):

        # Ricavo il numero di righe del file
        self.total_file_lines = (self.read_file(self.file_to_split).count("\n") + 1)

        division = (divmod(self.total_file_lines, int(self.hosts_number)))

        print("\n")
        for count in range(0, int(self.hosts_number)):
            if count == 0:
                self.lines_per_host.append(division[0] + division[1])
                print("Righe host" + str(count) + ": " + str(self.lines_per_host[count]))
            else:
                self.lines_per_host.append(division[0])
                print("Righe host" + str(count) + ": " + str(self.lines_per_host[count]))

        print("\n")

        return True

    def read_file(self, file):
        f = open(file, "r")
        self.file_text = f.read()
        #print("\nTesto del file:\n" + self.file_text)
        f.close()
        return self.file_text