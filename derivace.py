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
        (Adjektivum(lemma='blbý'), ['blbější', 'blbě', 'zblbnout']),
        (Substantivum(lemma='bok'), ['úbočí', 'boční', 'pobočník']),
        (Adjektivum(lemma='bosý'), ['bose', 'naboso']),
        (Substantivum(lemma='břeh'), ['pobřeží', 'pobřežní', 'nábřeží']),
        (Substantivum(lemma='cesta'), ['scestí', 'rozcestí', 'rozcestník',
                                       'cestovat']),
        (Substantivum(lemma='čelo'), ['průčelí', 'čelní', 'náčelník']),
        (Adjektivum(lemma='český'), ['česky', 'češtější']),
        (Substantivum(lemma='četa'), ['četař', 'četník', 'četnický', 'četařka',
                                      'četnice']),
        # TODO: čtený → čtenář
        (Adjektivum(lemma='dlouhý'), ['delší', 'dloužit', 'prodloužit']),
        (Substantivum(lemma='doba'), ['období', 'dobový']),
        (Adjektivum(lemma='dobrý'), ['dobře', 'udobřit', 'udobřený', 'lepší',
                                     'lépe', 'líp', 'dobrota', 'dobrotivý',
                                     'dobrotivec', 'dobrák']),
        (Adjektivum(lemma='drahý'), ['dražší', 'dráž', 'dražit', 'vydražit',
                                     'zdražit']),  # dráž?
        # do+vést?
        (Substantivum(lemma='důvod'), ['důvodový', 'bezdůvodný',
                                       'bezdůvodně']),  # TODO: oboje
        (Substantivum(lemma='dvůr'), ['nádvoří', 'dvorský']),  # TODO: dvorský
        (Adjektivum(lemma='hebký'), ['hebčí']),  # chceme hebčejší?
        (Adjektivum(lemma='hezký'), ['hezčí']),
        # hlad-i-t → hlad-k-ý?
        (Adjektivum(lemma='hladký'), ['hladší', 'hladce']),
        (Substantivum(lemma='hlava', atributy=dict(g='F')), [
            'záhlaví', 'náhlavní', 'pohlaví', 'pohlavní', 'úhlavní',
            'hlavice']),
        (Adjektivum(lemma='hloupý'), ['hloupě', 'hloupější', 'hlupák',
                                      'hlupácký', 'prohloupit']),
        (Adjektivum(lemma='hluchý'), ['hluše', 'hlušší', 'ohlušit',
                                      'zahlušit']),
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
            'zahraničí', 'hranit']),
        (Substantivum(lemma='hvězda', atributy=dict(g='F')), [
            'hvězdář', 'souhvězdí', 'hvězdný', 'hvězdice', 'hvězdářský']),
        (Adjektivum(lemma='chrabrý'), ['chrabře', 'chrabřejší']),
        (Substantivum(lemma='jeskyně'), ['jeskynní', 'jeskyňář']),
        (Substantivum(lemma='kolo'), ['kolař', 'soukolí', 'kolovat']),
        # TODO: komornější jen na vyžádání (obvykle se moc nestupňuje)
        (Substantivum(lemma='komora'), ['komorní', 'komornější', 'komorně',
                                        'komorník', 'komornický']),
        # krát-i-t → krát-k-ý?
        (Adjektivum(lemma='krátký'), ['kratší', 'zkrátit']),
        # krot-i-t → krot-k-ý
        (Substantivum(lemma='led'), ['náledí', 'lední', 'ledový', 'ledovat']),
        (Substantivum(lemma='les'), ['podlesí', 'lesní', 'lesník',
                                     'lesnický']),
        (Adjektivum(lemma='malý'), ['menší']),
        (Adjektivum(lemma='mělký'), ['mělčí', 'mělce']),
        (Substantivum(lemma='město'), ['náměstí', 'předměstí']),
        # TODO: nekrátit!
        (Substantivum(lemma='mícha', atributy=dict(g='F')), ['míšní']),
        (Adjektivum(lemma='mladý'), ['mladší', 'omladit']),
        (Substantivum(lemma='moře'), ['úmoří', 'mořský', 'námořní', 'námořník',
                                      'námořnice', 'námořnický']),
        (Adjektivum(lemma='mrtvý'), ['mrtvě', 'domrtva', 'mrtvice',
                                     'umrtvit']),
        (Adjektivum(lemma='nahý'), ['donaha']),
        (Adjektivum(lemma='nový'), ['novější', 'obnovit']),
        (Substantivum(lemma='oko'), ['obočí', 'oční']),
        (Substantivum(lemma='Olomouc'), ['olomoucký', 'olomoucky']),
        (Substantivum(lemma='Ostrava'), ['ostravský', 'ostravsky']),
        (Substantivum(lemma='pádlo'), ['pádlař', 'pádlařský', 'pádlovat']),
        (Adjektivum(lemma='pěkný'), ['pěkně', 'hezčí']),
        (Adjektivum(lemma='plachý'), ['plašší', 'plaše', 'plašit']),
        # pláč → plakat → uplakat → uplakaný (zas jen flexe)
        (Verbum(lemma='plakat', atributy=dict(e='A', a='I')), [
            'doplakat', 'oplakat', 'splakat', 'uplakat',
            'vyplakat', 'zaplakat', 'uplakaný', 'uplakanější', 'uplakaně']),
        (Adjektivum(lemma='povědomý'), ['povědomě', 'povědomější']),
        (Substantivum(lemma='Praha'), ['pražský']),
        (Adjektivum(lemma='prostý'), ['prostě', 'prostější',
                                                'prostší']),
        (Adjektivum(lemma='přímý'), ['přímější', 'přímit', 'přímený']),
        (Substantivum(lemma='rok'), ['roční', 'výročí', 'rokovat']),
        (Substantivum(lemma='ruka', atributy=dict(g='F')), [
            'ruční', 'ručník', 'náručí', 'područí', 'rukovat']),
        (Substantivum(lemma='sál'), ['předsálí', 'sálový']),
        (Substantivum(lemma='síla', atributy=dict(g='F')), [
            'silný', 'silnice', 'silničář', 'silniční', 'silový']),
        (Substantivum(lemma='skála'), ['úskalí', 'skalní']),
        (Substantivum(lemma='sklep'), ['předsklepí', 'sklepní']),
        (Adjektivum(lemma='skoupý'), ['skoupější', 'skoupě']),
        (Substantivum(lemma='slovo'), ['přísloví', 'úsloví', 'slovní',
                                       'slovníkář']),  # TODO
        # „posmutnělý“ ať už si vytvoří (m)ajka, to už je flexe a ne derivace
        (Adjektivum(lemma='smutný'), ['smutnější', 'smutnit', 'posmutnět']),
        (Adjektivum(lemma='stálý'), ['stálejší', 'stále']),
        (Adjektivum(lemma='starý'), ['starší', 'staře', 'stařec', 'stařecký',
                                     'stařešina']),
        (Substantivum(lemma='stopa'), ['stopař', 'stopařův', 'stopařka',
                                       'stopový', 'stopařský', 'stopovat']),
        (Substantivum(lemma='střed'), ['prostředí', 'ústředí', 'středový',
                                       'střední']),
        (Substantivum(lemma='střecha'), ['přístřeší', 'střešní']),
        (Adjektivum(lemma='suchý'), ['sušší', 'sušit', 'sušený', 'suše',
                                     'dosušit', 'usušit', 'vysušit']),
        # šíře, šířit
        (Adjektivum(lemma='široký'), ['širší']),
        (Substantivum(lemma='škola'), ['školní', 'školník', 'školský']),
        (Adjektivum(lemma='špatný'), ['horší', 'špatnější']),
        (Adjektivum(lemma='tenký'), ['tenčí', 'tenčit', 'ztenčit']),
        (Substantivum(lemma='traktor', vyznamy=dict(cizi=True)), [
            'traktorista', 'traktoristka', 'traktoristický']),  # TODO
        (Adjektivum(lemma='tvrdý'), ['tvrdě', 'tvrdší', 'tvrďák', 'tvrďácký',
                                     'tvrdit', 'tvrzený']),
        # řídit → úřad?
        (Substantivum(lemma='úřad'), ['úřední', 'úředník', 'úřednice',
                                      'úřednický', 'úřadovat']),
        # úžit → úz-k-ý?
        (Adjektivum(lemma='úzký'), ['užší', 'úžit', 'zúžit']),
        (Adjektivum(lemma='velký'), ['větší']),
        (Adjektivum(lemma='veliký'), ['větší', 'velikost', 'velikán',
                                      'zveličit']),
        (Adjektivum(lemma='veselý'), ['veselejší', 'veselice', 'veselit',
                                      'rozveselit', 'veselka']),
        (Substantivum(lemma='věta'), ['souvětí', 'větný']),
        (Substantivum(lemma='voda'), ['vodní', 'povodí', 'podvodnice',
                                      'vodnický']),
        (Adjektivum(lemma='vzácný'), ['vzácnější']),
        (Substantivum(lemma='vzduch'), ['ovzduší', 'vzdušný',
                                        'provzdušnit']),
        # vést → závod?
        (Substantivum(prefix='zá', koren='vod'), ['závodní', 'závodník',
                                                  'závodnice', 'závodnický']),
        # TODO: ztráta měkkosti!
        (Substantivum(lemma='zeď'), ['zedník', 'zednický']),
        (Substantivum(lemma='zem'), ['podzemí', 'území', 'zemní']),
        (Substantivum(lemma='země'), ['zemský', 'zázemí']),
        (Adjektivum(lemma='zlý'), ['horší', 'zlejší', 'zle', 'hůře', 'hůř']),
        # znamen-í → znamen-it-ý (je -it- téma?)
        (Adjektivum(koren='znamen', sufix='it', koncovka='ý', atributy=dict(
            d='1')), ['znamenitější']),

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
