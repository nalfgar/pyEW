#!pythona
# -*- coding: utf-8 -*-

'''
Funkcje obsługujące pomocnicze.
'''

import string
import collections
import decimal
import math

import xlwt

import pyEwmapaLib
import pyEwopisLib

import LS

decimal.getcontext().prec = 10 # ustawienie precyzji na 4 miejsca po przecinku

# kodowanie = 'iso-8859-2'
# kodowanie = 'cp1250'
kodowanie = 'utf-8'


obreb = collections.namedtuple('obreb', 'numer nazwa')
dzialka = collections.namedtuple('dzialka', 'obreb arkusz licznik mianownik pew pewP')
uzytek = collections.namedtuple('uzytek', 'ofu ozu ozk pew')

# lista numerów działek, których nie chcemy kontrolować
dz_nie_do_kontroli = []

def numer_dzialki(dzialka):
    '''Funkcja tworzy numer dzialki np 7.2-14/5 na postawie obiektu dzialka

    zwraca numer'''

    if dzialka.arkusz:
        arkusz = '.{0}'.format(dzialka.arkusz)
    else:
        arkusz = ''
    if dzialka.mianownik:
        mianownik = '/{0}'.format(dzialka.mianownik)
    else:
        mianownik = ''
    nr = '{0}{1}-{2}{3}'.format(dzialka.obreb, arkusz, dzialka.licznik, mianownik)
    return nr

def rozbij_numer(napis):
    '''Funkcja rozbija nr działki 10.5-78/5 na składowe [10,5,78,5]'''
    obr_ark, licz_mian = napis.split('-')
    if '.' in obr_ark:
        obreb, arkusz = obr_ark.split('.')
    else:
        obreb, arkusz = obr_ark, ''
    if r'/' in licz_mian:
        licznik, mianownik = licz_mian.split(r'/')
    else:
        licznik, mianownik = licz_mian, ''
    return obreb, arkusz, licznik, mianownik

def podaj_obreb(napis):
    '''Funkcja zwraca nr obrebu z numeru dzialki'''
    return rozbij_numer(napis)[0]

def podaj_arkusz(napis):
    '''Funkcja zwraca nr arkusza z numeru dzialki'''
    return rozbij_numer(napis)[1]

def podaj_licznik(napis):
    '''Funkcja zwraca licznik z numeru dzialki'''
    return rozbij_numer(napis)[2]

def podaj_mianownik(napis):
    '''Funkcja zwraca mianownik z numeru dzialki'''
    return rozbij_numer(napis)[3]

def podaj_licznik_mianownik(napis):
    '''Funkcja zwraca licznik/mianownik'''
    l = rozbij_numer(napis)[2]
    m = rozbij_numer(napis)[3]
    if m:
        m = '/' + m
    return l + m

def zamien_na_slownik(lista):
    '''Funkcja zamienia listę na słownik z kluczem elementem listy, wartość pusta'''
    slow = {}
    for i in lista:
        slow[i] = ''
    return slow

def porownaj_numery(dz1, dz2):
    '''Funkcja porównuje numerację działek w listach dz1 i dz2

    '''
    nr_dz1_set = set(dz1)
    nr_dz2_set = set(dz2)

    tylko_w_1 = tuple(nr_dz1_set.difference(nr_dz2_set))
    tylko_w_2 = tuple(nr_dz2_set.difference(nr_dz1_set))
    w_obu = tuple(nr_dz1_set.intersection(nr_dz2_set))

    return tylko_w_1, tylko_w_2, w_obu

def drukuj_dzialka_powierzchnia(numery, baza, naglowek):
    '''Funkcja drukuje wykaz działek zawarty w liście numery, z powierzchniami zawartymi w bazie
    z nagłówkiem nagłówek.

    '''
    print(naglowek)
    print('-' * len(naglowek))
    print('{0:20}{1}'.format('nr. dz', 'pow. dz.'))
    print('-' * len(naglowek))
    for i in numery:
        print('{0:20}{1}'.format(i, baza[i].pew.quantize(decimal.Decimal('1'))))
    print()

