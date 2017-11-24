#!pythona
# -*- coding: utf-8 -*-

'''
Funkcje obsługujące Ewmapę.
'''

import sys
import decimal
import math

# ~ import pyEwLib

# kodowanie = 'iso-8859-2'
# kodowanie = 'cp1250'
kodowanie = 'utf-8'

decimal.getcontext().prec = 10  # ustawienie precyzji na 4 miejsca po przecinku

G5KLU = {  # Aneks nr 3 do instrukcji G-5
    # Użytki rolne
    'RI': ['R', 'R', 'I'],
    'RII': ['R', 'R', 'II'],
    'RIIIa': ['R', 'R', 'IIIa'],
    'RIIIb': ['R', 'R', 'IIIb'],
    'RIVa': ['R', 'R', 'IVa'],
    'RIVb': ['R', 'R', 'IVb'],
    'RV': ['R', 'R', 'V'],
    'RVI': ['R', 'R', 'VI'],
    'S-RI': ['S', 'R', 'I'],
    'S-RII': ['S', 'R', 'II'],
    'S-RIIIa': ['S', 'R', 'IIIa'],
    'S-RIIIb': ['S', 'R', 'IIIb'],
    'S-RIVa': ['S', 'R', 'IVa'],
    'S-RIVb': ['S', 'R', 'IVb'],
    'S-RV': ['S', 'R', 'V'],
    'S-RVI': ['S', 'R', 'VI'],
    'S-PsI': ['S', 'Ps', 'I'],
    'S-PsII': ['S', 'Ps', 'II'],
    'S-PsIII': ['S', 'Ps', 'III'],
    'S-PsIV': ['S', 'Ps', 'IV'],
    'S-PsV': ['S', 'Ps', 'V'],
    'S-PsVI': ['S', 'Ps', 'VI'],
    'S-\xa3I': ['S', 'Ł', 'I'],
    'S-\xa3II': ['S', 'Ł', 'II'],
    'S-\xa3III': ['S', 'Ł', 'III'],
    'S-\xa3IV': ['S', 'Ł', 'IV'],
    'S-\xa3V': ['S', 'Ł', 'V'],
    'S-\xa3VI': ['S', 'Ł', 'VI'],
    '\xa3I': ['Ł', 'Ł', 'I'],
    '\xa3II': ['Ł', 'Ł', 'II'],
    '\xa3III': ['Ł', 'Ł', 'III'],
    '\xa3IV': ['Ł', 'Ł', 'IV'],
    '\xa3V': ['Ł', 'Ł', 'V'],
    '\xa3VI': ['Ł', 'Ł', 'VI'],
    'PsI': ['Ps', 'Ps', 'I'],
    'PsII': ['Ps', 'Ps', 'II'],
    'PsIII': ['Ps', 'Ps', 'III'],
    'PsIV': ['Ps', 'Ps', 'IV'],
    'PsV': ['Ps', 'Ps', 'V'],
    'PsVI': ['Ps', 'Ps', 'VI'],
    'B-RI': ['Br', 'R', 'I'],
    'B-RII': ['Br', 'R', 'II'],
    'B-RIIIa': ['Br', 'R', 'IIIa'],
    'B-RIIIb': ['Br', 'R', 'IIIb'],
    'B-RIVa': ['Br', 'R', 'IVa'],
    'B-RIVb': ['Br', 'R', 'IVb'],
    'B-RV': ['Br', 'R', 'V'],
    'B-RVI': ['Br', 'R', 'VI'],
    'B-PsI': ['Br', 'Ps', 'I'],
    'B-PsII': ['Br', 'Ps', 'II'],
    'B-PsIII': ['Br', 'Ps', 'III'],
    'B-PsIV': ['Br', 'Ps', 'IV'],
    'B-PsV': ['Br', 'Ps', 'V'],
    'B-PsVI': ['Br', 'Ps', 'VI'],
    'B-\xa3I': ['Br', 'Ł', 'I'],
    'B-\xa3II': ['Br', 'Ł', 'II'],
    'B-\xa3III': ['Br', 'Ł', 'III'],
    'B-\xa3IV': ['Br', 'Ł', 'IV'],
    'B-\xa3V': ['Br', 'Ł', 'V'],
    'B-\xa3VI': ['Br', 'Ł', 'VI'],
    'B-LsI': ['Br', 'Ls', 'I'],
    'B-LsII': ['Br', 'Ls', 'II'],
    'B-LsIII': ['Br', 'Ls', 'III'],
    'B-LsIV': ['Br', 'Ls', 'IV'],
    'B-LsV': ['Br', 'Ls', 'V'],
    'B-LsVI': ['Br', 'Ls', 'VI'],
    'Wsr': ['Wsr', '', ''],
    'Wsr-LsI': ['Wsr', 'Ls', 'I'],
    'Wsr-LsII': ['Wsr', 'Ls', 'II'],
    'Wsr-LsIII': ['Wsr', 'Ls', 'III'],
    'Wsr-LsIV': ['Wsr', 'Ls', 'IV'],
    'Wsr-LsV': ['Wsr', 'Ls', 'V'],
    'Wsr-LsVI': ['Wsr', 'Ls', 'VI'],
    'Wsr-RI': ['Wsr', 'R', 'I'],
    'Wsr-RII': ['Wsr', 'R', 'II'],
    'Wsr-RIIIa': ['Wsr', 'R', 'IIIa'],
    'Wsr-RIIIb': ['Wsr', 'R', 'IIIb'],
    'Wsr-RIVa': ['Wsr', 'R', 'IVa'],
    'Wsr-RIVb': ['Wsr', 'R', 'IVb'],
    'Wsr-RV': ['Wsr', 'R', 'V'],
    'Wsr-RVI': ['Wsr', 'R', 'VI'],
    'Wsr-PsI': ['Wsr', 'Ps', 'I'],
    'Wsr-PsII': ['Wsr', 'Ps', 'II'],
    'Wsr-PsIII': ['Wsr', 'Ps', 'III'],
    'Wsr-PsIV': ['Wsr', 'Ps', 'IV'],
    'Wsr-PsV': ['Wsr', 'Ps', 'V'],
    'Wsr-PsVI': ['Wsr', 'Ps', 'VI'],
    'Wsr-\xa3I': ['Wsr', 'Ł', 'I'],
    'Wsr-\xa3II': ['Wsr', 'Ł', 'II'],
    'Wsr-\xa3III': ['Wsr', 'Ł', 'III'],
    'Wsr-\xa3IV': ['Wsr', 'Ł', 'IV'],
    'Wsr-\xa3V': ['Wsr', 'Ł', 'V'],
    'Wsr-\xa3VI': ['Wsr', 'Ł', 'VI'],
    'W': ['W', '', ''],
    'W-LsI': ['W', 'Ls', 'I'],
    'W-LsII': ['W', 'Ls', 'II'],
    'W-LsIII': ['W', 'Ls', 'III'],
    'W-LsIV': ['W', 'Ls', 'IV'],
    'W-LsV': ['W', 'Ls', 'V'],
    'W-LsVI': ['W', 'Ls', 'VI'],
    'W-RI': ['W', 'R', 'I'],
    'W-RII': ['W', 'R', 'II'],
    'W-RIIIa': ['W', 'R', 'IIIa'],
    'W-RIIIb': ['W', 'R', 'IIIb'],
    'W-RIVa': ['W', 'R', 'IVa'],
    'W-RIVb': ['W', 'R', 'IVb'],
    'W-RV': ['W', 'R', 'V'],
    'W-RVI': ['W', 'R', 'VI'],
    'W-PsI': ['W', 'Ps', 'I'],
    'W-PsII': ['W', 'Ps', 'II'],
    'W-PsIII': ['W', 'Ps', 'III'],
    'W-PsIV': ['W', 'Ps', 'IV'],
    'W-PsV': ['W', 'Ps', 'V'],
    'W-PsVI': ['W', 'Ps', 'VI'],
    'W-\xa3I': ['W', 'Ł', 'I'],
    'W-\xa3II': ['W', 'Ł', 'II'],
    'W-\xa3III': ['W', 'Ł', 'III'],
    'W-\xa3IV': ['W', 'Ł', 'IV'],
    'W-\xa3V': ['W', 'Ł', 'V'],
    'W-\xa3VI': ['W', 'Ł', 'VI'],
    # Grunty leśne oraz zadrzewione i zakrzewione
    'Ls': ['Ls', '', ''],
    'LsI': ['Ls', 'Ls', 'I'],
    'LsII': ['Ls', 'Ls', 'II'],
    'LsIII': ['Ls', 'Ls', 'III'],
    'LsIV': ['Ls', 'Ls', 'IV'],
    'LsV': ['Ls', 'Ls', 'V'],
    'LsVI': ['Ls', 'Ls', 'VI'],
    'Lz': ['Lz', '', ''],
    'Lz-RI': ['Lz', 'R', 'I'],
    'Lz-RII': ['Lz', 'R', 'II'],
    'Lz-RIIIa': ['Lz', 'R', 'IIIa'],
    'Lz-RIIIb': ['Lz', 'R', 'IIIb'],
    'Lz-RIVa': ['Lz', 'R', 'IVa'],
    'Lz-RIVb': ['Lz', 'R', 'IVb'],
    'Lz-RV': ['Lz', 'R', 'V'],
    'Lz-RVI': ['Lz', 'R', 'VI'],
    'Lz-PsI': ['Lz', 'Ps', 'I'],
    'Lz-PsII': ['Lz', 'Ps', 'II'],
    'Lz-PsIII': ['Lz', 'Ps', 'III'],
    'Lz-PsIV': ['Lz', 'Ps', 'IV'],
    'Lz-PsV': ['Lz', 'Ps', 'V'],
    'Lz-PsVI': ['Lz', 'Ps', 'VI'],
    'Lz-\xa3I': ['Lz', 'Ł', 'I'],
    'Lz-\xa3II': ['Lz', 'Ł', 'II'],
    'Lz-\xa3III': ['Lz', 'Ł', 'III'],
    'Lz-\xa3IV': ['Lz', 'Ł', 'IV'],
    'Lz-\xa3V': ['Lz', 'Ł', 'V'],
    'Lz-\xa3VI': ['Lz', 'Ł', 'VI'],
    # Grunty zabudowane i zurbanizowane
    'B': ['B', '', ''],
    'Ba': ['Ba', '', ''],
    'Bi': ['Bi', '', ''],
    'Bp': ['Bp', '', ''],
    'Bz': ['Bz', '', ''],
    'K': ['K', '', ''],
    'dr': ['dr', '', ''],
    'Tk': ['Tk', '', ''],
    'Ti': ['Ti', '', ''],
    # Użytki ekologiczne
    'E-RI': ['E', 'R', 'I'],
    'E-RII': ['E', 'R', 'II'],
    'E-RIIIa': ['E', 'R', 'IIIa'],
    'E-RIIIb': ['E', 'R', 'IIIb'],
    'E-RIVa': ['E', 'R', 'IVa'],
    'E-RIVb': ['E', 'R', 'IVb'],
    'E-RV': ['E', 'R', 'V'],
    'E-RVI': ['E', 'R', 'VI'],
    'E-PsI': ['E', 'Ps', 'I'],
    'E-PsII': ['E', 'Ps', 'II'],
    'E-PsIII': ['E', 'Ps', 'III'],
    'E-PsIV': ['E', 'Ps', 'IV'],
    'E-PsV': ['E', 'Ps', 'V'],
    'E-PsVI': ['E', 'Ps', 'VI'],
    'E-\xa3I': ['E', 'Ł', 'I'],
    'E-\xa3II': ['E', 'Ł', 'II'],
    'E-\xa3III': ['E', 'Ł', 'III'],
    'E-\xa3IV': ['E', 'Ł', 'IV'],
    'E-\xa3V': ['E', 'Ł', 'V'],
    'E-\xa3VI': ['E', 'Ł', 'VI'],
    'E-Lz': ['E-Lz', '', ''],
    'E-Lz-RI': ['E-Lz', 'R', 'I'],
    'E-Lz-RII': ['E-Lz', 'R', 'II'],
    'E-Lz-RIIIa': ['E-Lz', 'R', 'IIIa'],
    'E-Lz-RIIIb': ['E-Lz', 'R', 'IIIb'],
    'E-Lz-RIVa': ['E-Lz', 'R', 'IVa'],
    'E-Lz-RIVb': ['E-Lz', 'R', 'IVb'],
    'E-Lz-RV': ['E-Lz', 'R', 'V'],
    'E-Lz-RVI': ['E-Lz', 'R', 'VI'],
    'E-Lz-PsI': ['E-Lz', 'Ps', 'I'],
    'E-Lz-PsII': ['E-Lz', 'Ps', 'II'],
    'E-Lz-PsIII': ['E-Lz', 'Ps', 'III'],
    'E-Lz-PsIV': ['E-Lz', 'Ps', 'IV'],
    'E-Lz-PsV': ['E-Lz', 'Ps', 'V'],
    'E-Lz-PsVI': ['E-Lz', 'Ps', 'VI'],
    'E-Lz-\xa3I': ['E-Lz', 'Ł', 'I'],
    'E-Lz-\xa3II': ['E-Lz', 'Ł', 'II'],
    'E-Lz-\xa3III': ['E-Lz', 'Ł', 'III'],
    'E-Lz-\xa3IV': ['E-Lz', 'Ł', 'IV'],
    'E-Lz-\xa3V': ['E-Lz', 'Ł', 'V'],
    'E-Lz-\xa3VI': ['E-Lz', 'Ł', 'VI'],
    'E-Ls': ['E-Ls', '', ''],
    'E-LsI': ['E-Ls', 'Ls', 'I'],
    'E-LsII': ['E-Ls', 'Ls', 'II'],
    'E-LsIII': ['E-Ls', 'Ls', 'III'],
    'E-LsIV': ['E-Ls', 'Ls', 'IV'],
    'E-LsV': ['E-Ls', 'Ls', 'V'],
    'E-LsVI': ['E-Ls', 'Ls', 'VI'],
    'E-Wp': ['E-Wp', '', ''],
    'E-Ws': ['E-Ws', '', ''],
    'E-W': ['E-W', '', ''],
    'E-W-RI': ['E-W', 'R', 'I'],
    'E-W-RII': ['E-W', 'R', 'II'],
    'E-W-RIIIa': ['E-W', 'R', 'IIIa'],
    'E-W-RIIIb': ['E-W', 'R', 'IIIb'],
    'E-W-RIVa': ['E-W', 'R', 'IVa'],
    'E-W-RIVb': ['E-W', 'R', 'IVb'],
    'E-W-RV': ['E-W', 'R', 'V'],
    'E-W-RVI': ['E-W', 'R', 'VI'],
    'E-W-PsI': ['E-W', 'Ps', 'I'],
    'E-W-PsII': ['E-W', 'Ps', 'II'],
    'E-W-PsIII': ['E-W', 'Ps', 'III'],
    'E-W-PsIV': ['E-W', 'Ps', 'IV'],
    'E-W-PsV': ['E-W', 'Ps', 'V'],
    'E-W-PsVI': ['E-W', 'Ps', 'VI'],
    'E-W-\xa3I': ['E-W', 'Ł', 'I'],
    'E-W-\xa3II': ['E-W', 'Ł', 'II'],
    'E-W-\xa3III': ['E-W', 'Ł', 'III'],
    'E-W-\xa3IV': ['E-W', 'Ł', 'IV'],
    'E-W-\xa3V': ['E-W', 'Ł', 'V'],
    'E-W-\xa3VI': ['E-W', 'Ł', 'VI'],
    'E-W-LsI': ['E-W', 'Ls', 'I'],
    'E-W-LsII': ['E-W', 'Ls', 'II'],
    'E-W-LsIII': ['E-W', 'Ls', 'III'],
    'E-W-LsIV': ['E-W', 'Ls', 'IV'],
    'E-W-LsV': ['E-W', 'Ls', 'V'],
    'E-W-LsVI': ['E-W', 'Ls', 'VI'],
    'E-N': ['E-N', '', ''],
    # Nieużytki
    'N': ['N', '', ''],
    # Grunty pod wodami
    'Wm': ['Wm', '', ''],
    'Wp': ['Wp', '', ''],
    'Ws': ['Ws', '', ''],

    # Tereny różne
    'Tr': ['Tr', '', '']}

