from collections import OrderedDict
import re


# Současná grafika (např. dě, tě, ně) zastírá, že se fonémy měkčí
# (d → ď, t → ť, n → ň) či že se mezi ně a jať vkládá j nebo ň (b, p, v; m).
# Naopak ch, h, k a r se i v grafice (na „povrchu“) mění. L a s prošly
# depalatalizací dokonce bez jakékoli stopy po ě.
PALATALIZACE = OrderedDict((
    # regresivní palatalizace (usnadnění výslovnosti)
    ('chš', 'šš'),
    ('hš', 'žš'),
    ('zš', 'žš'),

    # palatalizace vlivem měkčícího e/i
    ('chě', 'še'),
    ('chí', 'ší'),
    ('hě', 'ze'),
    ('kě', 'ce'),
    ('kí', 'čí'),
    ('lě', 'le'),
    ('rě', 'ře'),
    ('sě', 'se'),
))
PALATALIZOVAT = re.compile('|'.join(grafemy for grafemy in PALATALIZACE))


def palatalizace(slovo):
    while True:
        slovo, zmeneno = PALATALIZOVAT.subn(
            lambda nalez: PALATALIZACE[nalez.group()], slovo)
        if not zmeneno:
            return slovo
