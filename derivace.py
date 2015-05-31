#!/usr/bin/python3
import logging
import sys

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
        ('bok', dict(k='1'), {}, set(['úbočí'])),
        ('břeh', dict(k='1'), {}, set(['pobřeží'])),
        ('cesta', dict(k='1'), {}, set(['rozcestí'])),
        ('četa', dict(k='1'), {}, set(['četař', 'četník'])),
        ('doba', dict(k='1'), {}, set(['období'])),
        ('hlava', dict(k='1'), {}, set(['záhlaví'])),
        ('hora', dict(k='1'), {}, set(['horník', 'pohoří'])),
        ('houba', dict(k='1'), {}, set(['houbař'])),
        ('hrad', dict(k='1'), {}, set(['předhradí'])),
        ('hrana', dict(k='1'), {}, set(['rozhraní'])),  # → hranice?
        ('hranice', dict(k='1'), {}, set(['hraničář', 'příhraničí'])),
        ('hvězda', dict(k='1'), {}, set(['souhvězdí'])),
        ('kolo', dict(k='1'), {}, set(['kolař', 'soukolí'])),
        ('led', dict(k='1'), {}, set(['náledí'])),
        ('les', dict(k='1'), {}, set(['podlesí'])),
        ('pádlo', dict(k='1'), {}, set(['pádlař'])),
        ('město', dict(k='1'), {}, set(['náměstí'])),
        ('oko', dict(k='1'), {}, set(['obočí'])),
        ('traktor', dict(k='1'), {}, set(['traktorista'])),
        ('rok', dict(k='1'), {}, set(['výročí'])),
        ('sál', dict(k='1'), {}, set(['předsálí'])),
        # silný → silnice
        ('silnice', dict(k='1'), {}, set(['silničář'])),
        ('skála', dict(k='1'), {}, set(['úskalí'])),  # TODO, teď máme úskálí
        ('sklep', dict(k='1'), {}, set(['předsklepí'])),
        ('slovo', dict(k='1'), {}, set(['úsloví'])),
        ('střecha', dict(k='1'), {}, set(['přístřeší'])),
        ('škola', dict(k='1'), {}, set(['školník'])),
        ('věta', dict(k='1'), {}, set(['souvětí'])),
        ('vzduch', dict(k='1'), {}, set(['ovzduší'])),
        ('závod', dict(k='1'), {}, set(['závodník'])),
        ('zem', dict(k='1'), {}, set(['podzemí', 'území'])),
        ('autorův', dict(k='2'), {}, set()),
        ('blbý', dict(k='2', d='1'), {}, set(['blbější', 'blbě'])),
        ('bosý', dict(k='2', d='1'), {}, set(['bose', 'naboso'])),
        ('český', dict(k='2', d='1'), {}, set(['česky', 'češtější'])),
        ('dobrý', dict(k='2', d='1'), {}, set(['dobře'])),
        ('drahý', dict(k='2', d='1'), {}, set(['dražší', 'dráž'])),  # dráž?
        # důvod → důvodný
        ('důvodný', dict(k='2', d='1'), {}, set(['bezdůvodně'])),  # nemáme
        ('hebký', dict(k='2', d='1'), {}, set(['hebčí'])),  # chceme hebčejší?
        ('hezký', dict(k='2', d='1'), {}, set(['hezčí'])),
        ('hladký', dict(k='2', d='1'), {}, set(['hladší', 'hladce'])),
        ('hloupý', dict(k='2', d='1'), {}, set(['hloupě', 'hloupější'])),
        ('hluchý', dict(k='2', d='1'), {}, set(['hluše', 'hlušší'])),
        ('chrabrý', dict(k='2', d='1'), {}, set(['chrabře', 'chrabřejší'])),
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
        ('povědomý', dict(k='2', d='1'), {}, set(['povědomě', 'povědomější'])),
        ('prostý', dict(k='2', d='1'), {}, set(['prostě', 'prostější',
                                                'prostší'])),
        ('přímý', dict(k='2', d='1'), {}, set(['přímější'])),
        ('skoupý', dict(k='2', d='1'), {}, set(['skoupější', 'skoupě'])),
        ('smutný', dict(k='2', d='1'), {}, set(['smutnější'])),
        ('stálý', dict(k='2', d='1'), {}, set(['stálejší', 'stále'])),
        ('starý', dict(k='2', d='1'), {}, set(['starší', 'staře'])),
        ('špatný', dict(k='2', d='1'), {}, set(['horší', 'špatnější'])),
        ('tenký', dict(k='2', d='1'), {}, set(['tenčí'])),
        ('tvrdý', dict(k='2', d='1'), {}, set(['tvrdě', 'tvrdší'])),
        # pláč → plakat → uplakat → uplakaný
        ('plakat', dict(k='5', e='A', a='I'), {}, set([
            'neplakat', 'doplakat', 'oplakat', 'splakat', 'uplakat',
            'vyplakat', 'zaplakat', 'uplakaný', 'uplakanější', 'uplakaně'])),
        ('úzký', dict(k='2', d='1'), {}, set(['užší'])),
        ('veselý', dict(k='2', d='1'), {}, set(['veselejší'])),
        ('vodní', dict(k='2', d='1'), {}, set([])),
        ('vzácný', dict(k='2', d='1'), {}, set(['vzácnější'])),
        ('zlý', dict(k='2', d='1'), {}, set(['horší', 'zlejší'])),
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


def nastaveni():
    zakazat = False

    for arg in sys.argv:
        if arg == '--zakazat':
            zakazat = True
        elif zakazat:
            zakazat_proces(arg)
            zakazat = False


def zakazat_proces(proces):
    slovni_druh, proces = proces.split('.')
    if slovni_druh == 'Substantivum':
        Substantivum.zakazat_proces(proces)
    elif slovni_druh == 'Adverbium':
        Adverbium.zakazat_proces(proces)


if __name__ == '__main__':
    nastaveni()
    test()
