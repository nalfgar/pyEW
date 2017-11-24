#!pythona
# -*- coding: utf-8 -*-

'''
Funkcje obsługujące Ewopis.
'''


import fdb
import decimal

import pyEwLib
import pyEwmapaLib

# kodowanie = 'iso-8859-2'
# kodowanie = 'cp1250'
kodowanie = 'utf-8'


# podłączenie do zdalnego serwera
#~ ewopis = fdb.connect(dsn='192.168.0.172:/var/lib/firebird/2.5/data/2611022.fdb',
#~ ewopis = fdb.connect(dsn='192.168.0.172:/var/lib/firebird/2.5/data/1818032.fdb',
        #~ user='SYSDBA',
        #~ password='qqq')
# podłączenie do serwera lokalnego
ewopis = fdb.connect(dsn='D:\\GEODEZJA\\EWOPIS\\2601015.fdb',
        user='sysdba',
        password='qqq')


ewopis_cursor = ewopis.cursor()


def teryt():
    """Funkcja znajduje w bazie dane na temat jednostki ewidencyjnej

    """
    pytanie = """SELECT
                    gmina, numer, woje, powiat
                FROM
                    system"""
    ewopis_cursor.execute(pytanie)
    dane = ewopis_cursor.fetchall()
    return dane


def obreby():
    """Funkcja znajduje w bazie ewopis dane nt obrębów,

    zwraca listę"""
    pytanie = """SELECT
                    id, naz
                FROM
                    obreby
                ORDER BY id"""
    ewopis_cursor.execute(pytanie)
    dane = ewopis_cursor.fetchall()
    obreby = []
    for i in dane:
        o = pyEwLib.obreb(repr(i[0]),i[1])
        obreby.append(o)
    return obreby

def dzialka_z_obrebu(obreb, dzialka):
    """Funkcja znajduje w bazie ewopis powierzchnie działki z obrebu: obreb

    zwraca element dzialka (named tuple)"""
    pytanie = """SELECT
                    idd, pew
                FROM
                    dzialka
                WHERE
                    idobr='{0}' and
                    idd='{1}'""".format(obreb, dzialka)
    ewopis_cursor.execute(pytanie)
    dane = ewopis_cursor.fetchall()
    nr, pew = dane[0]
    if '.' in nr:
        arkusz, numer = nr.split('.')
        if r'/' in numer:
            licznik, mianownik = numer.split(r'/')
        else:
            licznik, mianownik = numer, ''
    else:
        arkusz, numer = '', nr
        if r'/' in numer:
            licznik, mianownik = numer.split(r'/')
        else:
            licznik, mianownik = numer, ''
    pew = decimal.Decimal(str(pew))
    u = pyEwLib.dzialka(obreb, arkusz, licznik, mianownik, pew, 0)
    return u

def dzialki_z_obrebu(obreb):
    """Funkcja znajduje w bazie ewopis wszystkie działki z obrebu: obreb

    zwraca listę zawierającą nazwane krotki"""

    pytanie = """SELECT
                    idd,
                    pew
                FROM
                    dzialka
                WHERE
                    status in (0,1) and
                    pew is not Null and
                    idobr='{0}'
                ORDER BY
                    idd""".format(obreb)
    ewopis_cursor.execute(pytanie)
    dane = ewopis_cursor.fetchall()
    linia = ''
    dzialki = {}
    for i in dane:
        linia = '{0}-{1}\t{2}\t{3}'.format(obreb, i[0], i[1], '0.0000')
        dz = pyEwmapaLib.dzialka_pola(linia)
        dzialki[dz.nr] = dz
    return dzialki

def dzialka_uzytki(obreb, dzialka):
    """Funkcja znajduje w bazie ewopis dzialkę z użytkami z obrebu: obreb,

    zwraca listę"""
    pytanie = """SELECT
                    d.pew as pow_dzialki,
                    u.ofu, u.ozu, u.ozk as klasa,
                    u.pew as pow_klasy
                FROM
                    dzialka d,
                    uzytki u
                WHERE
                    d.idd='{0}' and
                    u.rdze=d.id and
                    d.status in (0,1) and
                    d.idobr='{1}'
                ORDER BY
                    idd""".format(dzialka, obreb)
    ewopis_cursor.execute(pytanie)
    dane = ewopis_cursor.fetchall()
    uzytki = []
    for i in dane:
        u = pyEwLib.uzytek(i[1],i[2],i[3],i[4])
        uzytki.append(u)
    return uzytki

def dzialki_uzytki_z_obrebu(obreb):
    """Funkcja znajduje w bazie ewopis wszystkie działki z użytkami z obrebu: obreb,

    zwraca listę"""
    pytanie = """SELECT
                    d.idd as dzialka,
                    d.pew as pow_dzialki,
                    u.ofu, u.ozu, u.ozk as klasa,
                    u.pew as pow_klasy
                FROM
                    dzialka d,
                    uzytki u
                WHERE
                    u.rdze=d.id and
                    d.status in (0,1) and
                    u.status in (0,1) and
                    d.idobr='{0}'
                ORDER BY
                    d.idd""".format(obreb)
    ewopis_cursor.execute(pytanie)
    return ewopis_cursor.fetchall()

