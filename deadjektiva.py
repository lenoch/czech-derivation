from itertools import chain
# import logging

from upravy import uprava_pravopisu
from transformace_hlasek import alternace1
from transformace_hlasek import kraceni


def deadjektiva(lemma, atributy, vyznamy):
    return chain(
        stupnovani(lemma, dict(atributy), set(vyznamy)),
        mladost(lemma, dict(atributy), set(vyznamy)),
    )


def stupnovani(lemma, atributy, vyznamy):
    stupen = atributy.get('d')
    likvidy = ['l','r'] # připojuje se "ejší"
    jat = ['n', 'm', 'v', 't'] # zde se bude připojovat "ější"
    bezjotace = ['d', 'p', 'h', 'k'] #spadá sem i ch; připojuje se jen "ší", případné krácení v kořeni
    nepravidelne = {'starý':'starší', 'velký':'větší', 'malý':'menší', 'špatný':'horší', 'dobrý':'lepší', 'široký':'širší'}

    if stupen is None:
        raise ValueError('Nezadaný stupeň pro ' + str(lemma))
    elif stupen == '1':
        if lemma in nepravidelne:
            komparativ = nepravidelne[lemma]
        elif lemma[-2] in jat:
            komparativ = uprava_pravopisu(lemma[:-2] + alternace1(lemma[-2]) + 'ější')
        elif lemma[-2] in likvidy:
            komparativ = uprava_pravopisu(lemma[:-2] + alternace1(lemma[-2]) + 'ejší')
        elif lemma[-2] in bezjotace:
            if lemma[-3:-1] == "ch": # ošetření ch
                komparativ = uprava_pravopisu(lemma[:-3] + alternace1(lemma[-3:-1]) + 'ší')
            elif lemma[-2] == 'k': # krátký > kratší
                komparativ = uprava_pravopisu(lemma[:-4] + kraceni(lemma[-4]) + alternace1(lemma[-3]) + 'ší')
                # když vím, na jaké pozici se objeví samohláska, kterou je možné zkrátit, nemusím už používat další seznamy
            else:
                komparativ = uprava_pravopisu(lemma[:-2] + alternace1(lemma[-2]) + 'ší')
        else:
            komparativ = uprava_pravopisu(lemma[:-2] + alternace1(lemma[-2]) + 'í')
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
