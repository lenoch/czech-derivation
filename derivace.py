#!/usr/bin/python3
import logging
import sys

from adjektivum import Adjektivum
from adverbium import Adverbium
from substantivum import Substantivum
from verbum import Verbum


def test():
    pokusy = [
        (Substantivum(lemma='autor', atributy=dict(g='M'), vyznamy=dict(
            anim=True)), ['autorův', 'autorský', 'autorčin']),
        (Substantivum(lemma='bok'), ['úbočí', 'boční']),
        (Substantivum(lemma='břeh'), ['pobřeží', 'pobřežní']),
        (Substantivum(lemma='cesta'), ['scestí', 'rozcestí', 'rozcestník']),
        (Substantivum(lemma='čelo'), ['průčelí', 'čelní']),
        (Substantivum(lemma='četa'), ['četař', 'četník', 'četnický', 'četařka',
                                      'četnice']),
        (Substantivum(lemma='doba'), ['období', 'dobový']),
        # do+vést?
        (Substantivum(lemma='důvod'), ['důvodový', 'bezdůvodný',
                                       'bezdůvodně']),  # TODO: oboje
        (Substantivum(lemma='dvůr'), ['nádvoří', 'dvorský']),
        (Substantivum(lemma='hlava', atributy=dict(g='F')), [
            'záhlaví', 'náhlavní', 'pohlaví', 'pohlavní', 'úhlavní',
            'hlavice']),
        (Substantivum(lemma='hora'), ['horník', 'pohoří', 'podhůří', 'horský',
                                      'náhorní']),
        (Substantivum(lemma='houba'), ['houbař', 'podhoubí', 'houbařka',
                                       'hubní', 'houbový', 'houbařský',
                                       'houbařit']),  # TODO
        (Substantivum(lemma='housle', vyznamy=dict(cizi=True)), ['houslista',
                                                                 'houslový']),
        (Substantivum(lemma='hrad'), ['podhradí', 'předhradí', 'hradní']),
        (Substantivum(lemma='hrana', atributy=dict(g='F')), [
            'rozhraní', 'hranice', 'hraničář', 'příhraničí', 'hraniční',
            'zahraničí']),
        (Substantivum(lemma='hvězda', atributy=dict(g='F')), [
            'hvězdář', 'souhvězdí', 'hvězdný', 'hvězdice', 'hvězdářský']),
        (Substantivum(lemma='jeskyně'), ['jeskynní', 'jeskyňář']),
        (Substantivum(lemma='kolo'), ['kolař', 'soukolí']),
        # TODO: komornější jen na vyžádání (obvykle se moc nestupňuje)
        (Substantivum(lemma='komora'), ['komorní', 'komornější', 'komorně',
                                        'komorník', 'komornický']),
        (Substantivum(lemma='led'), ['náledí', 'lední', 'ledový']),
        (Substantivum(lemma='les'), ['podlesí', 'lesní', 'lesník',
                                     'lesnický']),
        # TODO: nekrátit!
        (Substantivum(lemma='mícha', atributy=dict(g='F')), ['míšní']),
        (Substantivum(lemma='pádlo'), ['pádlař', 'pádlařský']),
        (Substantivum(lemma='město'), ['náměstí', 'předměstí']),
        (Substantivum(lemma='moře'), ['úmoří', 'mořský', 'námořní', 'námořník',
                                      'námořnice', 'námořnický']),
        (Substantivum(lemma='oko'), ['obočí', 'oční']),
        (Substantivum(lemma='Olomouc'), ['olomoucký', 'olomoucky']),
        (Substantivum(lemma='Ostrava'), ['ostravský', 'ostravsky']),
        (Substantivum(lemma='Praha'), ['pražský']),
        (Substantivum(lemma='traktor', vyznamy=dict(cizi=True)), [
            'traktorista', 'traktoristka', 'traktoristický']),  # TODO
        (Substantivum(lemma='rok'), ['roční', 'výročí']),
        (Substantivum(lemma='ruka', atributy=dict(g='F')), [
            'ruční', 'ručník', 'náručí', 'područí']),
        (Substantivum(lemma='sál'), ['předsálí', 'sálový']),
        (Substantivum(lemma='síla', atributy=dict(g='F')), [
            'silný', 'silnice', 'silničář', 'silniční', 'silový']),
        (Substantivum(lemma='skála'), ['úskalí', 'skalní']),
        (Substantivum(lemma='sklep'), ['předsklepí', 'sklepní']),
        (Substantivum(lemma='slovo'), ['přísloví', 'úsloví', 'slovní',
                                       'slovníkář']),  # TODO
        (Substantivum(lemma='stopa'), ['stopař', 'stopařův', 'stopařka',
                                       'stopový', 'stopařský']),
        (Substantivum(lemma='střed'), ['prostředí', 'ústředí', 'středový',
                                       'střední']),
        (Substantivum(lemma='střecha'), ['přístřeší', 'střešní']),
        (Substantivum(lemma='škola'), ['školní', 'školník', 'školský']),
        # řídit → úřad?
        (Substantivum(lemma='úřad'), ['úřední', 'úředník', 'úřednice',
                                      'úřednický']),
        (Substantivum(lemma='věta'), ['souvětí', 'větný']),
        (Substantivum(lemma='voda'), ['vodní', 'povodí', 'podvodnice',
                                      'vodnický']),
        (Substantivum(lemma='vzduch'), ['ovzduší', 'vzdušný',
                                        'provzdušnit']),  # TODO
        # vést → závod?
        (Substantivum(prefix='zá', koren='vod'), ['závodní', 'závodník',
                                                  'závodnice', 'závodnický']),
        # TODO: ztráta měkkosti!
        (Substantivum(lemma='zeď'), ['zedník', 'zednický']),
        (Substantivum(lemma='zem'), ['podzemí', 'území', 'zemní']),
        (Substantivum(lemma='země'), ['zemský']),
        (Adjektivum(lemma='blbý'), ['blbější', 'blbě']),
        (Adjektivum(lemma='bosý'), ['bose', 'naboso']),
        (Adjektivum(lemma='český'), ['česky', 'češtější']),
        (Adjektivum(lemma='dlouhý'), ['delší', 'dloužit', 'prodloužit']),
        (Adjektivum(lemma='dobrý'), ['dobře', 'udobřit', 'udobřený']),
        (Adjektivum(lemma='drahý'), ['dražší', 'dráž', 'dražit',
                                               'vydražit']),  # dráž?
        (Adjektivum(lemma='hebký'), ['hebčí']),  # chceme hebčejší?
        (Adjektivum(lemma='hezký'), ['hezčí']),
        # hlad-i-t → hlad-k-ý?
        (Adjektivum(lemma='hladký'), ['hladší', 'hladce']),
        (Adjektivum(lemma='hloupý'), ['hloupě', 'hloupější', 'hlupák', 'hlupácký']),
        (Adjektivum(lemma='hluchý'), ['hluše', 'hlušší']),
        (Adjektivum(lemma='chrabrý'), ['chrabře', 'chrabřejší']),
        # krát-i-t → krát-k-ý?
        (Adjektivum(lemma='krátký'), ['kratší']),
        (Adjektivum(lemma='mělký'), ['mělčí', 'mělce']),
        (Adjektivum(lemma='mladý'), ['mladší']),
        (Adjektivum(lemma='mrtvý'), ['mrtvě', 'domrtva', 'mrtvice']),
        (Adjektivum(lemma='nahý'), ['donaha']),
        (Adjektivum(lemma='nový'), ['novější', 'obnovit']),
        (Adjektivum(lemma='pěkný'), ['pěkně']),
        (Adjektivum(lemma='plachý'), ['plašší', 'plaše', 'plašit']),
        (Adjektivum(lemma='povědomý'), ['povědomě', 'povědomější']),
        (Adjektivum(lemma='prostý'), ['prostě', 'prostější',
                                                'prostší']),
        (Adjektivum(lemma='přímý'), ['přímější', 'přímit', 'přímený']),
        (Adjektivum(lemma='skoupý'), ['skoupější', 'skoupě']),
        # „posmutnělý“ ať už si vytvoří (m)ajka, to už je flexe a ne derivace
        (Adjektivum(lemma='smutný'), ['smutnější', 'smutnit', 'posmutnět']),
        (Adjektivum(lemma='stálý'), ['stálejší', 'stále']),
        (Adjektivum(lemma='starý'), ['starší', 'staře', 'stařec', 'stařecký']),
        (Adjektivum(lemma='suchý'), ['sušší', 'sušit', 'sušený', 'suše']),
        (Adjektivum(lemma='špatný'), ['horší', 'špatnější']),
        (Adjektivum(lemma='tenký'), ['tenčí', 'tenčit']),
        (Adjektivum(lemma='tvrdý'), ['tvrdě', 'tvrdší', 'tvrďák', 'tvrďácký', 'tvrdit', 'tvrzený']),
        # pláč → plakat → uplakat → uplakaný (zas jen flexe)
        (Verbum(lemma='plakat', atributy=dict(e='A', a='I')), [
            'doplakat', 'oplakat', 'splakat', 'uplakat',
            'vyplakat', 'zaplakat', 'uplakaný', 'uplakanější', 'uplakaně']),
        # úžit → úz-k-ý?
        (Adjektivum(lemma='úzký'), ['užší', 'úžit']),
        (Adjektivum(lemma='veselý'), ['veselejší', 'veselice', 'veselit']),
        (Adjektivum(lemma='vzácný'), ['vzácnější']),
        (Adjektivum(lemma='zlý'), ['horší', 'zlejší']),
        # znamen-í → znamen-it-ý (je -it- téma?)
        (Adjektivum(koren='znamen', sufix='it', koncovka='ý', atributy=dict(
            d='1')), ['znamenitější']),
        # čtený → čtenář

        # číslovky:
        # přidat význam +NUM, ale při derivaci postupovat podle deklinace:
        # čtvrtý → čtvrťák („deadjektivum“)
        # pět → páťák („desubstantivum“)
    ]

    chybejici_odvozeniny = []
    for slovo, ocekavane_odvozeniny in pokusy:
        print(slovo, flush=True)
        slovo.vypsat_odvozeniny(max_hloubka_rekurze=5)

        odvozeniny = set(slovo.lemmata(max_hloubka_rekurze=5))
        chybejici = set(ocekavane_odvozeniny) - odvozeniny
        if chybejici:
            chybejici_odvozeniny.append((slovo.lemma, chybejici))

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
