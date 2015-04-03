from itertools import chain
# import logging

from upravy import palatalizace


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
            komparativ = palatalizace(lemma[:-1] + 'ější')
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
    if atributy.get('d') == '1':
        atributy['k'] = '6'
        yield lemma[:-1] + 'o', atributy, vyznamy

        if lemma[-3:] in ('cký', 'ský'):
            yield lemma[:-1] + 'y', atributy, vyznamy
        elif lemma[-1] in ('í', 'ý'):
            kmen = lemma[:-1]
            yield palatalizace(kmen + 'ě'), atributy, vyznamy
