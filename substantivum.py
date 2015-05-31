from itertools import chain

import adjektivum
import slovni_tvar
from upravy import palatalizace

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
        # u deadjektiv CHCEME stupeň fundujícího slova (degree), aby už se
        # nederivovalo dál
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

        if self.lemma[0].isupper() or self.vyznamy.keys() & frozenset((
            'vlastnost', 'subst_cirkumfix', 'subst_prefix', 'konatel')):
            return  # vlastní jména se taky neřeší

        vyjimka = VZACNA_CIRKUMFIXACE.get(self.lemma)
        if vyjimka:
            yield Substantivum(self, vyjimka, vyznamy=dict(
                subst_cirkumfix=True))

        prefixy = ['o', 'ob', 'od', 'ná', 'nad', 'po', 'pod', 'před', 'sou',
                   'ú', 'pří', 'roz', 'zá']

        for prefix in prefixy:
            yield Substantivum(self, palatalizace(prefix + self.kmen + 'í'),
                               vyznamy=dict(subst_cirkumfix=True))

        # TODO: slova typu „bezdůvodný“ se podle mě tvoří připojením předložky
        # bez důvodu → bez-důvod-n-ý

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

        if self.vyznamy.keys() & frozenset(('vlastnost', 'subst_cirkumfix',
                                            'subst_prefix', 'konatel')):
            return

        sufixy = (
            # nejspíš jde o dva alomorfy – ale na čem závisí jejich distribuce?
            'ař',
            'ář',

            'ista',

            # zřejmě měkčící, podobně jako adjektivní sufix -n- (možná je tento
            # jen -k- a váže se naopak na adjektivum? ale podle četníka spíš ne)
            'ník',
            # třeba u slovo → slovník jde o slovotvornou homonymii, ale to by
            # šlo omezit podmínkou, že dané substantivum má příznak životnosti
        )

        lemma = self.lemma
        if lemma[-1] in VOKALY:
            lemma = lemma[:-1]

        if lemma.endswith('c'):
            lemma = lemma[:-1] + 'č'

        for sufix in sufixy:
            yield Substantivum(self, lemma + sufix, vyznamy=dict(konatel=True))

    def adjektivum(self):
        """
        Kdy se používá měkký vzor a kdy tvrdý?

        Je sufix -n- regresivně měkčící, nebo je to (třeba) v případě vzduch+ný
        potence kořene, nějaké historické ś umlčené substantivními koncovkami?

        TODO: s výjimkou komorní → komornější se odvozená adjektiva moc
        nestupňují – takže přidat volbu programu, aby na vyžádání stupňoval,
        i když _nebude uveden_ stupeň.
        """
        if self.atributy.get('d'):
            return  # substantivum odvozené od adjektiva (ale: tvrdostní)

        kmen = self.kmen.lower()

        if kmen.endswith('ík'):  # četník → četnický (TODO: krátit)
            yield adjektivum.Adjektivum(self, palatalizace(kmen[:-1] + "'ký"))
        elif kmen.endswith('c'):  # Olomouc → olomoucký
            yield adjektivum.Adjektivum(self, palatalizace(kmen + "ký"))
        else:  # hora → horský, cestář → cestářský
            yield adjektivum.Adjektivum(self, palatalizace(kmen + "'ský"))

        # města (místa) by mohla mít příznak, který by tuhle derivaci blokoval
        # prozatím postačí je neřešit díky velkému písmenu
        if 'konatel' not in self.vyznamy and not self.kmen[0].isupper():
            # TODO: v kořeni se musí krátit
            yield adjektivum.Adjektivum(self, palatalizace(kmen + "'ní"))
            yield adjektivum.Adjektivum(self, palatalizace(kmen + "'ný"))
