#!pythona
# -*- coding: utf-8 -*-

'''
Część główna skryptu, wywołania funkcji analizujących.

Aby wszystko działało trzeba mieć:
- bazę Ewopis (ścieżkę deo bazy ustawiamy w pyEwopisLib w linii 26)
- pliki z Ewmapy
    * rozliczenie działek
    * pola

'''

# ncstroje@cyf-kr.edu.pl

import decimal
import math
import sys

import pyEwopisLib
import pyEwmapaLib
import pyEwLib

decimal.getcontext().prec = 10 # ustawienie precyzji na 4 miejsca po przecinku

# kodowanie = 'iso-8859-2'
# kodowanie = 'cp1250'
kodowanie = 'utf-8'

obreby = pyEwopisLib.obreby()

out = '2601015'

dzialki_ewmapa = pyEwmapaLib.czytaj_pola('Pola_' + out + '.txt') # wszystkie działki z bazy wektorowej
przec = pyEwmapaLib.czytaj_prz_baz('PrzBaz_' + out + '.txt')

if __name__ == '__main__':
    # pass
    # pyEwopisLib.ewopisWIN2_do_porownywarki(dzialki_uzytki)
    # pyEwopisLib.porownaj_dzialki(dzialki_uzytki)
    pyEwLib.analizuj_nr_dzialek(obreby, dzialki_ewmapa, '***')
    # pyEwLib.analizuj_pow_uzytkow(obreby, dzialki_ewmapa, przec, out, '***')
    # pyEwLib.analizuj_uzytki(obreby, dzialki_ewmapa)
    # pyEwLib.tworz_badanie_KW('5', kodowanie)
