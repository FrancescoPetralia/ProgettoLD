__author__ = 'francesco'

import unittest
import os
import nltk
import Pyro4
from text_analyzer import TextAnalyzer

'''
Modulo TestOccurrences. Questo modulo mette a disposizione metodi per lo unittesting dell'analizzatore.
'''


class TestOccurences(unittest.TestCase):
    '''
    Questa classe eredita da unittest.TestCase i metodi di default per lo unittesting in Python.
    '''

    def setUp(self):
        '''
        Metodo di setup per lo unittesting. Vengono create le istanze necessarie al test.
        Le azioni all'interno di questo metodo vengono eseguite prima dell'esecuzione del test.
        '''

        self.a1 = TextAnalyzer(0)
        self.a2 = TextAnalyzer(1)
        self.r1, self.r2 = self.a1.get_results(), self.a2.get_results()

    def test_final_results(self):
        '''
        Questo metodo verifica che i risultati prodotti da due analizzatore distinti sianoi medesimi.
        Nello specifico, solleva una assertEqual nel caso in cui i risultati coincidano. Dunque il test è passato.
        Nel caso in cui il test non sia stato passato, viene sollevato un messaggio con relativo errore.
        '''

        self.assertEqual(self.r1, self.r2, "chars_occurrence_test: test non apssato.")

    def tearDown(self):
        '''
        In questo metodo sono contenute tutte le azioni da compiere dopo che il test è avvenuto, e i risultati sono
        stati prodotti.
        In particolare, vengono cancellati i file di prova creati per il test.
        '''

        try:
            os.remove("splitted_file_0.txt")
            os.remove("splitted_file_1.txt")
        except Exception as e:
            pass


def main():
    unittest.main()

if __name__ == '__main__':
    main()
