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
    ('cí', 'čí'),  # hranice → příhraničí
    ('chě', 'še'),
    ('chí', 'ší'),  # střecha → přístřeší
    ('hě', 'ze'),
    ('hí', 'ží'),  # břeh → pobřeží
    ('kě', 'ce'),
    ('kí', 'čí'),  # bok → úbočí
    ('lě', 'le'),
    ('rě', 'ře'),
    ('rí', 'ří'),  # hora → pohoří
    ('sě', 'se'),

    # vynucená regresivní palatalizace? (vzduch+'ný → vzdušný)
    ("c'", "č"),
    ("h'", "ž"),
    ("ch'", "š"),
    ("k'", "č"),
    ("'", ""),
))
PALATALIZOVAT = re.compile('|'.join(grafemy for grafemy in PALATALIZACE))


KRACENI = OrderedDict((
    ('á', 'a'),  # krátký → kratší
    ('ú', 'u'),  # úzký → užší
    # někdy se možná bude hodit: ou → u, ů → o
))
ZKRATIT = re.compile('|'.join(grafemy for grafemy in KRACENI))


def palatalizovat(slovo):
    """
    Pokud subn najde např. „chě“ v „tichě“, zavolá pomocnou funkci, a ta mu za
    „chě“ vyhledá náhradu „še“. Když už není co měnit, palatalizace končí.
    """
    while True:
        slovo, zmeneno = PALATALIZOVAT.subn(
            lambda nalez: PALATALIZACE[nalez.group()], slovo)
        if not zmeneno:
            return slovo


def zkratit(slovo):  # stejná funkce jako palatalizace
    while True:
        slovo, zmeneno = ZKRATIT.subn(lambda nalez: KRACENI[nalez.group()],
                                     slovo)
        if not zmeneno:
            return slovo