print('Lz-\xa3I'.encode("utf-8").decode("utf-8"))

class dzialka_pola():
    def __init__(self, other):
        self.nr, self.pew, self.pewP = other.split('\n')[0].split()
        # print self.nr
        self.obr_ark, self.licz_mian = self.nr.split('-')

        if '.' in self.obr_ark:
            self.obreb, self.arkusz = self.obr_ark.split('.')
        else:
            self.obreb, self.arkusz = self.obr_ark, ''
        if r'/' in self.licz_mian:
            self.licznik, self.mianownik = self.licz_mian.split(r'/')
        else:
            self.licznik, self.mianownik = self.licz_mian, ''

        self.pew = decimal.Decimal(self.pew)
        self.pewP = decimal.Decimal(self.pewP)

    def nr_caly(self):
        return self.nr

    def nr_dzialki(self):
        return self.licz_mian

    def nr_obrebu(self):
        return self.obr_ark

    def __repr__(self):
        return repr((self.nr, self.obreb, self.arkusz, self.licznik, self.mianownik, self.pew, self.pewP))


def tworz_nr_dz_z_listy(lista):
    '''Funkcja tworzy listę poprawnych numerów działek

    zwraca listę'''
    nl = []
    if not lista[1]:
        return [lista[0]]
    elif '0' in lista[1]:
        nl.append(lista[0])
        lista[1].remove('0')
    for i in lista[1]:
        linia = '{0}/{1}'.format(lista[0], i)
        nl.append(linia)
    return nl