def drukuj_porownanie_ewmapa_ewopis(numery, baza_ewmapa, baza_ewopis,ozn_przekr_odch=None):
    naglowek = 'Porównanie działek ewopis - ewmapa'
    print(naglowek)
    if ozn_przekr_odch:
        naglowek = '{0} - oznaczenie działki dla której dp > dp_max'.format(ozn_przekr_odch)
    else:
        naglowek = 'Wydrukowano tylko działki dla których dp > dp_max'
    print(naglowek)
    linia = '{0:20}{1:15}{2:15}{3:10}{4}'
    print('-' * (len(linia.format('nr dz.','pow. wektor.','pow. ewid.', 'dp max,','dp'))+2))
    print(linia.format('nr dz.','pow. wektor.','pow. ewid.','dp max.' ,'dp'))
    print('-' * (len(linia.format('nr dz.','pow. wektor.','pow. ewid.','dp max.', 'dp'))+2))
    for i in numery:
        ewmapa_pew = baza_ewmapa[i].pewP.quantize(decimal.Decimal('1'))
        ewopis_pew = baza_ewopis[i].pew.quantize(decimal.Decimal('1'))
        dp = baza_ewmapa[i].pewP-baza_ewopis[i].pew
        dp = dp.quantize(decimal.Decimal('1'))
        dp_abs = dp.copy_abs()
        dp_max = pyEwmapaLib.dop_odch(ewmapa_pew)
        if ozn_przekr_odch:
            linia = '{0:20}{1:15}{2:15}{3:10}{4:6}{5}'
            if dp_abs > dp_max:
                print(linia.format(i,ewmapa_pew,ewopis_pew,dp_max, dp ,ozn_przekr_odch))
            else:
                print(linia.format(i,ewmapa_pew,ewopis_pew,dp_max, dp ,''))
        else:
            if dp_abs > dp_max:
                print(linia.format(i,ewmapa_pew,ewopis_pew,dp_max, dp))
            else:
                pass

def analizuj_nr_dzialek(obreby, dzialki_ewmapa, ozn_blednej_dz = None):
    ''' Funkcja drukuje analizę numerów i powierzchni działek zawartych
    w bazie wektorowej i w rejestrze.

    Pobiera dwa obligatoryjne argumenty listę obrębów dla których będzie
    przeprowadzana analiza, listę działek z bazy wektorowej, i opcjonalny
    argument napis oznaczający działki dla których dp>dp_max. Jeśli agumentu
    opcjonalnego brak to zostaną wydrukowane TYLKO działki dla których dp>dp_max.
    '''
    for obreb in obreby:
        dzialki_ewopis = pyEwopisLib.dzialki_z_obrebu(obreb.numer)
        dzialki_ewmapa_o = pyEwmapaLib.dzialki_z_obrebu(obreb.numer, dzialki_ewmapa)
        tylko_ewopis, tylko_ewmapa, ok = porownaj_numery(dzialki_ewopis, dzialki_ewmapa_o)

        tylko_ewopis_pos = pyEwmapaLib.sortuj_nr_dzialek(tylko_ewopis)
        tylko_ewmapa_pos = pyEwmapaLib.sortuj_nr_dzialek(tylko_ewmapa)

        ok_pos = pyEwmapaLib.sortuj_nr_dzialek(ok)

        linia = ' ***   Analiza numerów działek i powierzchni dla obrębu {0}, {1} ***'.format(obreb.numer.zfill(4), obreb.nazwa.encode(kodowanie))
        print('*' * len(linia))
        print(linia)
        print('*' * len(linia))
        print('Ilość działek w rejestrze: {0}'.format(len(dzialki_ewopis)))
        print('Ilość działek na mapie wektorowej: {0}'.format(len(dzialki_ewmapa_o)))
        print('Ilość działek o zgodnych numerach: {0}'.format(len(ok)))
        print(('*' * len(linia)) + '\n')
        #
        drukuj_dzialka_powierzchnia(tylko_ewopis_pos,dzialki_ewopis,'Działki z rejestru nie mające odpowiednika na mapie wektorowej')
        drukuj_dzialka_powierzchnia(tylko_ewmapa_pos,dzialki_ewmapa,'Działki z mapy wektorowej nie mające odpowiednika w rejestrze')
        drukuj_porownanie_ewmapa_ewopis(ok_pos,dzialki_ewmapa,dzialki_ewopis, ozn_blednej_dz)
        print('\n')

