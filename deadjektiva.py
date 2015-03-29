import logging

from upravy import uprava_pravopisu


def deadjektiva(lemma, atributy, vyznamy):
    for vysledek in stupnovani(lemma, atributy, vyznamy):
        yield vysledek


def stupnovani(lemma, atributy, vyznamy):
    stupen = atributy.get('d')
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