def anal_uzytek(uzytek):
    '''Funkcja analizuje użytek z bazy Firebird'''

    if [uzytek.ofu, uzytek.ozu, uzytek.ozk] in list(G5KLU.values()):
        for i in G5KLU:
            if G5KLU[i] == [uzytek.ofu, uzytek.ozu, uzytek.ozk]:
                return i
    else:
        return 0


def anal_klasouzytek(klk):
    '''Funkcja analizuje klasoużytek z pliku przecięcia baz ewmapy'''
    if r'/' in klk:
        klk = klk.replace(r'/', '-')
    if klk in G5KLU:
        return klk
    else:
        return klk


def sortuj_nr_dzialek(lista):
    '''Funkcja sortuje numery dzialek zgodnie z rosnącymi licznikami

    pobiera listę z numerami, zwraca listę list, z licznikiem i mianownikami.

    Sortuje tylko działki z obrębu (z jednakowymi przedrostkami).
    '''
    dzialki = {}
    for i in lista:
        if '.' in i:
            continue
        if '-' in i:
            przedr, i = i.split('-')
        else:
            przedr = None
        licznik_mianownik = i.split('/')
        if len(licznik_mianownik) == 1:
            licznik_mianownik.append(0)
        licznik, mianownik = licznik_mianownik[0], licznik_mianownik[1]
        if not licznik in dzialki:
            dzialki[licznik] = [mianownik]
        else:
            dzialki[licznik].append(mianownik)

    x = []
    posortowane = []
    for i in list(dzialki.keys()):
        x.append(int(i))
    x.sort()
    for i in x:
        if dzialki[repr(i)] != [0]:
            mian = []
            for j in dzialki[repr(i)]:
                mian.append(int(j))
            mian.sort()
            posortowane.append([i, mian])
        else:
            posortowane.append([i, []])
    nposortowane = []
    nr = ''
    for i in posortowane:
        licznik = repr(i[0])
        if i[1]:
            for j in i[1]:
                if j != 0:
                    mianownik = '/{0}'.format(j)
                    if przedr:
                        nr = przedr + '-' + licznik + mianownik
                    else:
                        nr = licznik + mianownik
                    nposortowane.append(nr)
        else:
            mianownik = ''
            if przedr:
                nr = przedr + '-' + licznik + mianownik
            else:
                nr = licznik + mianownik
            nposortowane.append(nr)

    return nposortowane


