from itertools import chain

import adjektivum
import slovni_tvar

class Verbum(slovni_tvar.SlovniTvar):
    PREFIXY = ('do', 'na', 'o', 's', 'u', 'vy', 'za')
    TEMATA = ('a', 'e', 'i', 'nou')

    def __init__(self, rodic=None, lemma='', atributy={}, vyznamy={}):
        super().__init__(rodic, lemma, atributy, vyznamy)

        self.atributy['k'] = '5'
        self.neg = self.atributy.get('e')
        self.aspekt = self.atributy.get('a')

        modus = self.atributy.get('m')
        if modus is not None and modus != 'F':
            raise ValueError('očekává se infinitiv')
        if not self.lemma.endswith('t'):
            raise ValueError('očekává se infinitiv')

        self.zjistit_tema()

    def zjistit_tema(self):
        self.kmen = self.lemma[:-1]  # pokud pomineme prefixy, samozřejmě
        for tema in self.TEMATA:
            if self.kmen.endswith(tema):
                self.tema = tema
                break
        else:
            raise ValueError('neznámý tematický sufix')

    def vytvorit_odvozeniny(self):
        return chain(
            self.negace(),
            self.prefixace(),
            self.adjektivizace(),
        )

    def negace(self):
        if self.neg != 'N':
            yield Verbum(self, 'ne' + self.lemma, dict(e='N'))

    def prefixace(self):
        if self.neg != 'N' and self.aspekt == 'I':
            for prefix in self.PREFIXY:
                yield Verbum(self, prefix + self.lemma, dict(a='P'))

    def adjektivizace(self):
        # přes slovnědruhově sporné n-ové participium
        yield adjektivum.Adjektivum(self, self.kmen + 'ný', dict(d='1', g='M'))
