import slovni_tvar


class Adverbium(slovni_tvar.SlovniTvar):
    def __init__(self, rodic=None, lemma='', atributy={}, vyznamy={}):
        super().__init__(rodic, lemma, atributy, vyznamy)

        self.atributy['k'] = '6'
        self.stupen = self.atributy.get('d')  # degree, stupeň
