#!/usr/bin/python3
import logging

from adjektivum import Adjektivum
from adverbium import Adverbium
from substantivum import Substantivum
from verbum import Verbum


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
    elif slovni_druh == '5':
        return Verbum(None, lemma, atributy, vyznamy)
    elif slovni_druh == '6':
        return Adverbium(None, lemma, atributy, vyznamy)
    else:
        raise ValueError('Nepodporovaný slovní druh: %s (%s)' % (
            slovni_druh, lemma))


def test():
    pokusy = [
        ('četa', dict(k='1'), {}, set(['četař', 'četník'])),
        ('hora', dict(k='1'), {}, set(['horník'])),
        ('houba', dict(k='1'), {}, set(['houbař'])),
        # hrana?
        ('hranice', dict(k='1'), {}, set(['hraničář'])),
        ('kolo', dict(k='1'), {}, set(['kolař'])),
        ('pádlo', dict(k='1'), {}, set(['pádlař'])),
        ('traktor', dict(k='1'), {}, set(['traktorista'])),
        # silný → silnice
        ('silnice', dict(k='1'), {}, set(['silničář'])),
        ('škola', dict(k='1'), {}, set(['školník'])),
        ('závod', dict(k='1'), {}, set(['závodník'])),
        ('blbý', dict(k='2', d='1'), {}, set(['blbější', 'blbě'])),
        ('bosý', dict(k='2', d='1'), {}, set(['bose', 'naboso'])),
        ('český', dict(k='2', d='1'), {}, set(['česky'])),
        ('dobrý', dict(k='2', d='1'), {}, set(['dobře'])),
        ('drahý', dict(k='2', d='1'), {}, set(['dražší', 'dráž'])),
        # důvod → důvodný
        ('důvodný', dict(k='2', d='1'), {}, set(['bezdůvodně'])),
        ('hebký', dict(k='2', d='1'), {}, set(['hebčí'])),  # chceme hebčejší?
        ('hezký', dict(k='2', d='1'), {}, set(['hezčí'])),
        ('hladký', dict(k='2', d='1'), {}, set(['hladší', 'hladce'])),
        ('hloupý', dict(k='2', d='1'), {}, set(['hloupě'])),
        ('hluchý', dict(k='2', d='1'), {}, set(['hluše'])),
        ('horší', dict(k='2', d='2'), {}, set([])),
        ('chrabrý', dict(k='2', d='1'), {}, set(['chrabře'])),
        ('komorní', dict(k='2', d='1'), {}, set(['komornější', 'komorně'])),
        ('krátký', dict(k='2', d='1'), {}, set(['kratší'])),
        ('mělký', dict(k='2', d='1'), {}, set(['mělčí', 'mělce'])),
        ('mladý', dict(k='2', d='1'), {}, set(['mladší'])),
        ('mrtvý', dict(k='2', d='1'), {}, set(['mrtvě', 'domrtva'])),
        ('nahý', dict(k='2', d='1'), {}, set(['donaha'])),
        ('nový', dict(k='2', d='1'), {}, set(['novější'])),
        ('olomoucký', dict(k='2', d='1'), {}, set(['olomoucky'])),
        ('ostravský', dict(k='2', d='1'), {}, set(['ostravsky'])),
        ('pěkný', dict(k='2', d='1'), {}, set(['pěkně'])),
        ('plachý', dict(k='2', d='1'), {}, set(['plašší', 'plaše'])),
        ('povědomý', dict(k='2', d='1'), {}, set(['povědomě'])),
        ('prostý', dict(k='2', d='1'), {}, set(['prostě'])),
        ('přímý', dict(k='2', d='1'), {}, set(['přímější'])),
        ('skoupý', dict(k='2', d='1'), {}, set(['skoupější', 'skoupě'])),
        ('smutný', dict(k='2', d='1'), {}, set(['smutnější'])),
        ('stálý', dict(k='2', d='1'), {}, set(['stálejší', 'stále'])),
        ('starý', dict(k='2', d='1'), {}, set(['starší', 'staře'])),
        ('špatný', dict(k='2', d='1'), {}, set(['špatnější'])),  # chceme?
        ('tenký', dict(k='2', d='1'), {}, set(['tenčí'])),
        ('tvrdý', dict(k='2', d='1'), {}, set(['tvrdě'])),
        # pláč → plakat → uplakat → uplakaný
        ('plakat', dict(k='5', e='A', a='I'), {}, set([
            'neplakat', 'doplakat', 'oplakat', 'splakat', 'uplakat',
            'vyplakat', 'zaplakat', 'uplakaný', 'uplakanější', 'uplakaně'])),
        ('úzký', dict(k='2', d='1'), {}, set(['užší'])),
        ('veselý', dict(k='2', d='1'), {}, set(['veselejší'])),
        ('vodní', dict(k='2', d='1'), {}, set([])),
        ('vzácný', dict(k='2', d='1'), {}, set(['vzácnější'])),
        ('zlý', dict(k='2', d='1'), {}, set(['zlejší'])),
        ('znamenitý', dict(k='2', d='1'), {}, set(['znamenitější'])),
    ]

    for lemma, atributy, vyznamy, ocekavane_odvozeniny in pokusy:
        try:
            slovo = vytvorit_slovni_tvar(lemma, atributy)
        except ValueError as ve:
            logging.exception(ve)

        print(slovo, flush=True)
        slovo.vypsat_odvozeniny(max_hloubka_rekurze=5)

        odvozeniny = set(slovo.lemmata(max_hloubka_rekurze=5))
        chybejici_odvozeniny = ocekavane_odvozeniny - odvozeniny
        if chybejici_odvozeniny:
            logging.error('chybí: %s', ', '.join(chybejici_odvozeniny))

        print('\n', flush=True)


if __name__ == '__main__':
    test()