def analizuj_pow_uzytkow(obreby, dzialki_ewmapa, baza_wektorowa, plik, ozn_blednej_dz = None):
    zgodne = open(plik + '_zgodne.txt', 'w')
    nie_zgodne = open(plik + '_nie_zgodne.txt', 'w')

    for obreb in obreby:
        dzialki_ewopis = pyEwopisLib.dzialki_z_obrebu(obreb.numer)
        dzialki_ewmapa_o = pyEwmapaLib.dzialki_z_obrebu(obreb.numer, dzialki_ewmapa)
        tylko_ewopis, tylko_ewmapa, ok = porownaj_numery(dzialki_ewopis, dzialki_ewmapa_o)

        ok_pos = pyEwmapaLib.sortuj_nr_dzialek(ok)

        linia = ' ***   Analiza uzytkow w dzialkach dla obrebu {0}, {1}   ***\n'.format(obreb.numer.zfill(4), obreb.nazwa)
        linia = ('*' * len(linia)) + '\n'
        zgodne.write(linia)
        nie_zgodne.write(linia)
        linia = ' ***   Analiza uzytkow w dzialkach dla obrebu {0}, {1}   ***\n'.format(obreb.numer.zfill(4), obreb.nazwa)
        zgodne.write(linia)
        nie_zgodne.write(linia)
        linia = ('*' * len(linia)) + '\n'
        zgodne.write(linia)
        nie_zgodne.write(linia)
        linia = 'Nr dzialki\n'
        zgodne.write(linia)
        nie_zgodne.write(linia)
        linia = '{0}{1}{2}{3}{4}\n'.format('Oznaczenie'.rjust(20), 'Pow. ewid.'.rjust(15), 'Pow. graf.'.rjust(15), 'dp'.rjust(10), 'dp_max'.rjust(10))
        zgodne.write(linia)
        nie_zgodne.write(linia)
        linia = ('*' * len(linia)) + '\n'
        zgodne.write(linia)
        nie_zgodne.write(linia)


        for dzialka in ok_pos:
        # for dzialka in ['15-1', '15-2']:
            nr_dz_ewmapa = podaj_licznik_mianownik(dzialka)
            # print(nr_dz_ewmapa)
            try:
                uzytki_ewmapa = baza_wektorowa[dzialka]
            except:
                uzytki_ewmapa = []
            uzytki_ewopis = pyEwopisLib.dzialka_uzytki(obreb.numer, nr_dz_ewmapa)

            # drukuj_porownanie_ewmapa_ewopis(ok_pos,dzialki_ewmapa,dzialki_ewopis, ozn_blednej_dz)

            # Ujednolicenie uzytkow
            # ewopis
            uzytki_dzialka_ewopis = set()
            uzytki_dzialka_ewopis_pole = {}
            for uzytek in uzytki_ewopis:
                uz_jednolity = pyEwmapaLib.anal_uzytek(uzytek)
                uz_jednolity = uz_jednolity.replace("£","Ł")
                # print(uz_jednolity.replace("£","Ł"), "ewop")
                uzytki_dzialka_ewopis.add(uz_jednolity)
                uzytki_dzialka_ewopis_pole[uz_jednolity] = decimal.Decimal(repr(uzytek.pew))

            # ewmapa
            uzytki_dzialka_ewmapa = set()
            uzytki_dzialka_ewmapa_pole = {}
            for uzytek in uzytki_ewmapa:
                uz_jednolity = pyEwmapaLib.anal_klasouzytek(uzytek)
                # print(uz_jednolity, "ewmap")
                uzytki_dzialka_ewmapa.add(uz_jednolity)
                uzytki_dzialka_ewmapa_pole[uz_jednolity] = uzytki_ewmapa[uzytek]

            uz_ok = uzytki_dzialka_ewmapa.intersection(uzytki_dzialka_ewopis)
            tylko_ewmapa = uzytki_dzialka_ewmapa.difference(uzytki_dzialka_ewopis)
            tylko_ewopis = uzytki_dzialka_ewopis.difference(uzytki_dzialka_ewmapa)
            # druk działek ze zgodnymi uzytkami
            if uz_ok and not tylko_ewmapa and not tylko_ewopis and dzialka not in dz_nie_do_kontroli:
                ewopis_pew = pyEwopisLib.dzialka_z_obrebu(obreb.numer, nr_dz_ewmapa).pew.quantize(decimal.Decimal('1'))
                ewmapa_pew = dzialki_ewmapa[dzialka].pewP.quantize(decimal.Decimal('1'))
                dp_max = pyEwmapaLib.dop_odch(ewopis_pew)
                dp = ewopis_pew - ewmapa_pew
                if float(dp_max) >= math.fabs(dp):
                    linia = '\n{0}{1}{2}{3}{4}\n'.format(dzialka, ewopis_pew.to_eng_string().rjust(35-len(dzialka)), ewmapa_pew.to_eng_string().rjust(15), dp.to_eng_string().rjust(10), dp_max.to_eng_string().rjust(10))
                elif float(dp_max) < math.fabs(dp):
                    linia = '\n{0}{1}{2}{3}{4} ***\n'.format(dzialka, ewopis_pew.to_eng_string().rjust(35-len(dzialka)), ewmapa_pew.to_eng_string().rjust(15), dp.to_eng_string().rjust(10), dp_max.to_eng_string().rjust(10))
                zgodne.write(linia)

                for j in uz_ok:
                    p_ewopis = uzytki_dzialka_ewopis_pole[j].quantize(decimal.Decimal('1'))
                    p_ewmapa = uzytki_dzialka_ewmapa_pole[j]
                    dp_max = pyEwmapaLib.dop_odch(p_ewopis)
                    dp = p_ewopis - p_ewmapa
                    dp = dp.quantize(decimal.Decimal('1'))

                    if float(dp_max) >= math.fabs(dp):
                        linia = '{0}{1}{2}{3}{4}\n'.format(j.rjust(20), p_ewopis.to_eng_string().rjust(15), p_ewmapa.to_eng_string().rjust(15), dp.to_eng_string().rjust(10), dp_max.to_eng_string().rjust(10))
                    elif float(dp_max) < math.fabs(dp):
                        pass
                        linia = '{0}{1}{2}{3}{4} ***\n'.format(j.rjust(20), p_ewopis.to_eng_string().rjust(15), p_ewmapa.to_eng_string().rjust(15), dp.to_eng_string().rjust(10), dp_max.to_eng_string().rjust(10))
                    zgodne.write(linia)
            # druk działek z NIEzgodnymi uzytkami
            elif dzialka not in dz_nie_do_kontroli:
                ewopis_pew = pyEwopisLib.dzialka_z_obrebu(obreb.numer, nr_dz_ewmapa).pew.quantize(decimal.Decimal('1'))
                ewmapa_pew = dzialki_ewmapa[dzialka].pew.quantize(decimal.Decimal('1'))
                dp_max = pyEwmapaLib.dop_odch(ewopis_pew)
                dp = ewopis_pew - ewmapa_pew
                if float(dp_max) >= math.fabs(dp):
                    linia = '\n{0}{1}{2}{3}{4}\n'.format(dzialka, ewopis_pew.to_eng_string().rjust(35-len(dzialka)), ewmapa_pew.to_eng_string().rjust(15), dp.to_eng_string().rjust(10), dp_max.to_eng_string().rjust(10))
                elif float(dp_max) < math.fabs(dp):
                    linia = '\n{0}{1}{2}{3}{4} ***\n'.format(dzialka, ewopis_pew.to_eng_string().rjust(35-len(dzialka)), ewmapa_pew.to_eng_string().rjust(15), dp.to_eng_string().rjust(10), dp_max.to_eng_string().rjust(10))
                nie_zgodne.write(linia)
                if uz_ok:
                    for j in uz_ok:
                        p_ewopis = uzytki_dzialka_ewopis_pole[j].quantize(decimal.Decimal('1'))
                        p_ewmapa = uzytki_dzialka_ewmapa_pole[j]
                        dp_max = pyEwmapaLib.dop_odch(p_ewopis)
                        dp = p_ewopis - p_ewmapa
                        dp = dp.quantize(decimal.Decimal('1'))

                        if float(dp_max) >= math.fabs(dp):
                            linia = '{0}{1}{2}{3}{4}\n'.format(j.rjust(20), p_ewopis.to_eng_string().rjust(15), p_ewmapa.to_eng_string().rjust(15), dp.to_eng_string().rjust(10), dp_max.to_eng_string().rjust(10))
                        elif float(dp_max) < math.fabs(dp):
                            linia = '{0}{1}{2}{3}{4}\n'.format(j.rjust(20), p_ewopis.to_eng_string().rjust(15), p_ewmapa.to_eng_string().rjust(15), dp.to_eng_string().rjust(10), dp_max.to_eng_string().rjust(10))
                        nie_zgodne.write(linia)

                if tylko_ewopis:
                    for j in tylko_ewopis:
                        #print dzialka, j
                        p_ewopis = uzytki_dzialka_ewopis_pole[j].quantize(decimal.Decimal('1'))
                        p_ewmapa = ''
                        dp_max = pyEwmapaLib.dop_odch(p_ewopis)
                        dp = ''
                        try:
                            linia = '{0}{1}{2}{3}{4} tylko w rej.\n'.format(j.rjust(20), p_ewopis.to_eng_string().rjust(15), p_ewmapa.rjust(15), dp.rjust(10), dp_max.to_eng_string().rjust(10))
                        except:
                            #pass
                            print(dzialka,j, p_ewopis, p_ewmapa, dp, dp_max)
                        # print(linia)
                        nie_zgodne.write(linia.encode(kodowanie).decode(kodowanie))
                if tylko_ewmapa:
                    for j in tylko_ewmapa:
                        p_ewopis = ''
                        p_ewmapa = uzytki_dzialka_ewmapa_pole[j]
                        dp_max = pyEwmapaLib.dop_odch(p_ewmapa)
                        dp = ''

                        linia = '{0}{1}{2}{3}{4} tylko w wek.\n'.format(j.rjust(20), p_ewopis.rjust(15), p_ewmapa.to_eng_string().rjust(15), dp.rjust(10), dp_max.to_eng_string().rjust(10))
                        nie_zgodne.write(linia)
    zgodne.close()
    nie_zgodne.close()

