#coding=utf-8
__author__ = 'Francesco'

import time

'''
Modulo che gestisce la misurazione del tempo.
'''


class ExecutionTimeMeasurement:
    '''
    Classe ExecutionTimeMeasurement che gestisce la misurazione del tempo.
    Usata per ottenere la misurazione, in secondi, di una data parte di codice.
    '''

    start = 0
    finish = 0
    interval = 0

    def __init__(self):
        pass

    def start_measurement(self):
        '''
        Metodo che stabilisce l'inizio della misurazione.
        '''
        self.start = time.clock()

    def finish_measurement(self):
        '''
        Metodo che stabilisce la fine della misurazione.
        '''
        self.finish = time.clock()
        self.interval = (self.start - self.finish)

    def get_measurement_interval(self):
        '''
        Metodo che ritorna l'intervallo della misurazione.
        :return: intervallo della misurazione.
        '''
        return abs(self.interval)


