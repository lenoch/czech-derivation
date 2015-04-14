from transformace_hlasek import alternace1

def sub_cirkumfixace(lemma,atributy,vyznamy):

    """
    Derivace substantiv pomocí cirkumfixace
    Jsou-li slova zakončena vokálem, tak tento vokál odpadá.
    V případě zakončení na konsonant dochází k měkčení,
    a to i po předešlém odpadnutí vokálu. Měkčení je shodné
    s fcí alternace1 v transformace_hlasek.py
    Výjimečně dochází k alternacím kvantity vok. (jméno - příjmení)
    To jsem zatím neřešil.

    Substantiva (navíc lemmata) asi nemohou být zakončena všemi vokály,
    ale touto problematikou jsem se dosud nezabýval a uvedl je všechny.

    V praxi jen cyklicky rozšiřuji slovo o jeden z množiny prefixů a o afix.

    K množině prefixů: 
    Čerpal jsem z výzkumu - Jazyk a slovník. Vybrané lingvistické studie.
    Dostupné na Google books, str. 171-173.

    Posledních 5 prefixů lze aplikovat jen na uzavřenou množinu slov, zpravidla 1-2.
    Přídávám jejich výčet - zahraničí, prostředí, průčelí, průvodčí,
    scestí, výročí, výsluní.
    Dilema - utvořit výjimky nebo zbytečně přegenerovávat?

    Funkce alternace1 mi neošetří alternaci ch-š, protože
    ji aplikuji až na poslední znak. Nevím, jak to udělat tak,
    aby to fungovalo, nezbylo mi nic jiné než udělat výjimku.
    """
    
    vokaly=['a','á','e','é','i','í','o','ó','u','ú','y','ý','ě']
    prefixy=['o','ob','od','ná','nad','po','pod','před','sou','ú', \
         'pří','roz','zá','za','pro','prů','s','vý']
    
    if lemma[-1:] in vokaly:
        lemma=lemma[:-1]

    if lemma[-2:]=='ch':
        lemma=lemma[:-2] + 'š'
        
    konsonant=alternace1(lemma[-1:])
    lemma=lemma[:-1] + konsonant
    for prefix in prefixy:
        yield prefix + lemma + 'í', atributy, vyznamy

def sub_prefixace(lemma,atributy,vyznamy):
    """
    Vytváření substantivních derivátů pomocí množiny prefixů
    Vycházím ze záznamu na Wikipedii - "Seznam českých předpon"
    Vybral jsem předpony, kterými lze teoreticky modifikovat příslušná substantiva
    """
    
    prefixy=['polo','pra','pa','skoro','sotva','mezi','ne','pseudo','super', \
             'maxi', 'mini','giga','ultra','ex','hyper','neo','retro']

    for prefix in prefixy:
        yield prefix + lemma, atributy, vyznamy

def sub_konatelska(lemma,atributy,vyznamy):
    """
    Vytváření konatelských substantiv
    V případě zakončení na vokál jej odseknu
    K alternacím s výjimkou c -> č nedochází
    Nakonec připojím jeden z množiny konatelských sufixů
    Zřídka funkce utvoří více než jedno v praxi používané slovo
    Tzn. vysoká míra nadgenerování
    """
    
    vokaly=['a','á','e','é','i','í','o','ó','u','ú','y','ý','ě']
    sufixy=['ař','ář','ista','ník']
    
    if lemma[-1:] in vokaly:
        lemma=lemma[:-1]

    if lemma[-1:]=='c': lemma=lemma[:-1] + 'č'

    for sufix in sufixy:
        yield lemma + sufix, atributy, vyznamy
