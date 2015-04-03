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

    def zformatovat_atributy(self):
        return ' '.join(atribut + '=' + hodnota for atribut, hodnota
                        in sorted(self.atributy.items()))
