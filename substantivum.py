from itertools import chain

import slovni_tvar
from transformace_hlasek import alternace1

VOKALY = frozenset('aáeéiíoóuúyýě')


class Substantivum(slovni_tvar.SlovniTvar):
    def __init__(self, rodic=None, lemma='', atributy={}, vyznamy={}):
        super().__init__(rodic, lemma, atributy, vyznamy)

        self.atributy['k'] = '1'
        # u deadjektiv nechceme stupeň fundujícího slova (degree)
        self.atributy.pop('d', None)

    def vytvorit_odvozeniny(self):
        return chain(
            self.konatelska(),
            self.cirkumfixace(),
            self.prefixace(),
        )

    def cirkumfixace(self):
        """
        Derivace substantiv pomocí cirkumfixace
        Jsou-li slova zakončena vokálem, tak tento vokál odpadá.
        V případě zakončení na konsonant dochází k měkčení,
        a to i po předešlém odpadnutí vokálu. Měkčení je shodné
        s fcí alternace1 v transformace_hlasek.py
        Výjimečně dochází k alternacím kvantity vok. (jméno - příjmení)
        To jsem zatím neřešil.

        Substantiva (navíc lemmata) asi nemohou být zakončena všemi vokály,
        ale touto problematikou jsem se dosud nezabýval a uvedl je všechny.

        V praxi jen cyklicky rozšiřuji slovo o jeden z množiny prefixů a o afix.

        K množině prefixů:
        Čerpal jsem z výzkumu - Jazyk a slovník. Vybrané lingvistické studie.
        Dostupné na Google books, str. 171-173.

        Posledních 5 prefixů lze aplikovat jen na uzavřenou množinu slov, zpravidla 1-2.
        Přídávám jejich výčet - zahraničí, prostředí, průčelí, průvodčí,
        scestí, výročí, výsluní.
        Dilema - utvořit výjimky nebo zbytečně přegenerovávat?

        Funkce alternace1 mi neošetří alternaci ch-š, protože
        ji aplikuji až na poslední znak. Nevím, jak to udělat tak,
        aby to fungovalo, nezbylo mi nic jiné než udělat výjimku.
        """

        if self.vyznamy.keys() & frozenset(('vlastnost', 'subst_cirkumfix',
                                            'subst_prefix', 'konatel')):
            return

        prefixy = ['o', 'ob', 'od', 'ná', 'nad', 'po', 'pod', 'před', 'sou',
                   'ú', 'pří', 'roz', 'zá', 'za', 'pro', 'prů', 's', 'vý']

        lemma = self.lemma
        if lemma[-1] in VOKALY:
            lemma = lemma[:-1]

        if lemma.endswith('ch'):
            lemma = lemma[:-2] + 'š'

        konsonant = alternace1(lemma[-1])
        lemma = lemma[:-1] + konsonant
        for prefix in prefixy:
            yield Substantivum(self, prefix + lemma + 'í', vyznamy=dict(
                subst_cirkumfix=True))

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

        sufixy = ['ař', 'ář', 'ista', 'ník']

        lemma = self.lemma
        if lemma[-1] in VOKALY:
            lemma = lemma[:-1]

        if lemma.endswith('c'):
            lemma = lemma[:-1] + 'č'

        for sufix in sufixy:
            yield Substantivum(self, lemma + sufix, vyznamy=dict(konatel=True))
