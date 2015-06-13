from itertools import chain

import slovni_tvar
from vyjimky import ADVERBIALNI_KOMPARATIVY

zakonceni = [  # TODO: dočasné
    ('dý', 'dě'),
    ('rý', 'ře'),
    ('bý', 'bě'),
    ('vý', 'vě'),
    ('mý', 'mě'),
    ('sý', 'se'),
    ('pý', 'pě'),
    ('tý', 'tě'),
    ('lý', 'le'),
    ('ný', 'ně'),
    ('ní', 'ně'),
    ('chý', 'še'),
    ('hý', 'ze'),
    ('ský', 'sky'),
    ('cký', 'cky'),
    ('ký', 'ce'),
]


class Adverbium(slovni_tvar.SlovniTvar):
    def __init__(self, rodic=None, atributy={}, vyznamy={}, lemma='', koren='',
                 prefix='', sufix='', koncovka=None):
        if lemma:
            koren, koncovka = self.odtrhnout_koncovku(lemma)

        super().__init__(rodic, atributy, vyznamy, koren, prefix, sufix,
                         koncovka)

        self.atributy['k'] = '6'  # kind, slovní druh, part of speech (POS)
        self.stupen = self.atributy.get('d')  # degree, stupeň

    @staticmethod
    def odtrhnout_koncovku(lemma):
        # jen kvůli výjimkám
        if lemma[-1] in ('e', 'ě'):
            return lemma[:-1], lemma[-1]
        elif lemma[-3:-1] in ('eji', 'ěji'):
            return lemma[:-3], lemma[-3:-1]
        else:
            return lemma, ''

    def vytvorit_odvozeniny(self):
        return chain(
            self.stupnovani(),
            self.prefixace_sufixace(),
        )

    # Jiné způsoby derivace než prefixaci a sufixaci neznáme
    def prefixace_sufixace(self):
        if self.prefixy:
            return  # nebudeme na sebe lepit víc prefixů, než je potřeba

        if self.lemma.endswith('o') and self.vyznamy.get('prefix') != 'na':
            yield Adverbium(self, vyznamy={'prefix': 'na'}, prefix='na')

        for adjektivni, adverbialni in zakonceni:
            if self.lemma.endswith(adverbialni):
                delka_zakonceni = len(adverbialni)
                lemma = self.lemma[:-delka_zakonceni] + adjektivni[:-1]
                yield Adverbium(self, prefix='do', koncovka='a')
                prefix = 'ze' if lemma[0] in ('s', 'z') else 'z'
                yield Adverbium(self, prefix=prefix, koncovka='a')
                yield Adverbium(self, prefix='na', koncovka='o',
                                vyznamy={'prefix': 'na'})

    def stupnovani(self):
        if self.stupen == '1':
            vyjimky = ADVERBIALNI_KOMPARATIVY.get(self.lemma, [])
            if vyjimky:
                for vyjimka in vyjimky:
                    yield Adverbium(self, dict(d='2'), lemma=vyjimka)
            else:
                yield Adverbium(self, dict(d='2'), sufix='ěji')

        elif self.stupen == '2':
            yield Adverbium(self, dict(d='3'), prefix='nej')
