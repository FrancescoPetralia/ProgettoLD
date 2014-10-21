# -*- coding: iso-8859-15 -*-

__author__ = 'Francesco'

#import os
#os.environ["PYRO_LOGFILE"] = "pyro.log"
#os.environ["PYRO_LOGLEVEL"] = "DEBUG"
import nltk
import argparse
import Pyro4
import socket
#import execution_time_measurement


class TextAnalyzer():

    path_of_file_to_read = ''
    path_of_file_to_write = ''
    my_file = ''
    all_tokenized_word = ''
    all_tokenized_sentences = ''
    results = ''
    e = ''
    flag = ''

    def __init__(self, pyro_obj_name):
        #self.p1 = "prova.txt"
        self.p2 = "text_analisys_results.txt"
        #self.e = ExecutionTimeMeasurement()
        #self.path_of_file_to_read = self.p1
        #self.my_file = self.read_file(self.path_of_file_to_read)
        self.all_tokenized_word = self.words_inside_file()
        self.all_tokenized_sentences = self.sentences_inside_file()
        self.my_uri = None
        self. pyro_obj_name = pyro_obj_name

        self.info_exec()

    def info_exec(self):
        file = open(self.pyro_obj_name + ".txt", 'w')
        file.write("Ciao sono il " + self.pyro_obj_name + "\n")

    def read_file(self, p1):
        file = open(p1, "r")
        self.my_file = file.read()
        file.close()
        return self.my_file

    def get_number_of_chars_in_file(self):
        return len(self.my_file)

    #interattivo
    def get_occurrence_number_of_searched_char(self):
         pass

    def words_inside_file(self):
        words = nltk.word_tokenize(self.my_file)
        return words

    def get_all_tokenized_words(self):
        return self.all_tokenized_word

    def get_number_of_words_inside_the_file(self):
        return len(self.all_tokenized_word)

    def get_longest_word_in_the_file(self):
        return max(self.all_tokenized_word, key=len)

    def get_dim_of_longest_word_in_the_file(self):
        return len(self.get_longest_word_in_the_file())

    def get_shortest_word_in_the_file(self):
        return min(self.all_tokenized_word, key=len)

    def get_dim_of_shortest_word_in_the_file(self):
        return len(self.get_shortest_word_in_the_file())

    #interattivo
    def get_occurences_number_of_searched_word(self, w):
        cnt = 0
        for word in self.all_tokenized_word:
            if w in word:
                cnt += 1

        return cnt

    def all_words_occurrences_chart(self):
        l = nltk.FreqDist(self.all_tokenized_word)
        return l.items()[:len(self.all_tokenized_word)]

    def sentences_inside_file(self):
        sentences = nltk.sent_tokenize(self.my_file)
        return sentences

    def get_all_tokenized_sentences(self):
        return self.all_tokenized_sentences

    def get_number_of_sentences_inside_the_file(self):
        return len(self.all_tokenized_sentences)

    def get_longest_sentence_in_the_file(self):
        return max(self.all_tokenized_sentences, key=len)

    def get_dim_of_longest_sentence_in_the_file(self):
        return len(self.get_longest_sentence_in_the_file())

    def get_shortest_sentence_in_the_file(self):
        return min(self.all_tokenized_sentences, key=len)

    def get_dim_of_shortest_sentence_in_the_file(self):
        return len(self.get_shortest_sentence_in_the_file())

    def get_number_of_lines(self):
        return self.my_file.count('\n')

    def search_word_in_sentences(self, word): #interattivo
        cnt = 0
        for sentence in self.all_tokenized_sentences:
            if word in sentence:
                cnt += 1

        return sentence, cnt

    def get_number_of_consonants(self):
        consonants = "bcdfghjklmnpqrstvexz"
        tot = 0
        for c in self.my_file:
            if c in consonants:
                tot += 1

        return tot

    def get_number_of_vowels(self):
        vowels = "aeiou"
        tot = 0
        for c in self.my_file:
            if c in vowels:
                tot += 1

        return tot
    
    def get_results(self, flag):

        self.flag = flag

        #self.e.start_measurement()
        self.results = \
        [#str(self.get_all_tokenized_words()),
        #str(self.get_all_tokenized_sentences()),
        "Numero totale di caratteri: " +  str(self.get_number_of_chars_in_file()) + ".",
        "Numero totale di parole nel file: " + str(self.get_number_of_words_inside_the_file()) + ".",
        "Numero totale di frasi nel file: " + str(self.get_number_of_sentences_inside_the_file()) + ".",
        "La frase piu' lunga e': '" + self.get_longest_sentence_in_the_file() + "',\n' ed e' lunga " + str(self.get_dim_of_longest_sentence_in_the_file()) + " caratteri.",
        "La frase piu' corta e': '" + self.get_shortest_sentence_in_the_file() + "', ed e' lunga " + str(self.get_dim_of_shortest_sentence_in_the_file()) + " caratteri.",
        "La parola piu' lunga e': '" + self.get_longest_word_in_the_file() + "', ed e' lunga " + str(self.get_dim_of_longest_word_in_the_file()) + " caratteri.",
        "La parola piu' corta e': '" + self.get_shortest_word_in_the_file() + "', ed e' lunga " + str(self.get_dim_of_shortest_word_in_the_file()) + " caratteri.",
        "Numero di righe nel file: " + str(self.get_number_of_lines()) + ".",
        "Numero di consonanti presenti nel file: " + str(self.get_number_of_consonants()) + ".",
        "Numero di vocali presenti nel file: " + str(self.get_number_of_vowels()) + "."]
        #self.e.finish_measurement()
        #print("Tempo di esecuzione dell'analisi: " + str(self.e.get_measurement_interval()) + " secondi.")

        if self.flag == 'w':
            for elements in self.results:
                f = self.p2
                f.write(elements)
                f.write("\n")

            return True

        elif self.flag == 'n':
            for elements in self.results:
                print(elements)

            return True

    # Questo metodo ritorna l'indirizzo ip del Name Server
    def get_ip_address(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = str(s.getsockname()[0])
        s.close()
        print(ip)
        return ip


def main():

    global __NS__, __PYRO_OBJ_NAME__
    text_analyzer_name = "Text_Analyzer_"

    # Configurazione del parser per gli argomenti in input
    parser = argparse.ArgumentParser(description="Valori di avvio: ")
    parser.add_argument("-id", help="Imposta l'id dell'analizzatore testuale.")
    parser.add_argument("-ns", help="Imposta l'indirizzo ip del Name Server.")
    args = parser.parse_args()

    # Controllo che gli argomenti siano settati correttamente
    if args.id is not None:
        identifier = str(args.id)
        #print("identifier: " + identifier)
    else:
        identifier = ""
        #print("identifier: " + identifier)

    if args.ns is not None:
        name_server_ip = str(args.ns)
        #print("name_server_ip: " + name_server_ip)
    else:
        name_server_ip = ""
        #print("name_server_ip: " + name_server_ip)

    try:

        if name_server_ip != "":
            __NS__ = Pyro4.naming.locateNS(name_server_ip)
            #print("nsip - locateNS(name_server_ip): " + str(ns))
        else:
            __NS__ = Pyro4.naming.locateNS()
            #print("nsip: locateNS() " + str(ns))

        __PYRO_OBJ_NAME__ = text_analyzer_name + str(identifier)
        print("Nome PyRO Object: " + __PYRO_OBJ_NAME__)

        analyzer = TextAnalyzer(__PYRO_OBJ_NAME__)

        try:
            daemon = Pyro4.Daemon(analyzer.get_ip_address())
            #print("Daemon: " + str(daemon))

        except:
            daemon = Pyro4.Daemon("127.0.0.1")
            #print("Daemon: " + str(daemon))

        # Associazione e registrazione sul server dell'uri del Pyro Object (eliminato) al TextAnalyzer
        uri_text_analyzer = daemon.register(analyzer)
        __NS__.register(__PYRO_OBJ_NAME__, uri_text_analyzer, safe=True)
        print("URI " + __PYRO_OBJ_NAME__ + ": " + str(uri_text_analyzer))

        #d = Pyro4.core.DaemonObject(daemon)
        #obj_list = d.registered()
        #print(str(obj_list))

        daemon.requestLoop()

    except Pyro4.naming.NamingError as e:

        print("Errore nella configurazione del'oggetto PyRO: " + str(e))

if __name__ == "__main__":

    main()