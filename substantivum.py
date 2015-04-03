import slovni_tvar


class Substantivum(slovni_tvar.SlovniTvar):
    def __init__(self, rodic=None, lemma='', atributy={}, vyznamy={}):
        super().__init__(rodic, lemma, atributy, vyznamy)

        self.atributy['k'] = '1'
        # u deadjektiv nechceme stupeň fundujícího slova (degree)
        self.atributy.pop('d', None)
