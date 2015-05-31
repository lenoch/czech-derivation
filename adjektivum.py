from itertools import chain

import adverbium
import slovni_tvar
import substantivum
from transformace_hlasek import alternace1, kraceni
from upravy import palatalizace


NEPRAVIDELNE_KOMPARATIVY = {
    'dobrý': 'lepší',
    'malý': 'menší',
    'starý': 'starší',
    'široký': 'širší',
    'špatný': 'horší',
    'velký': 'větší',  # TODO: veliký?
}


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
        likvidy = ['l', 'r']  # připojuje se "ejší"
        jat = ['n', 'm', 't', 'v']  # zde se bude připojovat "ější"
        # spadá sem i ch; připojuje se jen "ší", případné krácení v kořeni
        bez_jotace = ['d', 'h', 'k', 'p']

        if self.stupen == '1':
            komparativ = NEPRAVIDELNE_KOMPARATIVY.get(self.lemma)
            if komparativ:
                yield Adjektivum(self, komparativ, dict(d='2'))
                return

            kmen = self.lemma[:-1]
            kmenova_finala = kmen[-1]  # konsonant
            kmen_s_alternaci = kmen[:-1] + alternace1(kmenova_finala)

            if kmenova_finala in jat:
                # historická: v původní funkci (v transformacích) bez alternace
                komparativ = kmen_s_alternaci + 'ější'
            elif kmenova_finala in likvidy:
                komparativ = kmen_s_alternaci + 'ejší'
            elif kmenova_finala in bez_jotace:
                if kmen.endswith('ch'):  # kmen[-2] == 'c' (co jinýho před h)
                    komparativ = kmen[:-2] + alternace1('ch') + 'ší'
                elif kmenova_finala == 'k':
                    # krátký > kratší (úzký > užší)
                    komparativ = (kmen[:-3] + kraceni(kmen[-3]) +
                                  alternace1(kmen[-2]) + 'ší')
                    yield Adjektivum(self, palatalizace(komparativ),
                                     dict(d='2'))
                    # hezký > hezčí
                    komparativ = kmen_s_alternaci + 'í'
                else:
                    komparativ = kmen_s_alternaci + 'ší'
            else:
                komparativ = kmen_s_alternaci + 'í'
            yield Adjektivum(self, palatalizace(komparativ), dict(d='2'))

        elif self.stupen == '2':  # asi nemá smysl vytvářet nejnejlepšejší
            yield Adjektivum(self, 'nej' + self.lemma, dict(d='3'))

    # TODO: dobrota, dobrotivý (dobrotivec), dobrák
    def mladost(self):
        if self.stupen == '1' and self.lemma.endswith('ý'):
            # derivát je femininum (g = genus, jmenný rod)
            yield substantivum.Substantivum(
                self, self.lemma[:-1] + 'ost', dict(g='F'),
                {'vlastnost': True})

    def adverbializace(self):
        if self.stupen == '1':
            yield adverbium.Adverbium(self, self.lemma[:-1] + 'o')

            if self.lemma[-3:] in ('cký', 'ský'):
                yield adverbium.Adverbium(self, self.lemma[:-1] + 'y')
            elif self.lemma[-1] in ('í', 'ý'):
                kmen = self.lemma[:-1]
                yield adverbium.Adverbium(self, palatalizace(kmen + 'ě'))
