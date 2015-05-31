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
        ('bok', dict(k='1'), {}, set(['úbočí', 'boční'])),
        ('břeh', dict(k='1'), {}, set(['pobřeží', 'pobřežní'])),
        ('cesta', dict(k='1'), {}, set(['rozcestí'])),
        ('četa', dict(k='1'), {}, set(['četař', 'četník', 'četnický'])),
        ('doba', dict(k='1'), {}, set(['období'])),
        # do+vést?
        ('důvod', dict(k='1'), {}, set(['bezdůvodný', 'bezdůvodně'])),  # TODO
        ('hlava', dict(k='1'), {}, set(['záhlaví'])),
        ('hora', dict(k='1'), {}, set(['horník', 'pohoří', 'horský'])),
        ('houba', dict(k='1'), {}, set(['houbař', 'podhoubí'])),
        ('hrad', dict(k='1'), {}, set(['podhradí', 'předhradí', 'hradní'])),
        ('hrana', dict(k='1'), {}, set(['rozhraní'])),  # → hranice?
        ('hranice', dict(k='1'), {}, set(['hraničář', 'příhraničí',
                                          'hraniční'])),
        ('hvězda', dict(k='1'), {}, set(['souhvězdí', 'hvězdný'])),
        ('kolo', dict(k='1'), {}, set(['kolař', 'soukolí'])),
        # TODO: komornější jen na vyžádání (obvykle se moc nestupňuje)
        ('komora', dict(k='1'), {}, set(['komorní', 'komornější', 'komorně',
                                         'komorník'])),
        ('led', dict(k='1'), {}, set(['náledí', 'lední'])),
        ('les', dict(k='1'), {}, set(['podlesí', 'lesní', 'lesník'])),
        ('pádlo', dict(k='1'), {}, set(['pádlař'])),
        ('město', dict(k='1'), {}, set(['náměstí'])),
        ('oko', dict(k='1'), {}, set(['obočí', 'oční'])),
        ('Olomouc', dict(k='1'), {}, set(['olomoucký', 'olomoucky'])),
        ('Ostrava', dict(k='1'), {}, set(['ostravský', 'ostravsky'])),
        ('Praha', dict(k='1'), {}, set(['pražský'])),
        ('traktor', dict(k='1'), {}, set(['traktorista'])),
        ('rok', dict(k='1'), {}, set(['výročí', 'roční'])),
        ('sál', dict(k='1'), {}, set(['předsálí'])),
        # silný → silnice
        ('silnice', dict(k='1'), {}, set(['silničář', 'silniční'])),
        ('skála', dict(k='1'), {}, set(['úskalí', 'skalní'])),  # máme úskálí
        ('sklep', dict(k='1'), {}, set(['předsklepí', 'sklepní'])),
        ('slovo', dict(k='1'), {}, set(['přísloví', 'úsloví', 'slovní'])),
        ('střecha', dict(k='1'), {}, set(['přístřeší', 'střešní'])),
        ('škola', dict(k='1'), {}, set(['školník', 'školní'])),
        # řídit → úřad?
        ('úřad', dict(k='1'), {}, set(['úřední', 'úředník'])),
        ('věta', dict(k='1'), {}, set(['souvětí', 'větný'])),
        ('voda', dict(k='1'), {}, set(['vodní', 'povodí'])),
        ('vzduch', dict(k='1'), {}, set(['ovzduší', 'vzdušný'])),
        # vést → závod?
        ('závod', dict(k='1'), {}, set(['závodník', 'závodní'])),
        ('zem', dict(k='1'), {}, set(['podzemí', 'území', 'zemní'])),
        ('země', dict(k='1'), {}, set(['zemský'])),
        ('autorův', dict(k='2'), {}, set()),
        ('blbý', dict(k='2', d='1'), {}, set(['blbější', 'blbě'])),
        ('bosý', dict(k='2', d='1'), {}, set(['bose', 'naboso'])),
        ('český', dict(k='2', d='1'), {}, set(['česky', 'češtější'])),
        ('dobrý', dict(k='2', d='1'), {}, set(['dobře'])),
        ('drahý', dict(k='2', d='1'), {}, set(['dražší', 'dráž'])),  # dráž?
        ('hebký', dict(k='2', d='1'), {}, set(['hebčí'])),  # chceme hebčejší?
        ('hezký', dict(k='2', d='1'), {}, set(['hezčí'])),
        ('hladký', dict(k='2', d='1'), {}, set(['hladší', 'hladce'])),
        ('hloupý', dict(k='2', d='1'), {}, set(['hloupě', 'hloupější'])),
        ('hluchý', dict(k='2', d='1'), {}, set(['hluše', 'hlušší'])),
        ('chrabrý', dict(k='2', d='1'), {}, set(['chrabře', 'chrabřejší'])),
        ('krátký', dict(k='2', d='1'), {}, set(['kratší'])),
        ('mělký', dict(k='2', d='1'), {}, set(['mělčí', 'mělce'])),
        ('mladý', dict(k='2', d='1'), {}, set(['mladší'])),
        ('mrtvý', dict(k='2', d='1'), {}, set(['mrtvě', 'domrtva'])),
        ('nahý', dict(k='2', d='1'), {}, set(['donaha'])),
        ('nový', dict(k='2', d='1'), {}, set(['novější'])),
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
