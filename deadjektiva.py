from itertools import chain
# import logging

from upravy import uprava_pravopisu


def deadjektiva(lemma, atributy, vyznamy):
    return chain(
        stupnovani(lemma, dict(atributy), set(vyznamy)),
        mladost(lemma, dict(atributy), set(vyznamy)),
        adverbializace(lemma, dict(atributy), set(vyznamy)),
    )


def stupnovani(lemma, atributy, vyznamy):
    stupen = atributy.get('d')  # degree, stupeň
    if stupen is None:
        raise ValueError('Nezadaný stupeň pro ' + str(lemma))
    elif stupen == '1':
        if lemma.endswith('ý'):
            komparativ = uprava_pravopisu(lemma[:-1] + 'ější')
            atributy['d'] = '2'
            yield (komparativ, atributy, vyznamy)
            for vysledek in stupnovani(komparativ, atributy, vyznamy):
                yield vysledek
    elif stupen == '2':
        atributy['d'] = '3'
        yield ('nej' + lemma, atributy, vyznamy)


def mladost(lemma, atributy, vyznamy):
    if atributy.get('d') == '1' and lemma.endswith('ý'):
        del atributy['d']
        atributy.update(k='1', g='F')  # genus, jmenný rod
        yield lemma[:-1] + 'ost', atributy, vyznamy


def adverbializace(lemma, atributy, vyznamy):
    zakonceni = [  # dají se zkrátit díky „pravopisným“ úpravám
        ('dý', 'dě'),
        ('rý', 'ře'),  # rě → ře (už máme)
        ('bý', 'bě'),
        ('vý', 'vě'),
        ('mý', 'mě'),
        ('sý', 'se'),  # sě → se (čeština už nemá měkké ś)
        ('pý', 'pě'),
        ('tý', 'tě'),
        ('lý', 'le'),  # lě → le (ani měkké ľ)
        ('ný', 'ně'),
        ('ní', 'ně'),
        ('chý', 'še'),  # chě → še (historická palatalizace)
        ('hý', 'ze'),  # hě → ze (podobně)
        ('ský', 'sky'),
        ('cký', 'cky'),
        ('ký', 'ce'),  # kě → ce (a taky)
    ]

    if atributy.get('d') == '1':
        atributy['k'] = '6'
        yield lemma[:-1] + 'o', atributy, vyznamy

        # Kvůli ský/cký/chý používám dva cykly.
        # První na rozeznávání posledních tří znaků, druhý na poslední dva znaky
        # Do pravidla se v kazdem cyklu ulozi nektera z dvojic ve zmenach

        for adjektivni, adverbialni in zakonceni:
            if lemma.endswith(adjektivni):
                delka_zakonceni = len(adjektivni)
                yield lemma[:-delka_zakonceni] + adverbialni, atributy, vyznamy

                # Breakuju kvůli pravidlům na "ký" a "hý", která se znovu aplikovala
                # i pro na už jednou zpracovaná "cký/ský" popř. "chý"
                break
