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
    if vokala == "á":
        vokala = "a"
    elif vokala == "ů":
        vokala = "o"
    elif vokala == "ou":
        vokala = "u"
    elif vokala == "é":
        vokala == "e"
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

def palatalizace1(k):
    """
    program zajišťuje změkčování vybraných konzonantů
    podle historického vývoje první palatalizace
    + poslední stupeň palatalizace alveolár v češtině (r=>ř)
    """
    if k == 'k': # "k" změním na "č"
        k = 'č'
    elif k == 'g': # "g" změním na "ž" (nemělo by k tomu docházet, g se vyvinulo ve spisovném jazyce na "h", ponechávám pro možnost program rozšířit)
        k = 'ž'
    elif k == 'h': # "h" změním na "ž"
        k = 'ž'
    elif k == "ch": # spřežku "ch" změním na "š"
        k = 'š'
    elif k == 'r': # "r" změním na "ř"
        k = 'ř'
    return k # vracím výsledek

def palatalizace2(k):
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


def stupnovani(slovo, kat):
    """
    program slouží ke stupňování
    vstupem je nominativ a kategorie
    kategorie jsou Adj a Adv
    Tzn. ze vstupu adekvátnímu zápisu v korpusu jako tag A...1....1.*
    vytvoří výstup A...1....2.* a při volání prefixace i A...1....3.*
    V budoucnu by měla umět také pro vstup ekvivalentní D........1.*
    vytvořit D........2.* a D........3.*
    """
    if kat == "Adj":
        nepravidelnost = ["dobrý"] # prostor pro další
        """
    Pro nepravidelné stupňování bude nutné utvořit slovník (slovo - 1. stupeň)
    (Prozatím seznam, se slovníkem příliš neumím zacházet)
        """
        if slovo in nepravidelnost:
            print ("!! nepravidelné")  #prozatímní řešení, vytvoří i tak hypotetický 2. stupeň
            pass
        zmena = slovo[-2]  #která hláska se bude měnit
        slovo = slovo[0:-2] # zkrátíme slovo tak, aby končilo před hláskou změna
        vysledek1 = ""
        vysledek2 = ""  # pro 3. stupeň - bude se nejspíš volat derivace prefixů
        seznam = ["l", "r"]
        seznam2 = ["n", "m", "v", "t"]
        seznam3 = ["d", "p", "h"]
        if zmena in seznam:
            vysledek1 = slovo + palatalizace1(zmena)+ "ejší"
        elif zmena in seznam2:
            vysledek1 = slovo + zmena + "ější"
        elif zmena in seznam3:
            if slovo[-1] == "c":
                zmena = "ch"
                slovo = slovo[0:-1]
            vysledek1 = slovo + palatalizace1(zmena) + "ší"
        else:
            vysledek1 = slovo + palatalizace1(zmena) + "í"
    if kat == "Adv": # předpokládáme, že tahle funkce bude moci zahrnout i adverbia
        pass
    print (vysledek1)

    # pro třetí stupeň by se volal skript prefixace
""" Pozor na slovo krátký - kratší - nutné zjistit, jak častý je to jev, zda
vhodný do seznamu nebo pro vlastní pravidlo """

stupnovani("mladý", "Adj")
stupnovani("hezký", "Adj")
stupnovani("plachý", "Adj")
stupnovani("drahý", "Adj")
stupnovani("smutný", "Adj")
stupnovani("znamenitý", "Adj")
stupnovani("hebký", "Adj") #netvoří hebčejší, ale jen hebčí!
stupnovani("přímý", "Adj")
stupnovani("vzácný", "Adj")
stupnovani("dobrý", "Adj")
stupnovani("nový", "Adj")
stupnovani("veselý", "Adj")