def analizuj_uzytki(obreby, dzialki_ewmapa):
    ''' Funkcja sprawdza
    '''
    for obreb in obreby:
        dzialki_ewopis = pyEwopisLib.dzialki_z_obrebu(obreb.numer)
        dzialki_ewmapa_o = pyEwmapaLib.dzialki_z_obrebu(obreb.numer, dzialki_ewmapa)
        tylko_ewopis, tylko_ewmapa, ok = porownaj_numery(dzialki_ewopis, dzialki_ewmapa_o)

        tylko_ewopis_pos = pyEwmapaLib.sortuj_nr_dzialek(tylko_ewopis)
        tylko_ewmapa_pos = pyEwmapaLib.sortuj_nr_dzialek(tylko_ewmapa)

        ok_pos = pyEwmapaLib.sortuj_nr_dzialek(ok)

        for i in ok_pos:
            nr_dz = podaj_licznik_mianownik(i)
            for j in pyEwopisLib.dzialka_uzytki(obreb.numer, nr_dz):
                pyEwmapaLib.anal_uzytek(j, nr_dz)

def tworz_badanie_KW(nr_obr, kodowanie):
    '''Funkcja tworzy plik xls do porównania danych w EGB z danymi z KW.

    Pobiera numer obrębu dla którego ma utworzyć dane i kodowanie pliku wynikowego.
    Tworzy plik dyskowy xls.

    TODO:
    Funkcja nie działa dobrze dla działek, które mają na przykład dwie KW
    '''
    dzialki = {}
    dzialki_l = []

    dzialki_z_ksiegami = pyEwopisLib.do_badania_KW(nr_obr)

    for i in dzialki_z_ksiegami:
        nr = i[1]
        if not nr in list(dzialki.keys()):
            dzialki[nr] = [i]
        else:
            dzialki[nr].append(i)

    licznik_dz = 1
    licznik_xls = 0

    wb = xlwt.Workbook()
    ws = wb.add_sheet('EGB-KW')
    #overwriteOk = ws._cell_overwrite_ok
    ws._cell_overwrite_ok = True

    ldz = []
    for i in dzialki:
        ldz.append(i)
    pos = pyEwmapaLib.sortuj_nr_dzialek(ldz)

    for i in pos:
        if len(dzialki[i]) == 1:
            ws.write(licznik_xls,0, licznik_dz)
            ws.write(licznik_xls,1, dzialki[i][0][0])
            ws.write(licznik_xls,2, dzialki[i][0][1])
            ws.write(licznik_xls,3, dzialki[i][0][2])
            ws.write(licznik_xls,4, dzialki[i][0][3])
            ws.write(licznik_xls,5, dzialki[i][0][4])

            licznik_xls += 1
        else:
            ile_udzialow = len(dzialki[i])
            ws.merge(licznik_xls, licznik_xls+ile_udzialow-1, 0,0)
            ws.write(licznik_xls, 0, licznik_dz)
            ws.merge(licznik_xls, licznik_xls+ile_udzialow-1, 1,1)
            ws.write(licznik_xls, 1, dzialki[i][0][0])
            ws.merge(licznik_xls, licznik_xls+ile_udzialow-1, 2,2)
            ws.write(licznik_xls, 2, dzialki[i][0][1])

            ws.merge(licznik_xls, licznik_xls+ile_udzialow-1, 3,3)
            ws.write(licznik_xls, 3, dzialki[i][0][2])
            for j in range(ile_udzialow):
                ws.write(licznik_xls,4, dzialki[i][j][3])
                ws.write(licznik_xls,5, dzialki[i][j][4])
                licznik_xls += 1
        licznik_dz += 1
    teryt = pyEwopisLib.teryt()
    plik_xls = '{0}.{1}_wykaz_rozb_EGB-KW.xls'.format(teryt[0][1], nr_obr.zfill(4))
    wb.save(plik_xls)

