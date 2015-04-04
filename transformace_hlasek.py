###################################################
######## Transformace hlasek
###################################################

def kraceni(vokala):
    """
    program slouží ke zkrácení vokál
    s ohledem na historický vývoj
    jsou zde tedy pro ilustraci zaznamenány vztahy ů x o; ou x u
    !!! jedná se o kostru k rozšíření !!!
    Funkce: vstupem je řetězec - vokála a pokud je validní, výstupem je její krátká varianta
    """
    dlouhe = {'á':'a', 'é':'e', 'í':'i', 'ý':'y', 'ou':'u', 'ú':'u', 'ů':'o'}
    if vokala in dlouhe:
        return dlouhe[vokala]
    else:
        return vokala

def dlouzeni(vokala):
    """
    program slouží k prodloužení vokál
    jedná se protiklad ke krácení
    !!! jedná se o kostru k rozšíření !!!
    """
    if vokala == "a":
        vokala = "á"
    elif vokala == "o":
        vokala = "ů"
    elif vokala == "u":
        vokala = "ou"
    elif vokala == "e":
        vokala == "é"
    return vokala

def alternace1(k):
    """
    program zajišťuje změkčování vybraných konzonantů
    podle historického vývoje první palatalizace
    + poslední stupeň palatalizace alveolár v češtině (r=>ř)
    """
    if k == 'k': # "k" změním na "č"
        k = 'č'
    elif k == 'z': # "z" změním na "ž"; původně bylo g na ž, ale tohle je častější
        k = 'ž'
    elif k == 'h': # "h" změním na "ž"
        k = 'ž'
    elif k == "ch": # spřežku "ch" změním na "š"
        k = 'š'
    elif k == 'r': # "r" změním na "ř"
        k = 'ř'
    return k # vracím výsledek

def alternace2(k):
    """
    program zajišťuje změkčování vybraných konzonantů
    podle historického vývoje
    funkce je téměř totožná s první palatalizací,
    druhá palatalizace však proběhla jinak a má jiné výsledky
    """
    if k == 'k':  # "k" změním na "c"
        k = 'c'
    elif k == 'g': # "g" změním na "z"
        k = 'z'
    elif k == 'h': # "h" změním na "z"
        k = 'z'
    elif k == "ch": # spřežku "ch" změním na s
        k = 's'
    return n # vracím výsledek, pokud nebyl palatizovaný, je týž
