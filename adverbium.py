from itertools import chain

import slovni_tvar


_VYJIMKY_U_KOMPARATIVU = (
    (['dobře'], ['lépe', 'líp']),
    (['zle', 'špatně'], ['hůře', 'hůř']),
    (['brzy'], ['dříve', 'dřív']),
    (['dlouze', 'dlouho'], ['déle']),
    (['vysoce', 'vysoko'], ['výš', 'výše']),
    (['málo'], ['méně', 'míň']),
    (['těžko', 'těžce'], ['tíže', 'tíž']),
    (['snadno', 'snadně'], ['snáze', 'snáz', 'snadněji']),
    (['hluboko', 'hluboce'], ['hloub', 'blouběji']),
    (['široko', 'široce'], ['šíře', 'šíř', 'šířeji']),
    (['úzko', 'úzce'], ['úže', 'úžeji']),
)
VYJIMKY_U_KOMPARATIVU = {}
for pozitivy, komparativy in _VYJIMKY_U_KOMPARATIVU:
    for pozitiv in pozitivy:
        VYJIMKY_U_KOMPARATIVU[pozitiv] = komparativy

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
                 prefix='', sufix='', koncovka=''):
        super().__init__(rodic, atributy, vyznamy, koren, prefix, sufix,
                         koncovka)

        self.atributy['k'] = '6'
        self.stupen = self.atributy.get('d')  # degree, stupeň

    def vytvorit_odvozeniny(self):
        return chain(
            self.prefixace_sufixace(),
            self.stupnovani(),
        )

    # Jiné způsoby derivace než prefixaci a sufixaci neznáme
    def prefixace_sufixace(self):
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
            vyjimky = VYJIMKY_U_KOMPARATIVU.get(self.lemma, [])
            if vyjimky:
                for vyjimka in vyjimky:
                    yield Adverbium(self, dict(d='2'), lemma=vyjimka)
            else:
                yield Adverbium(self, dict(d='2'), sufix='ěji')

        elif self.stupen == '2':
            yield Adverbium(self, dict(d='3'), prefix='nej')
