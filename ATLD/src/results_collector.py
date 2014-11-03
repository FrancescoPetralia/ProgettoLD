__author__ = 'francesco'


class ResultsCollector():

    def __init__(self, object, hosts_number):
        self.text_analyzer = object
        self.hosts_number = int(hosts_number)
        self.results = []
        self.ret_values = []
        self.final_result = []

    def collect_all_results(self):

        cnt = 0
        for count in range(0, self.hosts_number):
            # Aggiungere try except!
            results, ret_val = self.text_analyzer[count].get_static_results()
            self.results.append(results)
            self.ret_values.append(ret_val)

            if self.ret_values[count]:
                cnt = (cnt + 1)

        # Sommo i risultati parziali di tutti i text_analyzer per formare il rilsultato finale.
        # In particolare, ogni text_analyzer ritorna un oggetto dizionario ed un booleano. Il secondo parametro
        # lo utilizzo per verificare se le singole sotto-analisi sono state eseguite con successo, mentre il primo
        # parametro è il dizionario di ogni text_analyzer. Accedo ad un valore interno al dizionario con la relativa
        # key.
        chars, lines, consonants, vowels, acc_chars, numbers, spaces, punct, words, sentences = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
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

        self.final_result = ["Numero di caratteri: " + str(chars) + ".",
                             "Numero di righe: " + str(lines) + ".",
                             "Numero di consonanti: " + str(consonants) + ".",
                             "Numero di vocali: " + str(vowels) + ".",
                             "Numero di caratteri accentati: " + str(acc_chars) + ".",
                             "Numero di cifre: " + str(numbers) + ".",
                             "Numero di spazi: " + str(spaces) + ".",
                             "Numero di segni di punteggiatura: " + str(punct) + ".",
                             "Numero di parole: " + str(words) + ".",
                             "Numero di frasi: " + str(sentences) + "."]

        #for elements in self.final_result:
        #    print(elements + "\n")

        if cnt == int(self.hosts_number):
            print("Analisi testuale eseguita con successo.\n")

    def get_final_result(self):
        return self.final_result