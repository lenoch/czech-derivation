from itertools import chain

import adjektivum
import slovni_tvar
from upravy import palatalizovat, zkratit

VOKALY = frozenset('aáeéiíoóuúyýě')

# Posledních 5 prefixů lze aplikovat jen na uzavřenou množinu slov,
# zpravidla 1-2.
# Přídávám jejich výčet - zahraničí, prostředí, průčelí, průvodčí,
# scestí, výročí, výsluní.
# Dilema - utvořit výjimky nebo zbytečně přegenerovávat?
#
# Ondra: Radši výjimky, ale ty by měly být podložené korpusem, tedy
# [lemma="(za|pro|prů|s|vý).+í" & tag="k1.*"]
VZACNA_CIRKUMFIXACE = {
    'čelo': 'průčelí',  # vážně?
    'hranice': 'zahraničí',
    'cesta': 'scestí',
    'rok': 'výročí',
    # vý-slun-í (odtrhává se tedy ze slunce deminutivní sufix -c-?)
    'střed': 'prostředí',  # tak?
    # prů-vodčí?
}


class Substantivum(slovni_tvar.SlovniTvar):
    def __init__(self, rodic=None, lemma='', atributy={}, vyznamy={}):
        super().__init__(rodic, lemma, atributy, vyznamy)

        self.atributy['k'] = '1'
        self.rod = self.atributy.get('g')
        # u deadjektiv nechceme stupeň fundujícího slova (degree)
        # další derivace se zastavuje jinými příznaky
        self.atributy.pop('d', None)
        self.odtrhnout_koncovku()

    def odtrhnout_koncovku(self):
        if self.lemma[-1] in VOKALY:
            self.kmen = self.lemma[:-1]
            self.koncovka = self.lemma[-1]
        else:
            self.kmen = self.lemma
            self.koncovka = ''

    def vytvorit_odvozeniny(self):
        return chain(
            self.konatelska(),
            self.cirkumfixace(),
            self.prefixace(),
            self.adjektivum(),
            self.posesivum(),
            self.mechovy(),
            self.autorka(),
            # TODO: hvězda → hvězdice
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
                    self.vyznamy.get('foreign')):
            return  # vlastní jména se taky neřeší

        vyjimka = VZACNA_CIRKUMFIXACE.get(self.lemma)
        if vyjimka:
            yield Substantivum(self, vyjimka, vyznamy=dict(
                subst_cirkumfix=True))

        prefixy = ['o', 'ob', 'od', 'ná', 'nad', 'po', 'pod', 'před', 'sou',
                   'ú', 'pří', 'roz', 'zá']

        for prefix in prefixy:
            yield Substantivum(self, palatalizovat(prefix + zkratit(self.kmen)
                               + 'í'), vyznamy=dict(subst_cirkumfix=True))

        # TODO: v podhůří se dlouží, v podhoubí se nemá krátit („podhubí“)

        # TODO: slova typu „bezdůvodný“ se podle mě tvoří připojením předložky
        # bez důvodu → bez-důvod-n-ý
        # TODO: vzniká námořní (od „na moři“) přímo, bez „námoří“?

    def prefixace(self):
        """
        Vytváření substantivních derivátů pomocí množiny prefixů
        Vycházím ze záznamu na Wikipedii - "Seznam českých předpon"
        Vybral jsem předpony, kterými lze teoreticky modifikovat příslušná substantiva
        """

        if self.vyznamy.keys() & frozenset(('subst_cirkumfix',
                                            'subst_prefix')):
            return

        prefixy = ['polo', 'pra', 'pa', 'skoro', 'sotva', 'mezi', 'ne',
                   'pseudo', 'super', 'maxi', 'mini', 'giga', 'ultra', 'ex',
                   'hyper', 'neo', 'retro']

        for prefix in prefixy:
            yield Substantivum(self, prefix + self.lemma, vyznamy=dict(
                subst_prefix=True))

    def konatelska(self):
        """
        Vytváření konatelských substantiv
        V případě zakončení na vokál jej odseknu
        K alternacím s výjimkou c -> č nedochází
        Nakonec připojím jeden z množiny konatelských sufixů
        Zřídka funkce utvoří více než jedno v praxi používané slovo
        Tzn. vysoká míra nadgenerování
        """

        if self.vyznamy.get('anim') or self.vyznamy.keys() & frozenset((
                'vlastnost', 'subst_cirkumfix', 'subst_prefix')):
            return

        sufixy = (
            # nejspíš jde o dva alomorfy – ale na čem závisí jejich distribuce?
            'ař',
            'ář',
        )

        lemma = self.lemma
        if lemma[-1] in VOKALY:
            lemma = lemma[:-1]

        if lemma.endswith('c'):
            lemma = lemma[:-1] + 'č'

        if self.vyznamy.get('foreign'):
            yield Substantivum(self, lemma + 'ista', dict(g='M'),
                               dict(anim=True))
        for sufix in sufixy:
            yield Substantivum(self, lemma + sufix, dict(g='M'),
                               dict(anim=True))

    def adjektivum(self):
        """
        Kdy se používá měkký vzor a kdy tvrdý?

        Je sufix -n- regresivně měkčící, nebo je to (třeba) v případě vzduch+ný
        potence kořene, nějaké historické ś umlčené substantivními koncovkami?

        TODO: krátit se musí asi jen v kořeni, jak ukazuje zá-vod-n-í a
        ná-moř-n-í

        TODO: s výjimkou komorní → komornější se odvozená adjektiva moc
        nestupňují – takže přidat volbu programu, aby na vyžádání stupňoval,
        i když _nebude uveden_ stupeň.
        """
        if self.vyznamy.get('vlastnost'):
            return  # substantivum odvozené od adjektiva (ale: tvrdostní)
        if self.rod == 'F' and self.vyznamy.get('moce'):
            return  # přechýlení, zatím k-ový sufix, ale jsou další

        kmen = self.kmen.lower()

        if kmen.endswith('ík'):  # četník → četnický
            yield adjektivum.Adjektivum(self, palatalizovat(kmen[:-2] +
                                        "ický"))
        elif kmen.endswith('c'):  # Olomouc → olomoucký
            yield adjektivum.Adjektivum(self, palatalizovat(kmen + "ký"))
        else:  # hora → horský, cestář → cestářský
            yield adjektivum.Adjektivum(self, palatalizovat(kmen + "'ský"))

        # města (místa) by mohla mít příznak, který by tuhle derivaci blokoval
        # prozatím postačí je neřešit díky velkému písmenu
        if not self.vyznamy.get('anim') and not self.kmen[0].isupper():
            yield adjektivum.Adjektivum(self, palatalizovat(zkratit(kmen) +
                                        "'ní"))
            yield adjektivum.Adjektivum(self, palatalizovat(zkratit(kmen) +
                                        "'ný"))

    def posesivum(self):
        if self.vyznamy.get('anim'):
            if self.rod == 'M':
                yield adjektivum.Adjektivum(self, self.kmen + 'ův', {},
                                            dict(posesivum=True))
            elif self.rod == 'F':
                yield adjektivum.Adjektivum(self, palatalizovat(
                    self.kmen + 'in'), {}, dict(posesivum=True))

    def mechovy(self):
        # sálový ale silový – je to kvůli „cizosti“ slova sál?
        if not self.vyznamy.get('anim') and not self.vyznamy.get('vlastnost'):
            yield adjektivum.Adjektivum(self, self.kmen + 'ový', dict(g='M'))

    def autorka(self):
        # přechylování, moce
        if self.rod != 'M':
            return
        if self.kmen.endswith('ík'):  # úředník → úřednice (ten samý sufix)
            yield Substantivum(self, self.kmen[:-2] + 'ice', dict(g='F'),
                               dict(moce=True))
        else:
            yield Substantivum(self, self.kmen + 'ka', dict(g='F'),
                               dict(moce=True))