def dzialka_uzytki_z_obrebu(obreb, dzialka):
    """Funkcja znajduje w bazie ewopis działkę:dzialka z użytkami z obrebu: obreb,

    zwraca listę"""
    pytanie = """SELECT
                    d.pew as pow_dzialki,
                    u.ofu, u.ozu, u.ozk as klasa,
                    u.pew as pow_klasy
                FROM
                    dzialka d,
                    uzytki u
                WHERE
                    u.rdze=d.id and
                    d.status in (0,1) and
                    d.idobr='{0}' and
                    d.idd='{1}'""".format(obreb, dzialka)
    ewopis_cursor.execute(pytanie)
    return ewopis_cursor.fetchall()

def dzialka_z_obrebu_z_jednostki(obreb, jednostka):
    """Funkcja znajduje w bazie ewopis wszystkie działki z użytkami z obrebu: obreb,

    zwraca listę"""
    pytanie = """SELECT
                    d.IDD as DZIALKA
                FROM
                    dzialka d
                JOIN
                    jedn_rej j on j.id=d.rjdr and j.sti in (0,1)
                    where d.status in (0,1) and
                    d.idobr='{0}' and
                    j.ijr='{1}'""".format(obreb, jednostka)
    ewopis_cursor.execute(pytanie)
    return ewopis_cursor.fetchall()

def do_badania_KW(obreb):
    '''Funkcja pobiera dane konieczne do stworzenia '''

    pytanie = """SELECT DISTINCT
                    DOKUMENTY.SYG AS DOKUMENT,
                    DZIALKA.IDD AS DZIALKA,
                    DZIALKA.PEW AS POWIERZCHNIA,
                    UDZIALY.UD AS UDZIAL,
                    PODMIOTY.NAZWA AS PODMIOT
                FROM
                    DZIALKA
                    LEFT JOIN JEDN_REJ ON (JEDN_REJ.ID=DZIALKA.RJDR AND JEDN_REJ.STI IN (0,1))
                    LEFT JOIN UDZIALY ON (UDZIALY.ID_JEDN=JEDN_REJ.ID AND UDZIALY.STI IN (0,1))
                    LEFT JOIN PODMIOTY ON (PODMIOTY.ID_PDM=UDZIALY.ID_PODM)
                    LEFT JOIN UZYTKI ON (DZIALKA.ID = UZYTKI.RDZE AND UZYTKI.STATUS IN (0,1))
                    LEFT JOIN DOKUMENTY_DZIALKI_RPWL ON (DZIALKA.ID = DOKUMENTY_DZIALKI_RPWL.IDDZ)
                    LEFT JOIN DOKUMENTY ON (DOKUMENTY_DZIALKI_RPWL.IDDOK = DOKUMENTY.ID AND DOKUMENTY_DZIALKI_RPWL.STATUS IN (0,1))
                WHERE
                    (DZIALKA.IDOBR = '{0}') AND
                    (DZIALKA.STATUS IN (0,1))  AND
                    (DOKUMENTY.SYG like 'TB%' or DOKUMENTY.SYG like 'KW%' or DOKUMENTY.SYG like 'LWH%')
                ORDER BY
                    DOKUMENT, DZIALKA""".format(obreb)
    ewopis_cursor.execute(pytanie)
    return ewopis_cursor.fetchall()

def dzialka_KW(obreb):
    '''Funkcja pobiera dane konieczne do stworzenia '''

    pytanie = """select distinct d.IDD as DZIALKA, dok.SYG as DOKUMENT
                from dzialka d
                join jedn_rej j on j.id=d.rjdr and j.sti in (0,1)
                left join dokumenty_dzialki_rpwl rpwl on rpwl.iddz=d.id and rpwl.status in (0,1)
                left join dokumenty dok on dok.id=rpwl.iddok and dok.kdk=5
                where d.status in (0,1) AND d.IDOBR = '{0}' AND dok.SYG IS NOT Null
                """.format(obreb)
    ewopis_cursor.execute(pytanie)
    return ewopis_cursor.fetchall()


def ewopisWIN2_do_porownywarki(dzialki_uzytki):
    '''Funkcja miała tak formatować dane z bazy Firebird aby je można było
    zaimportować do programu porównywarka użytków v. 3.xx'''

    for i in dzialki_uzytki:
        nr_dz = i[0]
        pew = i[1]
        ofu = i[2]
        ozu = i[3]
        ozk = i[4]
        pew_u = i[5]

        print("'1-{0}'\t{1}\t'{2}'\t'{3}'\t'{4}'\t{5}".format(nr_dz, pew, ofu.encode(kodowanie), ozu.encode(kodowanie), ozk.encode(kodowanie), pew_u))

