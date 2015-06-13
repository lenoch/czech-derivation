# Posledních 5 prefixů lze aplikovat jen na uzavřenou množinu slov,
# zpravidla 1-2.
# Přídávám jejich výčet - zahraničí, prostředí, průčelí, průvodčí,
# scestí, výročí, výsluní.
# Dilema - utvořit výjimky nebo zbytečně přegenerovávat?
#
# Ondra: Radši výjimky, ale ty by měly být podložené korpusem, tedy
# [lemma="(za|pro|prů|s|vý).+í" & tag="k1.*"]
ZAHRANICI = {
    'cesta': 's',
    'čelo': 'prů',  # vážně?
    'hranice': 'za',
    'rok': 'vý',
    # vý-slun-í (odtrhává se tedy ze slunce deminutivní sufix -c-?)
    'střed': 'pro',  # tak?
    # prů-vodčí?
}

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

ADVERBIALNI_KOMPARATIVY = {}
for pozitivy, komparativy in _VYJIMKY_U_KOMPARATIVU:
    for pozitiv in pozitivy:
        ADVERBIALNI_KOMPARATIVY[pozitiv] = komparativy
