from itertools import chain
import logging

import adverbium
import slovni_tvar
import substantivum
from upravy import palatalizovat, zkratit

NEPRAVIDELNE_KOMPARATIVY = {
    'dlouhý': 'delší',
    'dobrý': 'lepší',
    'malý': 'menší',
    'pěkný': 'hezčí',
    'starý': 'starší',
    'široký': 'širší',
    'špatný': 'horší',
    'velký': 'větší',
    'veliký': 'větší',
    'zlý': 'horší',
}


class Adjektivum(slovni_tvar.SlovniTvar):
    def __init__(self, rodic=None, lemma='', atributy={}, vyznamy={}):
        super().__init__(rodic, lemma, atributy, vyznamy)

        self.atributy['k'] = '2'
        self.stupen = self.atributy.get('d')  # degree, stupeň
        self.odtrhnout_koncovku()

    def odtrhnout_koncovku(self):
        if self.lemma[-1] in ('í', 'ý'):
            self.kmen = self.lemma[:-1]
            self.koncovka = self.lemma[-1]
        elif self.lemma[-2:] in ('ův', 'in'):
            self.kmen = self.lemma
            self.koncovka = ''

            # to by mělo přidělovat už fundující substantivum
            if 'posesivum' not in self.vyznamy:
                logging.warning('neoznačené posesivum? ' + self.lemma)
                self.vyznamy['posesivum'] = True
        else:
            raise ValueError('Nerozpoznaná adjektivní koncovka: ' + self.lemma)

    def vytvorit_odvozeniny(self):
        if self.stupen == '1':
            return chain(
                self.komparativ(),
                self.vlastnost(),
                self.adverbializace(),
            )
        elif self.stupen == '2':  # asi nemá smysl vytvářet nejnejlepšejší
            return self.superlativ()

    def komparativ(self):
        if self.vyznamy.get('posesivum'):
            return

        komparativ = NEPRAVIDELNE_KOMPARATIVY.get(self.lemma)
        if komparativ:
            yield Adjektivum(self, komparativ, dict(d='2'))
            # pravidelně tvořené tvary se tu a tam vyskytnou, takže jdeme dál

        kmenova_finala = self.kmen[-1]  # konsonant
        ŠÍ = ('d', 'h')  # zahrnuje i ch

        if self.kmen.endswith('sk'):
            komparativ = self.kmen[:-2] + 'štější'
        elif self.kmen.endswith('ck'):
            komparativ = self.kmen[:-2] + 'čtější'
        elif kmenova_finala in ŠÍ:
            komparativ = self.kmen + 'ší'
        elif kmenova_finala == 'k':
            komparativ = self.kmen + 'í'  # hezký > hezčí
        else:
            komparativ = self.kmen + 'ější'
        yield Adjektivum(self, palatalizovat(komparativ), dict(d='2'))

        if kmenova_finala == 'k' and len(self.kmen) >= 3:
            # krátký > kratší, úzký > užší
            zkraceny = zkratit(self.kmen[:-1]) + 'ší'
            yield Adjektivum(self, palatalizovat(zkraceny), dict(d='2'))

        # TODO: zjistit, jestli krácení neovliňuje kombinace souhlásek po
        # dlouhé samohlásce (-tk-, -zk-) => korpusem

    def superlativ(self):
        yield Adjektivum(self, 'nej' + self.lemma, dict(d='3'))

    # TODO: dobrota, dobrotivý (dobrotivec), dobrák
    def vlastnost(self):
        if self.koncovka == 'ý':
            # derivát je femininum (g = genus, jmenný rod)
            yield substantivum.Substantivum(
                self, self.lemma[:-1] + 'ost', dict(g='F'),
                dict(vlastnost=True))

    def adverbializace(self):
        yield adverbium.Adverbium(self, self.kmen + 'o')

        if self.lemma[-3:] in ('cký', 'ský'):
            yield adverbium.Adverbium(self, self.kmen + 'y')
        elif self.koncovka in ('í', 'ý'):
            yield adverbium.Adverbium(self, palatalizovat(self.kmen + 'ě'))
