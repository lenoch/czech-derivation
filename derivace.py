import logging

from adjektivum import Adjektivum
from adverbium import Adverbium
from substantivum import Substantivum


def vytvorit_slovni_tvar(lemma, atributy={}, vyznamy={}):
    slovni_druh = atributy.get('k')  # kind, slovní druh, part of speech (POS)
    if slovni_druh is None:
        raise ValueError('Nezadaný slovní druh pro ' + str(lemma))
    elif slovni_druh == '1':
        return Substantivum(None, lemma, atributy, vyznamy)
    elif slovni_druh == '2':
        return Adjektivum(None, lemma, atributy, vyznamy)
    elif slovni_druh == '4':
        # přidat význam +NUM, ale při derivaci postupovat podle deklinace:
        # čtvrtý → čtvrťák („deadjektivum“)
        # pět → páťák („desubstantivum“)
        raise ValueError('Číslovky zatím neumíme rozlišit')
    elif slovni_druh == '6':
        return Adverbium(None, lemma, atributy, vyznamy)
    else:
        raise ValueError('Nepodporovaný slovní druh: %s (%s)' % (
            slovni_druh, lemma))


def test():
    pokusy = [
        ('dobrý', dict(k='2', d='1'), {}, set(['dobře'])),
        ('horší', dict(k='2', d='2'), {}, set([])),
        ('pěkný', dict(k='2', d='1'), {}, set(['pěkně'])),
        ('starý', dict(k='2', d='1'), {}, set(['starší'])),
    ]

    for lemma, atributy, vyznamy, ocekavane_odvozeniny in pokusy:
        try:
            slovo = vytvorit_slovni_tvar(lemma, atributy)
        except ValueError as ve:
            logging.exception(ve)

        print(slovo)

        # (zatím?) se ověřují jen přímé derivace
        odvozeniny = set(odvozenina.lemma for odvozenina in slovo.odvozeniny())
        chybejici_odvozeniny = ocekavane_odvozeniny - odvozeniny
        if chybejici_odvozeniny:
            logging.error('chybí: %s', ', '.join(chybejici_odvozeniny))

        slovo.vypsat_odvozeniny(max_hloubka_rekurze=5)
        print('\n')


if __name__ == '__main__':
    test()
