from upravy import palatalizovat


class SlovniTvar:
    def __init__(self, rodic=None, atributy={}, vyznamy={}, koren='',
                 prefix='', sufix='', koncovka=None, nahradit_sufix=None):
        """
        Slovní tvar se dá vytvořit od jiného a k tomu doplnit některé položky.
        """
        self.rodic = rodic  # odkaz na fundující slovo
        if rodic:
            self.koren = rodic.koren
            self.prefixy = list(rodic.prefixy)
            self.sufixy = list(rodic.sufixy)
            self.tema = rodic.tema  # nastavuje sloveso
            self.koncovka = rodic.koncovka

            self.atributy = dict(rodic.atributy)
            self.vyznamy = dict(rodic.vyznamy)

            if koren:
                self.koren = koren
            if prefix:
                self.prefixy.insert(0, prefix)
            if nahradit_sufix is not None:
                self.sufixy[-1] = nahradit_sufix
            if sufix:
                self.sufixy.append(sufix)
                self.koncovka = ''
            if koncovka is not None:
                self.koncovka = koncovka

            self.atributy.update(atributy)
            self.vyznamy.update(vyznamy)
        else:
            self.koren = koren
            self.prefixy = [prefix] if prefix else []
            self.sufixy = [sufix] if sufix else []
            self.tema = None
            self.koncovka = koncovka or ''

            self.atributy = dict(atributy)
            self.vyznamy = dict(vyznamy)

    @property
    def kmen(self):
        return palatalizovat(''.join(self.prefixy) + self.koren +
                             ''.join(self.sufixy)).replace('_', '')

    @property
    def lemma(self):
        return palatalizovat(''.join(self.prefixy) + self.koren +
                             ''.join(self.sufixy) +
                             self.koncovka).replace('_', '')

    def __str__(self):
        return '  '.join((self.lemma, self.zformatovat_atributy(),
                         self.zformatovat_vyznamy()))

    def zformatovat_atributy(self):
        return ' '.join(atribut + '=' + str(hodnota) for atribut, hodnota
                        in sorted(self.atributy.items()))

    def zformatovat_vyznamy(self):
        return ' '.join(vyznam + '=' + hodnota if isinstance(hodnota, str) else
                        '+' + vyznam if hodnota else '-' + vyznam for
                        vyznam, hodnota in sorted(self.vyznamy.items()))

    def vypsat_odvozeniny(self, max_hloubka_rekurze=0, hloubka_rekurze=0):
        for odvozenina in self.odvozeniny():
            print('  '*hloubka_rekurze, odvozenina, sep='  ', flush=True)
            if hloubka_rekurze <= max_hloubka_rekurze:
                odvozenina.vypsat_odvozeniny(
                    max_hloubka_rekurze=max_hloubka_rekurze,
                    hloubka_rekurze=hloubka_rekurze + 1)

    vytvorit_odvozeniny = [].__iter__
    _zapamatovane_odvozeniny = None

    def odvozeniny(self):
        if self._zapamatovane_odvozeniny is None:
            self._zapamatovane_odvozeniny = list(
                self.vytvorit_odvozeniny() or [])
        for odvozenina in self._zapamatovane_odvozeniny:
            yield odvozenina

    def lemmata(self, max_hloubka_rekurze=0, hloubka_rekurze=0):
        for odvozenina in self.odvozeniny():
            yield odvozenina.lemma
            if hloubka_rekurze <= max_hloubka_rekurze:
                for lemma in odvozenina.lemmata(max_hloubka_rekurze,
                                                hloubka_rekurze + 1):
                    yield lemma

    @classmethod
    def zakazat_proces(cls, proces):
        setattr(cls, proces, cls.prazdny_proces)

    def prazdny_proces(self):
        return []