def dop_odch(pole, skala=None):
    '''Funkcja oblicza dopuszcza odchyłkę pola powierzchni działki

    funkcja pobiera dwa argumenty, drugi opcjonalny - pole powierzchni i skalę
    jeśli jest tylko jeden argument odchyłka jest liczona z wzoru bez
    uwzglednienia skali, jeśli jest podana skala to z nią.
    '''

    if not skala:
        pole = float(pole)
        dp_max = 2 * ((0.002 * pole) + (0.2 * math.sqrt(pole)))
    else:
        dp_max = 2 * ((0.002 * pole) + (0.0004 * skala * math.sqrt(pole)))
    dp_max = decimal.Decimal(repr(dp_max)).quantize(decimal.Decimal('1'))
    return dp_max

def czytaj_prz_baz(plik):
    '''Funkcja czyta plik wygenerowany przez "obliczenie przecięcia" z Ewmapy
    '''
    plik = open(plik, 'r').readlines()
    dzialki = {}
    uzytki = {}

    for linia in plik:
        try:
            nr, uz, pow = linia.split('\n')[0].split()
        except:
            print(linia)
        pow = decimal.Decimal(pow)
        if pow != 0:
            if not nr in list(dzialki.keys()):
                dzialki[nr] = {uz: pow}
            else:
                if not uz in list(dzialki[nr].keys()):
                    dzialki[nr][uz] = pow
                else:
                    dzialki[nr][uz] += pow

    return dzialki

def czytaj_pola(plik):
    '''Funkcja czyta plik wygenerowany przez "przenoszenie pól" z Ewmapy
    '''
    plik = open(plik, 'r').readlines()
    dzialki = {}

    for linia in plik:
        dz = dzialka_pola(linia)
        dzialki[dz.nr] = dz
    return dzialki

def dzialki_z_obrebu(obreb, baza):
    dzialki = []
    for i in baza:
        if baza[i].obreb == obreb:
            dzialki.append(i)
    return dzialki
