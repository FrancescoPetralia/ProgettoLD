__author__ = 'francesco'

import datetime
from collections import Counter

'''
Modulo ResulstsCollector. Gestisce la raccolta dei risultati parziali di ogni host in un unico risultato finale.
'''


class ResultsCollector():
    '''
    Gestisce la raccolta dei risultati parziali di ogni host in un unico risultato finale.
    In particolare, ogni host restituisce un dizionario contenente i propri risultati parziali; una volta raccolti
    tutti i sotto-dizionari, viene creata una lista che è la somma dei risultati parziali di ciasscun host e
    che definisce il risultato finale dell'analisi.
    '''

    def __init__(self, object, hosts_number):

        self.text_analyzer = object
        self.hosts_number = int(hosts_number)
        self.results = []
        self.ret_values = []
        self.final_result = []
        self.deserialized_dict = []
        self.chars_occs = dict()
        self.words_occs = dict()
        self.all_chars_occurrences = None
        self.all_words_occurrences = None

    def collect_all_results(self):
        '''
        Questo metodo raccoglie i risultati parziali di ciascun host remoto e li somma, inserendoli all'interno di una
        lista di tuple del tipo: [(risultato1, somma_totale), (risultato2, somma_totale), ..., ...]
        '''

        ncnt = 0
        for count in range(0, self.hosts_number):

            results, ret_val = self.text_analyzer[count].get_results()
            self.results.append(results)
            self.ret_values.append(ret_val)

            if self.ret_values[count]:
                ncnt = (ncnt + 1)

        # Sommo i risultati parziali di tutti i text_analyzer per formare il rilsultato finale.
        # In particolare, ogni text_analyzer ritorna un oggetto dizionario ed un booleano. Il secondo parametro
        # lo utilizzo per verificare se le singole sotto-analisi sono state eseguite con successo, mentre il primo
        # parametro è il dizionario di ogni text_analyzer. Accedo ad un valore interno al dizionario con la relativa
        # key.
        chars, lines, consonants, vowels, acc_chars, numbers, spaces, punct, words, sentences = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        shortest_words, longest_words = [], []
        shortest_sentences, longest_sentences = [], []
        shortest_word, shortest_word_len, longest_word, longest_word_len = "", 0, "", 0
        shortest_sentence, shortest_sentence_len, longest_sentence, longest_sentence_len = "", 0, "", 0
        chars_occurrences, words_occurrences = [], []

        for count in range(0, self.hosts_number):
            chars += self.results[count]['n_chars']
            lines += self.results[count]['n_lines']
            consonants += self.results[count]['n_consonants']
            vowels += self.results[count]['n_vowels']
            acc_chars += self.results[count]['n_accented_chars']
            numbers += self.results[count]['n_numbers']
            spaces += self.results[count]['n_spaces']
            punct += self.results[count]['n_punctuation']
            words += self.results[count]['n_words']
            sentences += self.results[count]['n_sentences']
            shortest_words.append(self.results[count]['shortest_word'])
            longest_words.append(self.results[count]['longest_word'])
            shortest_sentences.append(self.results[count]['shortest_sentence'])
            longest_sentences.append(self.results[count]['longest_sentence'])
            chars_occurrences.append(self.results[count]['all_characters_occurrences'])
            words_occurrences.append(self.results[count]['all_words_occurrences'])

        shortest_word = min(shortest_words, key=len)
        shortest_word_len = len(shortest_word)
        longest_word = max(longest_words, key=len)
        longest_word_len = len(longest_word)
        shortest_sentence = min(shortest_sentences, key=len)
        shortest_sentence_len = len(shortest_sentence)
        longest_sentence = max(longest_sentences, key=len)
        longest_sentence_len = len(longest_sentence)

        self.all_chars_occurrences = self.all_characters_occurrences_gather(chars_occurrences)
        self.all_words_occurrences = self.all_words_occurrences_gather(words_occurrences)

        twenty_most_common_chars = self.get_twenty_most_common_chars()
        twenty_most_common_words = self.get_twenty_most_common_words()

        if shortest_word_len == 1:
            w_carattere = " carattere."
        else:
            w_carattere = " caratteri."

        if longest_word_len == 1:
            s_carattere = " carattere."
        else:
            s_carattere = " caratteri."

        self.final_result = ["Numero di caratteri: " + str(chars) + ".",
                             "Numero di righe: " + str(lines) + ".",
                             "Numero di consonanti: " + str(consonants) + ".",
                             "Numero di vocali: " + str(vowels) + ".",
                             "Numero di caratteri accentati: " + str(acc_chars) + ".",
                             "Numero di cifre: " + str(numbers) + ".",
                             "Numero di spazi: " + str(spaces) + ".",
                             "Numero di segni di punteggiatura: " + str(punct) + ".",
                             "Numero di parole: " + str(words) + ".",
                             "Numero di frasi: " + str(sentences) + ".",
                             "La parola più corta è: '" + shortest_word + "', ed è lunga " + str(shortest_word_len)
                             + w_carattere,
                             "La parola più lunga è: '" + longest_word + "', ed è lunga " + str(longest_word_len)
                             + s_carattere,
                             "La frase più corta è: '" + shortest_sentence + "', ed è lunga " + str(shortest_sentence_len)
                             + " caratteri.",
                             "La frase più lunga è: '" + longest_sentence + "', ed è lunga " + str(longest_sentence_len)
                             + " caratteri."]

        self.final_result.append("\nElenco dei 20 caratteri più utilizzati (carattere, occorrenza):")
        count = 0
        for key, val in twenty_most_common_chars:

            count += 1
            self.final_result.append(" - " + str(("" + key + "", str(val) + " volte")))

        self.final_result.append("\nElenco delle 20 parole più utilizzate (parola, occorrenza):")
        count = 0
        for key, val in twenty_most_common_words:

            count += 1
            self.final_result.append(" - " + str(("" + key + "", str(val) + " volte")))

        if ncnt == int(self.hosts_number):
            print("Analisi testuale eseguita con successo.")

    def all_characters_occurrences_gather(self, chars_occurrences):
        '''
        Metodo che trasforma le occorrenze dei caratteri calcolate dagli hosts remoti, contenute in una lista
        di liste di tuple, in un unico dizionario, strutturato nel seguente modo:
        [(carattere_1, occorrenza), (carattere_2, occorrenza), ..., ...], dove carattere_n è la key, e occorrenza è il
        valore relativo alla key.
        :param chars_occurrences: lista di liste di tuple dei caratteri e delle relative occorrenze.
        :return: dizionario dei caratteri, ordinati in senso decrescente in base all'occorrenza.
        '''

        for l in chars_occurrences:
            for elements in l:
                try:
                    self.chars_occs[elements[0]] = (self.chars_occs[elements[0]] + elements[1])
                except KeyError as e:
                    self.chars_occs[elements[0]] = elements[1]

        return Counter(self.chars_occs).most_common()

    def get_twenty_most_common_chars(self):
        '''
        Metodo che ritorna i 20 caratteri più utilizzati.
        :return: dizionario dei 20 caratteri più utilizzati.
        '''

        return Counter(self.chars_occs).most_common(20)

    def all_words_occurrences_gather(self, words_occurrences):
        '''
        Metodo che trasforma le occorrenze dei caratteri calcolate dagli hosts remoti, contenute in una lista
        di liste di tuple, in un unico dizionario, strutturato nel seguente modo:
        [(parola_1, occorrenza), (parola_2, occorrenza), ..., ...], dove parola_n è la key, e occorrenza è il
        valore relativo alla key.
        La trasformazione viene effettuata per via delle grandi dimensioni che può arrivare ad assumere la lista di
        occorrenze delle parole, dell'ordine di milioni o decine di milioni.
        In questo modo, adottando il dizionario, che è di tipo hastable, cioè una tabella hash, si riduce il
        costo computazionale dovuto alla gestione di un insieme contenente una grandissima quantità di elementi.
        :param words_occurrences: lista di liste di tuple delle parole e relative occorrenze.
        :return: dizionario delle parole, ordinate in senso decrescente in base all'occorrenza.
        '''

        for l in words_occurrences:
            for elements in l:
                try:
                    self.words_occs[elements[0]] = (self.words_occs[elements[0]] + elements[1])
                except KeyError as e:
                    self.words_occs[elements[0]] = elements[1]

        return Counter(self.words_occs).most_common()

    def get_twenty_most_common_words(self):
        '''
        Metodo che ritorna le 20 parole più utilizzate.
        :return: dizionario delle 20 parole più utilizzate.
        '''

        return Counter(self.words_occs).most_common(20)

    def get_final_result(self):
        '''
        Metodo che ritorna la lista contenente il risulato finale.
        :return: lista contenente il risultato finale.
        '''

        return self.final_result

    def save(self):
        '''
        Metodo che salva la lista dei risultati su file.
        :return: True, se il risultato è stato salvato correttamente su file. False se il risultato non è stato salvato
        correttamente su file.
        '''

        now = datetime.datetime.now()

        d_m_y = "_" + str(now.day) + str(now.month) + str(now.year) + "_"
        h_m_s = str(now.hour) + str(now.minute) + str(now.second)

        final_res = []
        most_common = []

        for count in range(0, 13):
            final_res.append(self.final_result[count] + "\n")

        most_common.append("\nElenco delle occorrenze dei caratteri (carattere, occorrenza):")
        for key, val in self.all_chars_occurrences:
            most_common.append(str(("" + key + "", str(val) + " volte")))
        most_common.append("\nElenco delle occorrenze delle parole (parola, occorrenza):")
        for key, val in self.all_words_occurrences:
            most_common.append(str(("" + key + "", str(val) + " volte")))

        for elements in most_common:
            final_res.append(elements)

        try:
            f = open("../res/text_analysis_result" + d_m_y + h_m_s + ".txt", 'w')
            f.write("Analisi eseguita su " + str(self.hosts_number) + " host.\n\n")
            for count in range(0, len(final_res)):
                f.write(str(final_res[count]) + "\n")
            f.close()
            print("\nAnalisi salvata in: ../res/text_analysis_result" + d_m_y + h_m_s + ".txt")
            return True, "\nAnalisi salvata in: ../res/text_analysis_result" + d_m_y + h_m_s + ".txt"
        except Exception as e:
            print("\nErrore nel salvataggio: " + str(e))
            return False, "\nErrore nel salvataggio: " + str(e)