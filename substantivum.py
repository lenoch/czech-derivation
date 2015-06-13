from itertools import chain

import adjektivum
import slovni_tvar
from upravy import zkratit
from vyjimky import ZAHRANICI

VOKALY = frozenset('aáeéiíoóuúyýě')

class Substantivum(slovni_tvar.SlovniTvar):
    def __init__(self, rodic=None, atributy={}, vyznamy={}, lemma='', koren='',
                 prefix='', sufix='', koncovka='', nahradit_sufix=None):
        if lemma:
            koren, koncovka = self.odtrhnout_koncovku(lemma)

        super().__init__(rodic, atributy, vyznamy, koren, prefix, sufix,
                         koncovka, nahradit_sufix)

        self.atributy['k'] = '1'  # kind, slovní druh, part of speech (POS)
        self.rod = self.atributy.get('g')
        # u deadjektiv nechceme stupeň fundujícího slova (degree)
        # další derivace se zastavuje jinými příznaky
        self.atributy.pop('d', None)

    @staticmethod
    def odtrhnout_koncovku(lemma):
        # TODO: co další případy?  nejde jen tak odtrhnout -ě, musí se ponechat
        # měkčení (Ruzyně → ruzyňský, jeskyně → jeskyňář)
        if lemma.endswith('ně'):
            return lemma[:-2] + 'ň', 'e'
        elif lemma[-1] in VOKALY:
            return lemma[:-1], lemma[-1]
        else:
            return lemma, ''

    def vytvorit_odvozeniny(self):
        return chain(
            self.konatelska(),
            self.cirkumfixace(),
            self.prefixace(),
            self.adjektivum(),
            self.posesivum(),
            self.mechovy(),
            self.autorka(),
            self.hvezdice(),
            # TODO: deminuce
        )

    def cirkumfixace(self):
        """
        Derivace substantiv pomocí cirkumfixace

        Ke kmeni (tzn. lemmatu bez případné vokalické koncovky) se připojuje
        sufix -'í. Ten je měkčící, mění dokonce c na č (pohraničí).

        Výjimečně dochází k alternacím kvantity vok. (jméno - příjmení)
        To jsem zatím neřešil.

        Substantiva (navíc lemmata) asi nemohou být zakončena všemi vokály,
        ale touto problematikou jsem se dosud nezabýval a uvedl je všechny.

        K množině prefixů:
        Čerpal jsem z výzkumu - Jazyk a slovník. Vybrané lingvistické studie.
        Dostupné na Google books, str. 171-173.
        """

        if self.lemma[0].isupper() or self.vyznamy.get('anim') or (
            self.vyznamy.keys() & frozenset((
                'vlastnost', 'subst_cirkumfix', 'subst_prefix'))) or (
                    self.vyznamy.get('cizi')):
            return  # vlastní jména se taky neřeší

        prefixy = ['o', 'ob', 'od', 'ná', 'nad', 'po', 'pod', 'před', 'sou',
                   'ú', 'pří', 'roz', 'zá']

        vyjimka = ZAHRANICI.get(self.lemma)
        if vyjimka:
            prefixy.insert(0, vyjimka)

        for prefix in prefixy:
            yield Substantivum(self, prefix=prefix, koren=zkratit(self.koren),
                               koncovka='í',
                               vyznamy=dict(subst_cirkumfix=True))

        # TODO: v podhůří se dlouží (v pohoří ale ne, takže nepravidelnost?)
        # TODO: v podhoubí se nemá krátit („podhubí“)

        # TODO: slova typu „bezdůvodný“ se podle mě tvoří připojením předložky
        # bez důvodu → bez-důvod-n-ý
        # TODO: vzniká námořní (od „na moři“) přímo, bez „námoří“?

    def prefixace(self):
        """
        Vytváření substantivních derivátů pomocí množiny prefixů
        Vycházím ze záznamu na Wikipedii - "Seznam českých předpon"
        Vybral jsem předpony, kterými lze teoreticky modifikovat příslušná substantiva
        """
        if self.prefixy:
            return

        prefixy = ['polo', 'pra', 'pa', 'skoro', 'sotva', 'mezi', 'ne',
                   'pseudo', 'super', 'maxi', 'mini', 'giga', 'ultra', 'ex',
                   'hyper', 'neo', 'retro']

        for prefix in prefixy:
            yield Substantivum(self, vyznamy=dict(subst_prefix=True),
                               prefix=prefix)

    def konatelska(self):
        """
        Vytváření konatelských substantiv (z neživotných jmen)

        -ař/-ář je produktivní,
        -ista jde zřejmě jen ke slovům cizího původu
        -n-ík se dělá u adjektiv

        Na sufix -ic- se připojuje sufix -ář a -ic- se měkčí na -ič-:
        sil-n-ic-e → sil-n-ič-ář, želez-n-ic-e → želez-n-ič-ář,
        hran-ic-e → hran-ič-ář, kop-an-ic-e → kop-an-ič-ář, páleničář

        Výjimečně se měkčí ještě:
        (čep? → čepec) čepice → čepičář, oko → očař, krk → krčař, ucho → ušař
        raritka: lžíce → Lžičař, ruka/ruce → ručař
        většinou SYN2010, [tag="N.*" & lemma=".*č[aá]ř"] a podobné dotazy

        TODO:
        mást → z-mást → z-mat-ek → z-mat-k-ář
        vy-sad-i-t → vý-sad-ek → vý-sad-k-ář
        výjimky: kůň → koňař (krácení – i když jen z pohledu nominativu koně)
        """
        # s výjimkou hodnostáře a rovnostáře se už sufixu -ost- nederivuje
        # (přinejmenším pomocí -ař/-ář)
        if self.vyznamy.get('anim') or self.kmen.endswith('ost'):
            return

        # proti přegenerovávání  TODO: nezneužívat (tolik) příznaky
        if self.vyznamy.keys() & frozenset(('subst_cirkumfix',
                                            'subst_prefix')):
            return

        if self.kmen.endswith('ic') and self.rod == 'F':
            yield Substantivum(self, dict(g='M'), dict(anim=True),
                               nahradit_sufix='ič', sufix='ář')

        if self.vyznamy.get('cizi'):
            yield Substantivum(self, dict(g='M'), dict(anim=True),
                               sufix='_ist', koncovka='a')

        # nejspíš jde o dva alomorfy – ale na čem závisí jejich distribuce?
        # -ař je asi častější, -ář je asi většinou u delších (víceslabičných)
        # slov
        for sufix in ('ář', 'ař'):
            yield Substantivum(self, dict(g='M'), dict(anim=True), sufix=sufix)

    def adjektivum(self):
        """
        Kdy se používá měkký vzor a kdy tvrdý?

        Je sufix -n- regresivně měkčící, nebo je to (třeba) v případě vzduch+ný
        potence kořene, nějaké historické ś umlčené substantivními koncovkami?

        Krátí se (jen) v kořeni, jak ukazuje zá-vod-n-í a ná-moř-n-í.

        TODO: s výjimkou komorní → komornější se odvozená adjektiva moc
        nestupňují – takže přidat volbu programu, aby na vyžádání stupňoval,
        i když _nebude uveden_ stupeň.
        """
        if self.vyznamy.get('vlastnost'):
            return  # substantivum odvozené od adjektiva (ale: tvrdostní)
        if self.rod == 'F' and self.vyznamy.get('moce'):
            return  # přechýlení, zatím k-ový sufix, ale jsou další

        koren = self.koren.lower()

        if self.kmen.endswith('ík'):  # četník → četnický
            yield adjektivum.Adjektivum(self, dict(d='N'), koren=koren,
                                        nahradit_sufix='ic', sufix='k',
                                        koncovka='ý')
        elif self.kmen.endswith('c'):  # Olomouc → olomoucký
            yield adjektivum.Adjektivum(self, dict(d='N'), koren=koren,
                                        sufix='k', koncovka='ý')
        else:  # hora → horský, cestář → cestářský, Praha → pražský
            # měkčení?  bůh → božský, Valach → valašský, loni → loňský,
            # Ostroh → ostrožský
            yield adjektivum.Adjektivum(self, dict(d='N'), koren=koren,
                                        sufix='sk', koncovka='ý')

        # města (místa) by mohla mít příznak, který by tuhle derivaci blokoval
        # prozatím postačí je neřešit díky velkému písmenu
        if not self.vyznamy.get('anim') and not self.kmen[0].isupper():
            sufix = "'n" if self.kmen[-1] in ('chk') else 'n'  # bok → boční
            for koncovka in ('í', 'ý'):
                yield adjektivum.Adjektivum(self, dict(d='N'), koren=zkratit(
                    self.koren), sufix=sufix, koncovka=koncovka)

    def posesivum(self):
        if self.vyznamy.get('anim'):
            if self.rod == 'M':
                yield adjektivum.Adjektivum(self, dict(d='N'),
                                            dict(posesivum=True), sufix='ův')
            elif self.rod == 'F':
                yield adjektivum.Adjektivum(self, dict(d='N'),
                                            dict(posesivum=True), sufix="'in")

    def mechovy(self):
        # sálový ale silový – je to kvůli „cizosti“ slova sál?
        if not self.vyznamy.get('anim') and not self.vyznamy.get('vlastnost'):
            yield adjektivum.Adjektivum(self, dict(d='N', g='M'), sufix='ov',
                                        koncovka='ý')

    def autorka(self):
        # přechylování, moce
        if self.rod != 'M':
            return
        if self.kmen.endswith('ík'):  # úředník → úřednice (ten samý sufix)
            yield Substantivum(self, dict(g='F'), dict(moce=True),
                               nahradit_sufix='ic', koncovka='e')
        else:
            yield Substantivum(self, dict(g='F'), dict(moce=True), sufix='k',
                               koncovka='a')

    def hvezdice(self):
        """
        hvězd-a > hvězd-ic-e (asi od neživotných feminin)
        """
        if self.sufixy and self.sufixy[-1] in ('ost', 'ic'):
            return

        if self.rod == 'F' and not self.vyznamy.get('anim'):
            yield Substantivum(self, sufix='ic', koncovka='e')
