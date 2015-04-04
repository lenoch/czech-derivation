from itertools import chain
# import logging

import adverbium
import slovni_tvar
import substantivum
from upravy import palatalizace


class Adjektivum(slovni_tvar.SlovniTvar):
    def __init__(self, rodic=None, lemma='', atributy={}, vyznamy={}):
        super().__init__(rodic, lemma, atributy, vyznamy)

        self.atributy['k'] = '2'
        self.stupen = self.atributy.get('d')  # degree, stupeň

    def vytvorit_odvozeniny(self):
        return chain(
            self.stupnovani(),
            self.mladost(),
            self.adverbializace(),
        )

    def stupnovani(self):
        if self.stupen == '1':
            if self.lemma.endswith('ý'):
                komparativ = Adjektivum(
                    self, palatalizace(self.lemma[:-1] + 'ější'), dict(d='2'))
                yield komparativ

                # superlativ se dá vygenerovat rekurzí
                # for superlativ in komparativ.stupnovani():
                #     yield superlativ
        elif self.stupen == '2':  # asi nemá smysl vytvářet nejnejlepšejší
            yield Adjektivum(self, 'nej' + self.lemma, dict(d='3'))

    def mladost(self):
        if self.stupen == '1' and self.lemma.endswith('ý'):
            # derivát je femininum (g = genus, jmenný rod)
            yield substantivum.Substantivum(
                self, self.lemma[:-1] + 'ost', dict(g='F'))

    def adverbializace(self):
        if self.stupen == '1':
            yield adverbium.Adverbium(self, self.lemma[:-1] + 'o')

            if self.lemma[-3:] in ('cký', 'ský'):
                yield adverbium.Adverbium(self, self.lemma[:-1] + 'y')
            elif self.lemma[-1] in ('í', 'ý'):
                kmen = self.lemma[:-1]
                yield adverbium.Adverbium(self, palatalizace(kmen + 'ě'))
