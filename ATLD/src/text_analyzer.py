# -*- coding: iso-8859-15 -*-

__author__ = 'Francesco'

import os
#os.environ["PYRO_LOGFILE"] = "pyro.log"
#os.environ["PYRO_LOGLEVEL"] = "DEBUG"
import nltk
import argparse
import Pyro4
import socket
import signal
import sys


class TextAnalyzer():

    def __init__(self, identifier):

        self.results = None
        self.all_tokenized_words = None
        self.all_tokenized_sentences = None
        self.my_uri = None
        self.file_to_read = "splitted_file_" + str(identifier) + ".txt"

        self.tokenize_words()
        self.tokenize_sentences()

    def read_file(self):
        f = open(self.file_to_read, "r")
        file_text = f.read()
        f.close()
        return file_text

    def tokenize_words(self):
        self.all_tokenized_words = self.words_inside_file()

    def tokenize_sentences(self):
        self.all_tokenized_sentences = self.sentences_inside_file()

    def get_number_of_chars_in_file(self):
        return len(self.read_file())

    #interattivo
    def get_occurrence_number_of_searched_char(self):
        pass

    def words_inside_file(self):
        words = nltk.word_tokenize(self.read_file())
        return words

    def get_all_tokenized_words(self):
        return self.all_tokenized_words

    def get_number_of_words_inside_the_file(self):
        return len(self.all_tokenized_words)

    def get_longest_word_in_the_file(self):
        return max(self.all_tokenized_words, key=len)

    def get_dim_of_longest_word_in_the_file(self):
        return len(self.get_longest_word_in_the_file())

    def get_shortest_word_in_the_file(self):
        return min(self.all_tokenized_words, key=len)

    def get_dim_of_shortest_word_in_the_file(self):
        return len(self.get_shortest_word_in_the_file())

    #interattivo
    def get_occurences_number_of_searched_word(self, w):
        cnt = 0
        for word in self.all_tokenized_words:
            if w in word:
                cnt += 1

        return cnt

    def all_words_occurrences_chart(self):
        l = nltk.FreqDist(self.all_tokenized_words)
        return l.items()[:len(self.all_tokenized_words)]

    def sentences_inside_file(self):
        sentences = nltk.sent_tokenize(self.read_file())
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
        return self.read_file().count('\n')

    #interattivo
    def search_word_in_sentences(self, word):
        cnt = 0
        for sentence in self.all_tokenized_sentences:
            if word in sentence:
                cnt += 1

        return sentence, cnt

    def get_number_of_consonants(self):
        consonants = "bcdfghjklmnpqrstvexz"
        tot = 0
        for c in self.read_file():
            if c in consonants:
                tot += 1

        return tot

    def get_number_of_vowels(self):
        vowels = "aeiou"
        tot = 0
        for c in self.read_file():
            if c in vowels:
                tot += 1

        return tot

    def get_interactive_results(self):
        pass
    
    def get_static_results(self):

        self.results = \
            [self.get_number_of_chars_in_file(),
             self.get_number_of_words_inside_the_file(),
             self.get_number_of_sentences_inside_the_file(),
             self.get_longest_sentence_in_the_file(),
             self.get_dim_of_longest_sentence_in_the_file(),
             self.get_shortest_sentence_in_the_file(),
             self.get_dim_of_shortest_sentence_in_the_file(),
             self.get_longest_word_in_the_file(),
             self.get_dim_of_longest_word_in_the_file(),
             self.get_shortest_word_in_the_file(),
             self.get_dim_of_shortest_word_in_the_file(),
             self.get_number_of_lines(),
             self.get_number_of_consonants(),
             self.get_number_of_vowels()
             ]

        return self.results, True

    # Questo metodo ritorna l'indirizzo ip assegnatomi dalla rete
    def get_ip_address(self):
        # SOCK_DGRAM imposta un trasporto UDP, mentre SOCK_STREAM un trasporto TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("www.google.com", 80))
        ip = str(s.getsockname()[0])
        #s.bind(ip, 0)
        s.close()

        return ip


def stop_connection_and_unregister_from_ns(signal, frame):
        print("Chiusura della connessione in corso...")
        __NS__.remove(__PYRO_OBJ_NAME__)
        sys.exit(0)


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
        print(identifier, __PYRO_OBJ_NAME__)
        
        analyzer = TextAnalyzer(identifier)

        try:
            daemon = Pyro4.Daemon(analyzer.get_ip_address())
            print(analyzer.get_ip_address())
            print("Daemon: " + str(daemon))

        except Exception as e:
            daemon = Pyro4.Daemon("127.0.0.1")
            print("Daemon: " + str(daemon))

        # Associazione e registrazione sul server dell'uri del Pyro Object (eliminato) al TextAnalyzer
        uri_text_analyzer = daemon.register(analyzer)
        __NS__.register(__PYRO_OBJ_NAME__, uri_text_analyzer)
        print("URI " + __PYRO_OBJ_NAME__ + ": " + str(uri_text_analyzer))

        #d = Pyro4.core.DaemonObject(daemon)
        #obj_list = d.registered()
        #print(str(obj_list))

        signal.signal(signal.SIGINT, stop_connection_and_unregister_from_ns)
        signal.signal(signal.SIGTERM, stop_connection_and_unregister_from_ns)

        daemon.requestLoop()

    except Pyro4.naming.NamingError as e:

        print("Errore nella configurazione del'oggetto PyRO: " + str(e))

if __name__ == "__main__":

    main()