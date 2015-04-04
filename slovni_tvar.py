class SlovniTvar:
    def __init__(self, rodic=None, lemma='', atributy={}, vyznamy={}):
        """
        Slovní tvar se dá vytvořit od jiného a k tomu doplnit některé položky.
        """
        self.rodic = rodic  # odkaz na fundující slovo
        if rodic:
            self.lemma = rodic.lemma
            self.atributy = dict(rodic.atributy)
            self.vyznamy = dict(rodic.vyznamy)

            if lemma:
                self.lemma = lemma
            self.atributy.update(atributy)
            self.vyznamy.update(vyznamy)
        else:
            self.lemma = lemma
            self.atributy = atributy
            self.vyznamy = vyznamy

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
            print('  '*hloubka_rekurze, odvozenina, sep='  ')
            if hloubka_rekurze <= max_hloubka_rekurze:
                odvozenina.vypsat_odvozeniny(
                    max_hloubka_rekurze=max_hloubka_rekurze,
                    hloubka_rekurze=hloubka_rekurze + 1)

    vytvorit_odvozeniny = [].__iter__
    _zapamatovane_odvozeniny = None

    def odvozeniny(self):
        if self._zapamatovane_odvozeniny is None:
            self._zapamatovane_odvozeniny = list(self.vytvorit_odvozeniny())
        for odvozenina in self._zapamatovane_odvozeniny:
            yield odvozenina
