from itertools import chain
import logging

import adverbium
import slovni_tvar
import substantivum
from upravy import zkratit
import verbum

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
    def __init__(self, rodic=None, atributy={}, vyznamy={}, lemma='', koren='',
                 prefix='', sufix='', koncovka='', nahradit_sufix=None):
        if lemma:
            koren, koncovka = self.odtrhnout_koncovku(lemma)

        super().__init__(rodic, atributy, vyznamy, koren, prefix, sufix,
                         koncovka, nahradit_sufix)

        self.atributy['k'] = '2'  # kind, slovní druh, part of speech (POS)
        self.stupen = self.atributy.get('d', '1')  # degree, stupeň
        self.gradable = self.stupen in ('1', '2', '3')
        if not self.gradable:
            self.stupen = self.atributy['d'] = 'N'  # nestupňovatelné

    @staticmethod
    def odtrhnout_koncovku(lemma):
        if lemma[-1] in ('í', 'ý'):
            return lemma[:-1], lemma[-1]
        elif lemma[-2:] in ('ův', 'in'):
            return lemma, ''
        else:
            raise ValueError('Nerozpoznaná adjektivní koncovka: ' + lemma)

    def vytvorit_odvozeniny(self):
        if self.stupen in ('1', 'N'):
            return chain(
                self.komparativ(),
                self.vlastnost(),
                self.adverbializace(),
                self.lesnik(),
                # self.slovnik(),
                # TODO: starý → stařec, tvrdý → tvrďák
                self.susit(),
            )
        elif self.stupen == '2':  # asi nemá smysl vytvářet nejnejlepšejší
            return self.superlativ()

    def komparativ(self):
        if not self.gradable:
            return

        vyjimka = NEPRAVIDELNE_KOMPARATIVY.get(self.lemma)
        if vyjimka:
            yield Adjektivum(self, dict(d='2'), lemma=vyjimka)
            # pravidelně tvořené tvary se tu a tam vyskytnou, takže jdeme dál

        kmenova_finala = self.kmen[-1]  # konsonant
        sufixy = dict(
            k='',  # hezk-ý → hezč-í
            d='š',  # mlad-ý → mlad-š-í
            h='š',  # drah-ý → draž-š-í, ale i plach-ý → plaš-š-í
        )

        yield Adjektivum(self, dict(d='2'), sufix=sufixy.get(
            kmenova_finala, 'ějš'), koncovka='í')

        if kmenova_finala == 'k' and len(self.kmen) >= 3:
            # krá-t-ký > krat-š-í, úz-k-ý > už-š-í
            zkraceny = zkratit(self.kmen[:-1])
            yield Adjektivum(self, dict(d='2'), koren=zkraceny, sufix='š',
                             koncovka='í')

        # TODO: zjistit, jestli krácení neovliňuje kombinace souhlásek po
        # dlouhé samohlásce (-tk-, -zk-) => korpusem

    def superlativ(self):
        yield Adjektivum(self, dict(d='3'), prefix='nej')

    # TODO: dobrota, dobrotivý (dobrotivec), dobrák
    def vlastnost(self):
        if self.koncovka == 'ý':
            # derivát je femininum (g = genus, jmenný rod)
            yield substantivum.Substantivum(self, dict(g='F'), dict(
                vlastnost=True, anim=False), sufix='ost')

    def adverbializace(self):
        if self.vyznamy.get('posesivum'):
            return

        yield adverbium.Adverbium(self, koncovka='o')

        if self.lemma[-3:] in ('cký', 'ský'):
            yield adverbium.Adverbium(self, koncovka='y')
        elif self.koncovka in ('í', 'ý'):
            yield adverbium.Adverbium(self, koncovka='ě')

    def lesnik(self):
        if self.lemma.endswith('ní') and not self.vyznamy.get('posesivum'):
            yield substantivum.Substantivum(self, dict(g='M'), dict(anim=True),
                                            sufix='ík')

    # def slovnik(self):
    #     # životnost základu asi nesouvisí s životností odvozeniny:
    #     # slovo → slovní → slovník
    #     # hora → horní → horník
    #     if self.lemma.endswith('ní') and not self.vyznamy.get('posesivum'):
    #         yield substantivum.Substantivum(
    #             self, self.kmen + 'ík', dict(g='I'),
    #             dict(anim=False))
    #         yield substantivum.Substantivum(
    #             self, self.kmen + 'ice', dict(g='F'),
    #             dict(anim=False))

    def susit(self):
        # sloveso s významem „stávat se suchým“ (ale: plachý → plašit)
        if not self.gradable:
            # adjektivní kořeny tuto vlastnost mají, odvozené často (?) ne, tak
            # toho prozatím využijeme
            return

        # zabránění sekundární derivaci: udobřit → udobřený → *udobřenit
        # (jeden tematický sufix tam už je)
        if self.tema:
            return

        yield verbum.Verbum(self, dict(a='I'), tema='i', koncovka='t')

    # další: postaršit, zesmutnět, posmutnět
    # jiná témata: blb-nou-t
