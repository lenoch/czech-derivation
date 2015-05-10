#!/usr/bin/python3

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
        ('drahý', dict(k='2', d='1'), {}, set(['dražší'])),
        ('hebký', dict(k='2', d='1'), {}, set(['hebčí'])),  # chceme hebčejší?
        ('hezký', dict(k='2', d='1'), {}, set(['hezčí'])),
        ('hladký', dict(k='2', d='1'), {}, set(['hladší'])),
        ('horší', dict(k='2', d='2'), {}, set([])),
        ('krátký', dict(k='2', d='1'), {}, set(['kratší'])),
        ('mladý', dict(k='2', d='1'), {}, set(['mladší'])),
        ('nový', dict(k='2', d='1'), {}, set(['novější'])),
        ('pěkný', dict(k='2', d='1'), {}, set(['pěkně'])),
        ('plachý', dict(k='2', d='1'), {}, set(['plašší', 'plaše'])),
        ('přímý', dict(k='2', d='1'), {}, set(['přímější'])),
        ('smutný', dict(k='2', d='1'), {}, set(['smutnější'])),
        ('starý', dict(k='2', d='1'), {}, set(['starší'])),
        ('špatný', dict(k='2', d='1'), {}, set(['špatnější'])),  # chceme?
        ('tenký', dict(k='2', d='1'), {}, set(['tenčí'])),
        ('úzký', dict(k='2', d='1'), {}, set(['užší'])),
        ('veselý', dict(k='2', d='1'), {}, set(['veselejší'])),
        ('vzácný', dict(k='2', d='1'), {}, set(['vzácnější'])),
        ('zlý', dict(k='2', d='1'), {}, set(['zlejší'])),
        ('znamenitý', dict(k='2', d='1'), {}, set(['znamenitější'])),
        # TODO: draze/draho: dráž
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