def m2ha(metry):
    '''Funkcja zamienia metry kwadratowe na hektary, z dokladnoscia do 1m (0.0001)

    Zwraca napis'''

    decimal.getcontext().prec = 4
    m = decimal.Decimal(metry)
    ha = m/10000
    try:
        calk, ulam = ha.to_eng_string().split('.')
    except ValueError:
        calk = ha.to_eng_string()
        ulam = '0'
    if len(ulam) < 4:
        brak = 4-len(ulam)
        zera = ''.zfill(brak)
        ulam = ulam + zera
    return '{0}.{1}'.format(calk, ulam)

def tworz_wypis_z_rej(obreb):
    '''Funkcja tworzy wypisy z rejestru gruntów w formacie csv'''

    woj = '26'
    pow = '04'
    gmi = '045'
    oobr = obreb.zfill(4)
    teryt = woj + pow + gmi + '.' + oobr + '-'

    if pow == '01' and gmi == '015':
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '032':
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '052':
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '062':
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '072':
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '022' and (oobr in ['0001','0007','0008','0011','0013','0018','0023']):
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '022' and (oobr in ['0004','0005','0006','0014','0021','0022','0026']):
        nr_obr_lesnego = '1'

    elif pow == '04' or pow == '08':
        nr_obr_lesnego = '1'

    elif pow == '12' and gmi == '032':
        nr_obr_lesnego = '2'
    elif pow == '12' and gmi == '082':
        nr_obr_lesnego = '1'


    kat_wyj = r'd:\zest_gruntow\\' + woj + pow + gmi + '\\'

    plik_wyj = kat_wyj + oobr + '.csv'
    plik_wyj = open(plik_wyj, 'w')
    dzialki = {}
    licznik = 1
    dzialki_ewopis = pyEwopisLib.dzialki_uzytki_z_obrebu(obreb)
    linia = 'Lp.;nr obr. lesn;nr ark mapy;nr oddzialu;Wojewodztwo;Powiat;Gmina;Obreb;Nr dzialki;Pow. dzialki;OFU;OZU;OZK;Pow. uzytku\n'
    plik_wyj.write(linia)
    linia = ';\n'
    plik_wyj.write(linia)
    for i in dzialki_ewopis:
        if not i[0] in list(dzialki.keys()):
            dzialki[i[0]] = [i]
        else:
            dzialki[i[0]].append(i)
    for i in dzialki:
        ddz = teryt + i
        # przypisanie działce odpowiedniego numeru arkusza mapy Leśnej
        if ddz in LS.dz_ark_LS:
            nr_ark_LS = LS.dz_ark_LS[ddz]
        else:
            nr_ark_LS = 'ARKUSZ'
            linia = 'dla {0} brak arkusza mapy'.format(ddz)
            print(linia)

        # przypisanie działce odpowiedniego numeru oddziału Leśnego
        if ddz in LS.dz_oddz_LS:
            nr_odd_LS = LS.dz_oddz_LS[ddz]
        else:
            nr_odd_LS = 'ODDZIAL'
            linia = 'dla {0} brak oddzialu'.format(ddz)
            print(linia)


        linia = '"{0}";"{1}";"{2}";"{3}";"{4}";"{5}";"{6}";"{7}";"{8}";{9}\n'.format(licznik,nr_obr_lesnego,nr_ark_LS,nr_odd_LS,woj,pow,gmi,oobr,i, m2ha(int(dzialki[i][0][1])))
        plik_wyj.write(linia)
        for j in dzialki[i]:
            if j[3] == None and j[4] == None:
                linia = ';;;;;;;;;;{0};{1};{2};{3}\n'.format(j[2],'','',m2ha(int(j[5])))
            else:
                try:
                    linia = ';;;;;;;;;;{0};{1};{2};{3}\n'.format(j[2].encode(kodowanie),j[3].encode(kodowanie),j[4].encode(kodowanie),m2ha(int(j[5])))
                except:
                    print(j)

            plik_wyj.write(linia)
        linia = ';\n'
        plik_wyj.write(linia)
        licznik += 1
    plik_wyj.close()

