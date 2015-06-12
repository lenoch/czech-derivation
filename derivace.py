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
        return Substantivum(None, atributy, vyznamy, lemma)
    elif slovni_druh == '2':
        return Adjektivum(None, atributy, vyznamy, lemma)
    elif slovni_druh == '4':
        # přidat význam +NUM, ale při derivaci postupovat podle deklinace:
        # čtvrtý → čtvrťák („deadjektivum“)
        # pět → páťák („desubstantivum“)
        raise ValueError('Číslovky zatím neumíme rozlišit')
    elif slovni_druh == '5':
        return Verbum(None, atributy, vyznamy, lemma)
    elif slovni_druh == '6':
        return Adverbium(None, atributy, vyznamy, lemma)
    else:
        raise ValueError('Nepodporovaný slovní druh: %s (%s)' % (
            slovni_druh, lemma))


def test():
    pokusy = [
        ('autor', dict(k='1', g='M'), dict(anim=True), set(['autorův', 'autorský', 'autorčin'])),
        ('bok', dict(k='1'), {}, set(['úbočí', 'boční'])),
        ('břeh', dict(k='1'), {}, set(['pobřeží', 'pobřežní'])),
        ('cesta', dict(k='1'), {}, set(['scestí', 'rozcestí', 'rozcestník'])),
        ('čelo', dict(k='1'), {}, set(['průčelí', 'čelní'])),
        ('četa', dict(k='1'), {}, set(['četař', 'četník', 'četnický', 'četařka', 'četnice'])),
        ('doba', dict(k='1'), {}, set(['období', 'dobový'])),
        # do+vést?
        ('důvod', dict(k='1'), {}, set(['bezdůvodný', 'bezdůvodně',
                                        'důvodový'])),  # TODO
        ('dvůr', dict(k='1'), {}, set(['nádvoří', 'dvorský'])),
        ('hlava', dict(k='1', g='F'), {}, set(['záhlaví', 'náhlavní',
                                               'pohlaví', 'pohlavní',
                                               'úhlavní', 'hlavice'])),
        ('hora', dict(k='1'), {}, set(['horník', 'pohoří', 'podhůří', 'horský', 'náhorní'])),
        ('houba', dict(k='1'), {}, set(['houbař', 'podhoubí', 'houbařka',
                                        'hubní', 'houbový', 'houbařský'])),  # TODO: houbařit
        ('housle', dict(k='1'), {'foreign': True},
         set(['houslista', 'houslový'])),
        ('hrad', dict(k='1'), {}, set(['podhradí', 'předhradí', 'hradní'])),
        ('hrana', dict(k='1', g='F'), {}, set(['rozhraní', 'hranice',
                                               'hraničář', 'příhraničí',
                                               'hraniční', 'zahraničí'])),
        ('hvězda', dict(k='1', g='F'), {}, set(['hvězdář', 'souhvězdí',
                                                'hvězdný', 'hvězdice',
                                                'hvězdářský'])),
        ('jeskyně', dict(k='1'), {}, set(['jeskynní', 'jeskyňář'])),
        ('kolo', dict(k='1'), {}, set(['kolař', 'soukolí'])),
        # TODO: komornější jen na vyžádání (obvykle se moc nestupňuje)
        ('komora', dict(k='1'), {}, set(['komorní', 'komornější', 'komorně',
                                         'komorník', 'komornický'])),
        ('led', dict(k='1'), {}, set(['náledí', 'lední', 'ledový'])),
        ('les', dict(k='1'), {}, set(['podlesí', 'lesní', 'lesník', 'lesnický'])),
        ('mícha', dict(k='1', g='F'), {}, set(['míšní'])),  # TODO: nekrátit!
        ('pádlo', dict(k='1'), {}, set(['pádlař', 'pádlařský'])),
        ('město', dict(k='1'), {}, set(['náměstí', 'předměstí'])),
        ('moře', dict(k='1'), {}, set(['úmoří', 'mořský', 'námořní', 'námořník', 'námořnice', 'námořnický'])),
        ('oko', dict(k='1'), {}, set(['obočí', 'oční'])),
        ('Olomouc', dict(k='1'), {}, set(['olomoucký', 'olomoucky'])),
        ('Ostrava', dict(k='1'), {}, set(['ostravský', 'ostravsky'])),
        ('Praha', dict(k='1'), {}, set(['pražský'])),
        ('traktor', dict(k='1'), {'foreign': True},
         set(['traktorista', 'traktoristka'])),  # traktoristický
        ('rok', dict(k='1'), {}, set(['roční', 'výročí'])),
        ('ruka', dict(k='1', g='F'), {}, set(['ruční', 'ručník', 'náručí', 'područí'])),
        ('sál', dict(k='1'), {}, set(['předsálí', 'sálový'])),
        ('síla', dict(k='1', g='F'), {}, set(['silný', 'silnice', 'silničář',
                                              'silniční', 'silový'])),
        ('skála', dict(k='1'), {}, set(['úskalí', 'skalní'])),
        ('sklep', dict(k='1'), {}, set(['předsklepí', 'sklepní'])),
        ('slovo', dict(k='1'), {}, set(['přísloví', 'úsloví', 'slovní'])),  # slovníkář
        ('stopa', dict(k='1'), {}, set(['stopař', 'stopařův', 'stopařka',
                                        'stopový', 'stopařský'])),
        ('střed', dict(k='1'), {}, set(['prostředí', 'ústředí', 'středový',
                                        'střední'])),
        ('střecha', dict(k='1'), {}, set(['přístřeší', 'střešní'])),
        ('škola', dict(k='1'), {}, set(['školní', 'školník', 'školský'])),
        # řídit → úřad?
        ('úřad', dict(k='1'), {}, set(['úřední', 'úředník', 'úřednice', 'úřednický'])),
        ('věta', dict(k='1'), {}, set(['souvětí', 'větný'])),
        ('voda', dict(k='1'), {}, set(['vodní', 'povodí', 'podvodnice', 'vodnický'])),
        ('vzduch', dict(k='1'), {}, set(['ovzduší', 'vzdušný', 'provzdušnit'])),  # TODO
        # vést → závod?  (jinak se „zá“ považuje za součást kořene)
        ('závod', dict(k='1'), {}, set(['závodní', 'závodník', 'závodnice', 'závodnický'])),
        ('zeď', dict(k='1'), {}, set(['zedník', 'zednický'])),  # TODO: ztráta měkkosti!
        ('zem', dict(k='1'), {}, set(['podzemí', 'území', 'zemní'])),
        ('země', dict(k='1'), {}, set(['zemský'])),
        ('blbý', dict(k='2', d='1'), {}, set(['blbější', 'blbě'])),
        ('bosý', dict(k='2', d='1'), {}, set(['bose', 'naboso'])),
        ('český', dict(k='2', d='1'), {}, set(['česky', 'češtější'])),
        ('dlouhý', dict(k='2', d='1'), {}, set(['delší', 'dloužit', 'prodloužit'])),
        ('dobrý', dict(k='2', d='1'), {}, set(['dobře', 'udobřit', 'udobřený'])),
        ('drahý', dict(k='2', d='1'), {}, set(['dražší', 'dráž', 'dražit',
                                               'vydražit'])),  # dráž?
        ('hebký', dict(k='2', d='1'), {}, set(['hebčí'])),  # chceme hebčejší?
        ('hezký', dict(k='2', d='1'), {}, set(['hezčí'])),
        # hlad-i-t → hlad-k-ý?
        ('hladký', dict(k='2', d='1'), {}, set(['hladší', 'hladce'])),
        ('hloupý', dict(k='2', d='1'), {}, set(['hloupě', 'hloupější', 'hlupák', 'hlupácký'])),
        ('hluchý', dict(k='2', d='1'), {}, set(['hluše', 'hlušší'])),
        ('chrabrý', dict(k='2', d='1'), {}, set(['chrabře', 'chrabřejší'])),
        # krát-i-t → krát-k-ý?
        ('krátký', dict(k='2', d='1'), {}, set(['kratší'])),
        ('mělký', dict(k='2', d='1'), {}, set(['mělčí', 'mělce'])),
        ('mladý', dict(k='2', d='1'), {}, set(['mladší'])),
        ('mrtvý', dict(k='2', d='1'), {}, set(['mrtvě', 'domrtva', 'mrtvice'])),
        ('nahý', dict(k='2', d='1'), {}, set(['donaha'])),
        ('nový', dict(k='2', d='1'), {}, set(['novější', 'obnovit'])),
        ('pěkný', dict(k='2', d='1'), {}, set(['pěkně'])),
        ('plachý', dict(k='2', d='1'), {}, set(['plašší', 'plaše', 'plašit'])),
        ('povědomý', dict(k='2', d='1'), {}, set(['povědomě', 'povědomější'])),
        ('prostý', dict(k='2', d='1'), {}, set(['prostě', 'prostější',
                                                'prostší'])),
        ('přímý', dict(k='2', d='1'), {}, set(['přímější', 'přímit', 'přímený'])),
        ('skoupý', dict(k='2', d='1'), {}, set(['skoupější', 'skoupě'])),
        # „posmutnělý“ ať už si vytvoří (m)ajka, to už je flexe a ne derivace
        ('smutný', dict(k='2', d='1'), {}, set(['smutnější', 'smutnit', 'posmutnět'])),
        ('stálý', dict(k='2', d='1'), {}, set(['stálejší', 'stále'])),
        ('starý', dict(k='2', d='1'), {}, set(['starší', 'staře', 'stařec', 'stařecký'])),
        ('suchý', dict(k='2', d='1'), {}, set(['sušší', 'sušit', 'sušený', 'suše'])),
        ('špatný', dict(k='2', d='1'), {}, set(['horší', 'špatnější'])),
        ('tenký', dict(k='2', d='1'), {}, set(['tenčí', 'tenčit'])),
        ('tvrdý', dict(k='2', d='1'), {}, set(['tvrdě', 'tvrdší', 'tvrďák', 'tvrďácký', 'tvrdit', 'tvrzený'])),
        # pláč → plakat → uplakat → uplakaný (zas jen flexe)
        ('plakat', dict(k='5', e='A', a='I'), {}, set([
            'neplakat', 'doplakat', 'oplakat', 'splakat', 'uplakat',
            'vyplakat', 'zaplakat', 'uplakaný', 'uplakanější', 'uplakaně'])),
        # úžit → úz-k-ý?
        ('úzký', dict(k='2', d='1'), {}, set(['užší', 'úžit'])),
        ('veselý', dict(k='2', d='1'), {}, set(['veselejší', 'veselice', 'veselit'])),
        ('vzácný', dict(k='2', d='1'), {}, set(['vzácnější'])),
        ('zlý', dict(k='2', d='1'), {}, set(['horší', 'zlejší'])),
        # znamen-í → znamen-it-ý (je -it- téma?)
        ('znamenitý', dict(k='2', d='1'), {'tema': True}, set(['znamenitější'])),
        # čtený → čtenář
    ]

    chybejici_odvozeniny = []
    for lemma, atributy, vyznamy, ocekavane_odvozeniny in pokusy:
        try:
            slovo = vytvorit_slovni_tvar(lemma, atributy, vyznamy)
        except ValueError as ve:
            logging.exception(ve)

        print(slovo, flush=True)
        slovo.vypsat_odvozeniny(max_hloubka_rekurze=5)

        odvozeniny = set(slovo.lemmata(max_hloubka_rekurze=5))
        chybejici = ocekavane_odvozeniny - odvozeniny
        if chybejici:
            chybejici_odvozeniny.append((lemma, chybejici))

        print('\n', flush=True)

    for lemma, chybejici in chybejici_odvozeniny:
        logging.error('chybí: %s → %s', lemma, ', '.join(chybejici))


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
