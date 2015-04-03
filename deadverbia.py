zakonceni = [  # TODO: dočasné
    ('dý', 'dě'),
    ('rý', 'ře'),
    ('bý', 'bě'),
    ('vý', 'vě'),
    ('mý', 'mě'),
    ('sý', 'se'),
    ('pý', 'pě'),
    ('tý', 'tě'),
    ('lý', 'le'),
    ('ný', 'ně'),
    ('ní', 'ně'),
    ('chý', 'še'),
    ('hý', 'ze'),
    ('ský', 'sky'),
    ('cký', 'cky'),
    ('ký', 'ce'),
]


# Odvozování adverbií na základě prefixace a sufixace, na další jsem zatím nenarazil
def prefixace_sufixace(lemma, atributy, vyznamy):
    if lemma.endswith('o'):
        yield 'na' + lemma, atributy, vyznamy

    for adjektivni, adverbialni in zakonceni:
        if lemma.endswith(adverbialni):
            delka_zakonceni = len(adverbialni)
            lemma = lemma[:-delka_zakonceni] + adjektivni[:-1]
            yield 'do' + lemma + 'a', atributy, vyznamy
            prefix = 'ze' if lemma[0] in ('s', 'z') else 'z'
            yield prefix + lemma + 'a', atributy, vyznamy
            yield 'na' + lemma + 'o', atributy, vyznamy


_VYJIMKY_U_KOMPARATIVU = (
    (['dobře'], ['lépe', 'líp']),
    (['zle', 'špatně'], ['hůře', 'hůř']),
    (['brzy'], ['dříve', 'dřív']),
    (['dlouze', 'dlouho'], ['déle']),
    (['vysoce', 'vysoko'], ['výš', 'výše']),
    (['málo'], ['méně', 'míň']),
    (['těžko', 'těžce'], ['tíže', 'tíž']),
    (['snadno', 'snadně'], ['snáze', 'snáz', 'snadněji']),
    (['hluboko', 'hluboce'], ['hloub', 'blouběji']),
    (['široko', 'široce'], ['šíře', 'šíř', 'šířeji']),
    (['úzko', 'úzce'], ['úže', 'úžeji']),
)
VYJIMKY_U_KOMPARATIVU = {}
for pozitivy, komparativy in _VYJIMKY_U_KOMPARATIVU:
    for pozitiv in pozitivy:
        VYJIMKY_U_KOMPARATIVU[pozitiv] = komparativy


def stupnovani(lemma, atributy, vyznamy):
    if atributy.get('d') == '1':
        # Kvůli množství (snad všech) výjimek níže, které mají více variant,
        # jsem udělal komparativ jako seznam
        atributy['d'] = '2'

        komparativy = VYJIMKY_U_KOMPARATIVU.get(lemma, [])
        if not komparativy:
            if lemma.endswith('ce'):
                komparativy = [lemma[:-2] + 'čeji']
            elif lemma.endswith('cky'):
                komparativy = [lemma[:-3] + 'čtěji']
            elif lemma.endswith('sky'):
                komparativy = [lemma[:-3] + 'štěji']
            elif lemma[-1] in ('e', 'ě'):
                komparativy = [lemma + 'ji']

        for komparativ in komparativy:
            yield komparativ, atributy, vyznamy

    if atributy.get('d') == '2':
        atributy['d'] = '3'
        # Pokud nedošlo ke konverzi z 1. stupně, tak se za komparativ vezme
        # vstupní slovo
        if not komparativy:
            komparativy = [lemma]

        for komparativ in komparativy:
            yield 'nej' + komparativ, atributy, vyznamy