def tworz_wypis_z_rej_skr(obreb):
    '''Funkcja tworzy wypisy z rejestru gruntów (tylko teryt i nr dzialki)w formacie csv'''

    woj = '26'
    pow = '01'
    gmi = '015'
    oobr = obreb.zfill(4)
    teryt = woj + pow + gmi + '.' + oobr + '-'

    if pow == '01' and gmi == '015':
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '032':
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '052':
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '062':
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '072':
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '022' and (oobr in ['0001','0007','0008','0011','0013','0018','0023']):
        nr_obr_lesnego = '2'
    elif pow == '01' and gmi == '022' and (oobr in ['0004','0005','0006','0014','0021','0022','0026']):
        nr_obr_lesnego = '1'

    elif pow == '04' or pow == '08':
        nr_obr_lesnego = '1'

    elif pow == '12' and gmi == '032':
        nr_obr_lesnego = '2'
    elif pow == '12' and gmi == '082':
        nr_obr_lesnego = '1'


    kat_wyj = r'd:\zest_gruntow\\' + woj + pow + gmi + '\\'
    plik_wyj = kat_wyj + oobr + '.csv'
    plik_wyj = open(plik_wyj, 'w')
    dzialki = {}
    licznik = 1
    dzialki_ewopis = pyEwopisLib.dzialki_uzytki_z_obrebu(obreb)
    #linia = 'Lp.;Wojewodztwo;Powiat;Gmina;Obreb;Nr dzialki;Nr oddzialu\n'
    #plik_wyj.write(linia)
    linia = ';\n'
    plik_wyj.write(linia)
    for i in dzialki_ewopis:
        if not i[0] in list(dzialki.keys()):
            dzialki[i[0]] = [i]
        else:
            dzialki[i[0]].append(i)
    for i in dzialki:
        linia = '{0};"{1}";"{2}";"{3}";"{4}";"{5}";"{6}"\n'.format(licznik,nr_obr_lesnego,woj,pow,gmi,oobr,i)
        plik_wyj.write(linia)
        licznik += 1
    plik_wyj.close()
