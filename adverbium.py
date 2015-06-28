import slovni_tvar
from vyjimky import ADVERBIALNI_KOMPARATIVY


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
        return self.stupnovani()

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
