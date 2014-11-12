__author__ = 'francesco'

import pickle

class ResultsCollector():

    def __init__(self, object, hosts_number):
        self.text_analyzer = object
        self.hosts_number = int(hosts_number)
        self.results = []
        self.ret_values = []
        self.final_result = []
        self.deserialized_dict = []
        self.chars_occs = None
        self.words_occs = None

    def collect_all_results(self):

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

        all_chars_occurrences = self.all_characters_occurrences_gather(chars_occurrences)
        all_words_occurrences = self.all_words_occurrences_gather(words_occurrences)

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

        self.final_result.append("\nElenco dei 30 caratteri più utilizzati (carattere, occorrenza):")
        for key, val in all_chars_occurrences.items():
            self.final_result.append(str(("" + key + "", str(val) + " volte")))
        self.final_result.append("\nElenco delle 30 parole più utilizzate (parola, occorrenza):")
        for key, val in all_words_occurrences.items():
            self.final_result.append(str(("" + key + "", str(val) + " volte")))

        if ncnt == int(self.hosts_number):
            print("Analisi testuale eseguita con successo.")

    def all_characters_occurrences_gather(self, chars_occurrences):

        keys, values, self.chars_occs = [], [], dict()

        for count in range(0, self.hosts_number):
            for i in chars_occurrences[count]:
                keys.append(i[0])
                values.append(i[1])

        for count in range(0, len(keys)):
            i, s = -1, 0
            for elements in keys:
                i += 1
                if keys[count] == elements:
                    s += values[i]
                else:
                    pass

            self.chars_occs.update(({keys[count]: s}))

        return self.chars_occs

    def get_all_characters_occurrences(self):
        return self.chars_occs

    def all_words_occurrences_gather(self, words_occurrences):

        keys, values, self.words_occs = [], [], dict()

        for count in range(0, self.hosts_number):
            for i in words_occurrences[count]:
                keys.append(i[0])
                values.append(i[1])

        for count in range(0, len(keys)):
            i, s = -1, 0
            for elements in keys:
                i += 1
                if keys[count] == elements:
                    s += values[i]
                else:
                    pass

            self.words_occs.update(({keys[count]: s}))

        return self.words_occs

    def get_all_words_occurrences(self):
        return self.words_occs

    def get_final_result(self):
        return self.final_result