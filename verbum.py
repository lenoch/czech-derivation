from itertools import chain

import adjektivum
import slovni_tvar

class Verbum(slovni_tvar.SlovniTvar):
    # TODO: pro-dlouž-it, ob-nov-it
    PREFIXY = ('do', 'na', 'o', 's', 'u', 'vy', 'za')
    TEMATA = ('a', 'e', 'i', 'nou')

    def __init__(self, rodic=None, atributy={}, vyznamy={}, lemma='', koren='',
                 prefix='', sufix='', koncovka=''):
        if lemma:
            koren, sufix, koncovka = self.zjistit_tema(lemma)

        super().__init__(rodic, atributy, vyznamy, koren, prefix, sufix,
                         koncovka)

        self.atributy['k'] = '5'
        self.neg = self.atributy.get('e')
        self.aspekt = self.atributy.get('a')
        self.tema = self.sufixy[-1] if self.sufixy else ''

        modus = self.atributy.get('m')
        if modus is not None and modus != 'F':
            raise ValueError('očekává se infinitiv')

    @classmethod
    def zjistit_tema(cls, lemma):
        # TODO: nepravidelná/atematická slovesa řešit výjimkami
        if not lemma.endswith('t'):
            raise ValueError('očekává se infinitiv')
        kmen = lemma[:-1]  # derivaci začínáme od neprefigovaných sloves!
        for tema in cls.TEMATA:
            if kmen.endswith(tema):
                koren = kmen[:-len(tema)]
                return koren, tema, 't'
        else:
            raise ValueError('neznámý tematický sufix (nepravidelné sloveso?)')

    def vytvorit_odvozeniny(self):
        return chain(
            self.negace(),
            self.adjektivizace(),
            self.prefixace(),
        )

    def negace(self):
        if self.neg != 'N':
            yield Verbum(self, dict(e='N'), prefix='ne')

    def prefixace(self):
        if self.neg != 'N' and self.aspekt == 'I':
            for prefix in self.PREFIXY:
                yield Verbum(self, dict(a='P'), prefix=prefix)

    def adjektivizace(self):
        # přes slovnědruhově sporné n-ové participium
        if self.vyznamy.get('posesivum'):
            return

        # tenčit → tenčený, plašit → plašený
        if self.tema == 'i':
            yield adjektivum.Adjektivum(self, dict(d='1', g='M'),
                                        nahradit_sufix="'e", sufix='n',
                                        koncovka='ý')
        else:  # plakat → plakaný
            yield adjektivum.Adjektivum(self, dict(d='1', g='M'), sufix='n',
                                        koncovka='ý')
        # TODO: posmutnělý
