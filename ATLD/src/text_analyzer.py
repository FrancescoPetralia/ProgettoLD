# -*- coding: iso-8859-15 -*-

__author__ = 'Francesco'

import nltk, argparse, Pyro4, socket
#import execution_time_measurement


class TextAnalyzer:

    path_of_file_to_read = ''
    path_of_file_to_write = ''
    my_file = ''
    all_tokenized_word = ''
    all_tokenized_sentences = ''
    results = ''
    e = ''
    flag = ''

    def __init__(self):
        self.p1 = "prova.txt"
        self.p2 = "text_analisys_results.txt"
        #self.e = ExecutionTimeMeasurement()
        self.path_of_file_to_read = self.p1
        self.my_file = self.read_file(self.path_of_file_to_read)
        self.all_tokenized_word = self.words_inside_file()
        self.all_tokenized_sentences = self.sentences_inside_file()

    def read_file(self, p1):
        #lettura del file
        in_file = open(p1, "r")
        self.my_file = in_file.read()
        #self.my_file = self.my_file.decode("cp1252")
        #self.my_file.encode("utf-8", "ignore")
        in_file.close()
        return self.my_file

    def get_number_of_chars_in_file(self):
        return len(self.my_file)

    def get_occurrence_number_of_searched_char(self): #interattivo
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

    def get_occurences_number_of_searched_word(self, w): #interattivo
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
    def get_ip_addr(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ns_ip = str(s.getsockname()[0])
        s.close()
        print(ns_ip)
        return ns_ip


def main():

    global nsip, PYRO_OBJ_NAME
    text_analyzer_name = "Text_Analyzer_"

    # Configurazione del parser per gli argomenti in input
    parser = argparse.ArgumentParser(description="Valori di avvio: ")
    parser.add_argument("-id", help="Imposta l'id dell'analizzatore testuale.")
    parser.add_argument("-nsip", help="Imposta l'indirizzo ip del Name Server.")
    args = parser.parse_args()

    # Controllo che gli argomenti siano settati correttamente
    if args.id is None:
        identifier = ''
    else:
        identifier = str(args.id)

    if args.nsip is None:
        name_server_ip = ''
    else:
        name_server_ip = str(args.nsip)

    a = TextAnalyzer()

    try:
        if name_server_ip != '':
            nsip = Pyro4.naming.locateNS(name_server_ip)
        else:
            nsip = Pyro4.naming.locateNS()

        PYRO_OBJ_NAME = text_analyzer_name + str(identifier)
        print(PYRO_OBJ_NAME)
        daemon = Pyro4.Daemon(a.get_ip_addr())

        try:
            # Siccome Pyro associa un Pyro Object al Text_Analizer_N (dove N = (0, 1, 2, 3, ...)), una volta reperito
            # l'uri del Pyro Object, posso rimuoverlo, perché non mi serve più.
            print("prima del remove")
            uri_text_analyzer = nsip.lookup(PYRO_OBJ_NAME)
            print("dopo il lookup")
            nsip.remove(PYRO_OBJ_NAME)
            print("dopo il remove")
        except Pyro4.naming.NamingError as e:
            print("Errore durante il remove dell'oggetto: " + str(e))

        # Associazione e registrazione sul server dell'uri del Pyro Object (eliminato) al TextAnalyzer
        uri_text_analyzer = daemon.register(a)
        nsip.register(PYRO_OBJ_NAME, uri_text_analyzer)

        print("URI " + PYRO_OBJ_NAME + ": " + str(uri_text_analyzer))

        daemon.requestLoop()

        if a.get_results('n'):
            print("Analisi eseguita con successo.")
        else:
            print("Errore, analisi non eseguita.")

    except Pyro4.naming.NamingError as e:
        print("Errore nella configurazione del'oggetto PyRO: " + str(e))

if __name__ == "__main__":

    main()