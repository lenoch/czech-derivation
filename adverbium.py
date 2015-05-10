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
    def __init__(self, rodic=None, lemma='', atributy={}, vyznamy={}):
        super().__init__(rodic, lemma, atributy, vyznamy)

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
            yield Adverbium(self, 'na' + self.lemma, vyznamy={'prefix': 'na'})

        for adjektivni, adverbialni in zakonceni:
            if self.lemma.endswith(adverbialni):
                delka_zakonceni = len(adverbialni)
                lemma = self.lemma[:-delka_zakonceni] + adjektivni[:-1]
                yield Adverbium(self, 'do' + lemma + 'a')
                prefix = 'ze' if lemma[0] in ('s', 'z') else 'z'
                yield Adverbium(self, prefix + lemma + 'a')
                yield Adverbium(self, 'na' + lemma + 'o',
                                vyznamy={'prefix': 'na'})

    def stupnovani(self):
        if self.stupen == '1':
            vyjimky = VYJIMKY_U_KOMPARATIVU.get(self.lemma, [])
            if vyjimky:
                for vyjimka in vyjimky:
                    yield Adverbium(self, vyjimka, dict(d='2'))
            else:
                if self.lemma.endswith('ce'):
                    yield Adverbium(self, self.lemma[:-2] + 'čeji',
                                    dict(d='2'))
                elif self.lemma.endswith('cky'):
                    yield Adverbium(self, self.lemma[:-3] + 'čtěji',
                                    dict(d='2'))
                elif self.lemma.endswith('sky'):
                    yield Adverbium(self, self.lemma[:-3] + 'štěji',
                                    dict(d='2'))
                elif self.lemma[-1] in ('e', 'ě'):
                    yield Adverbium(self, self.lemma + 'ji', dict(d='2'))

        elif self.stupen == '2':
            yield Adverbium(self, 'nej' + self.lemma, dict(d='3'))
