import transformace_hlasek

# predpony
# z, s, v, u, o,
def z(slovo):
    out = "z" + slovo
    return out
def s(slovo):
    out = "s" + slovo
    return out
def v(slovo):
    out = "v" + slovo
    return out
def u(slovo):
    out = "u" + slovo
    return out
def o(slovo):
    out = "o" + slovo
    return out

###############################################x
# ne, do, po, ná, na, ob, vy, vý, vz, za, zá, pů
def negace(slovo):
    out = "ne" + slovo
    return out

def do(slovo):
    out = "do" + slovo
    return out

def po(slovo):
    out = "po" + slovo
    return out

def na1(slovo):
    out = "na" + slovo
    return out

def na2(slovo):
    out = "ná" + slovo
    return out

def ob(slovo):
    out = "ob" + slovo
    return out

def vy1(slovo):
    out = "vy" + slovo
    return out

def vy2(slovo):
    out = "vý" + slovo
    return out

def vz(slovo):
    out = "vz" + slovo
    return out

def za1(slovo):
    out = "za1" + slovo
    return out

def za2(slovo):
    out = "zá" + slovo
    return out

def pu2(slovo):
    out = "pů" + slovo
    return out

####################################################x
# pro, nej, při, prů, pře, pří, sou, nad, pod, pra
def pro(slovo):
    out = "pro" + slovo
    return out

def nej(slovo):
    out = "nej" + slovo
    return out

def pri1(slovo):
    out = "při" + slovo
    return out

def pri2(slovo):
    out = "pří" + slovo
    return out

def pru(slovo):
    out = "prů" + slovo
    return out

def pod(slovo):
    out = "pod" + slovo
    return out

def nad(slovo):
    out = "nad" + slovo
    return out

def sou(slovo):
    out = "sou" + slovo
    return out

def pra(slovo):
    out = "pra" + slovo
    return out

####################################################X
# nade, před, vele,
def pred(slovo):
    out = "před" + slovo
    return out

def vele(slovo):
    out = "vele" + slovo
    return out

#####################################################X
# přede, proti
def proti(slovo):
    out = "proti" + slovo
    return out
######################################################x
##########xx  Is in?
#######################################################x

def is_in(seznam,item):
    """ověřuje, jestli je položka v seznamu"""
    #print("tohle je",item)
    if item is not None:
        if isinstance(seznam, list):
            pass
        else:
            seznam = [seznam]
        if isinstance(item, list):
            for i in item:
                #print(item, "je seznam, tak volám is_in", i)
                is_in(seznam,i)
            return
        if item not in seznam:
            if item[0:1] == item [2:3] == item [4:5]:
                return
            return seznam.append(item)
            """má vložit položku do seznamu"""
        else:
            #pass
            print ("item", item, "v seznamu", seznam, "už je.")
    return

####################################################xxx
### DERIVACE ###
########################################################

def derivace_pref(zaklad,kat,zmena, pocet):
    """
    Řídicí část derivace prefixů.
    """
    # kat = S, Adj, Pro, Num, V, Adv, Pre, Kon,
    # zmena = adverb,
    # pocet - 1/2 - jednou půjde jen do první vrstvy, 2, se pokusí derivovat mnohem dál
    jmeno = zaklad
    # zapamatuje si základní slovo, s kterým začínal
    vystup = [jmeno]
    # vloží jej do výstupu
    is_in(vystup,(der_proces(zaklad,kat,zmena,jmeno)))
    for k in range(1,pocet):
        # chci vidět, jak to bude při opakování - do hloubky,
        # vygeneruje-li slovo nekonat => pryč s ním.
        # Vygeneruje slova dokonat =>
        # automaticky ho nechat projet to znova a vytvořit v hlubší vrstvě "nedokonat"
        # původně jsem měla while => s tím,
        # že se to mělo zastavit v podmínkách, ale ani ty nefungují
        if len(vystup) > 0:
            # občas záhadně vygeneroval výstup jako prázdný seznam, to tady má zahodit
            for i in vystup:
                # potřebuju vzít prvky seznamu a vytáhnout je jako string
                i = "".join(i)
                # abych je mohla hodit do sem,
                pomocna = der_proces(i,kat,zmena,jmeno)
                if pomocna is not None:
                    for item in pomocna:
                        # vložit do hlavního seznamu
                        is_in(vystup,pomocna)
    print (vystup)

def der_proces(zaklad,kat,zmena,jmeno):
    zaklad = str(zaklad)  # základ by měl být str, ale pro jistotu.
    derivat = str()
    vystup = []
    zacatek = zaklad[0]+zaklad[1]
    zacatek_3 = zaklad[0]+zaklad[1]+zaklad[2] # 1., 2. a 3. písmeno základu
    zacatek_j = jmeno[0]+jmeno[1]
    pokracovani = ""  # 3. a 4. písmeno
    if len(jmeno) > 4:
        pokracovani = zaklad[2]+zaklad[3]
    pokracovani2 = "" # 5. a 6. písmeno
    pokracovani_3 = "" # 3., 4., a 5. písmeno
    # následující seznamy kombinovat s podmínkou při delší derivaci takže, délka základu musí být větší než jména
    not_u2 = ["ne","vy","na","ná","za","zá","po"]
    not_u3 = ["nej","pro","vel","pře"]
    not_na12 = ["ne","na","ná","vy","za"]
    not_na22 = ["ne","na","ná","vy","za"]
    not_po2 = ["ne","ná","na"]
    not_do2 = ["ne","do"]
    #print (zacatek, "zacatek")
    if len(zaklad) > (len(jmeno)+1):
        # v případě, že chceme derivovat co nejdál, zastaví se to na
        #print(jmeno, zaklad, "ok")
        if (len(zaklad))-(len(jmeno)) > 3:
            pokracovani2 = zaklad[4]+zaklad[5]
            pokracovani_3 = zaklad[2]+zaklad[3]+zaklad[4]
    """ Zastaví se pokud: """
    if (len(zaklad) > (len(jmeno)+1)) and kat == "S":
        # aby nevznikala slova jako zaprůchod atd.
        return
    if len(zaklad) - len(jmeno) > 4:
        #možno změnit... zatím jen proto, aby se to někdy zastavilo,
        # nebude derivovat slova jako neprotiprávní apod.
        return
    if len(zaklad)< 2:  # 1 písmeno je opravdu nevalidní vstup
        return
    """ Samotná derivace """
    if kat == "S" and zaklad[-1] == "í":
        if zacatek != "ná":
        # městí => mění na náměstí
            derivat = na2(zaklad)
            is_in(vystup,derivat)
        return vystup
    if kat == "Adj" or kat == "Adv":
        # pokud je slovo adjektivum nebo adverbium
        if zaklad[-1] == "í" and zacatek_3 != "nej":
            if zacatek != "ne":
                derivat = negace(zaklad)
                derivat = nej(derivat)
                is_in(vystup,derivat)
            derivat = nej(zaklad)
            is_in(vystup,derivat)
            print (vystup, "nej")
        if zacatek_3 == "nej":
            print ("Dál už derivovat nelze")
            return zaklad, vystup
    if zacatek == "ne" and zacatek_j != "ne":
        if kat == "Adv" or (kat == "V" and zmena == "adverb"):
            derivat = negace(zaklad)
            derivat = do(derivat)
            is_in(vystup,derivat)
            #print (vystup,"adv/v+adverb")
        return
    if zacatek == "po" and pokracovani == "po":
        """ PO """
        return
    elif pokracovani== "po" and zacatek_j == "po":  #teoreticky, nutno ověřit
        return
    else:
        derivat = po(zaklad)
        is_in(vystup,derivat)
        ######################x
    if (zacatek not in not_do2 or zaklad[0] == "u") and pokracovani != "do":
        #print("jsem v ne do")
        """ DO """
        derivat = do(zaklad)
        is_in(vystup,derivat)
            #####################
    if zacatek not in not_na12 and pokracovani != "na":
        """ NA """
        derivat = na1(zaklad)
        #print (vystup,"na")
        is_in(vystup,derivat)
            #####################
    if zacatek not in not_na22 and pokracovani != "ná" and (kat == "S" or kat == "Adj" or kat == "Adv"):
        """ NÁ """
        derivat = na2(zaklad)
        is_in(vystup,derivat)
            #####################
    if zacatek != "vy" and pokracovani != "vy" and zaklad[0] != "u":
        """ VY """
        derivat = vy1(zaklad)
        is_in(vystup,derivat)
            #####################
    if zaklad [0] != "u" and (zacatek not in not_u2 and zacatek != zacatek_j):
        """ U """
        derivat = u(zaklad)
        is_in(vystup,derivat)
        if zaklad [0:4] == "ušnic":
            derivat = za1(zaklad)
            is_in(vystup,derivat)
    if kat != "V" and len(zaklad) == len(jmeno):
        """ PROTI """
        derivat = proti(zaklad)
        is_in(vystup,derivat)
    derivat = negace(zaklad)
    is_in(vystup,derivat)
    return vystup


# test_in("vykonat",derivace_pref("konat","V","",1))
derivace_pref("městí","S","",2)  # => zatím neřeším kořeny.
derivace_pref("výraznější","Adj","",1)
derivace_pref("chod","S","",2)
derivace_pref("konečna","Adv","",2)
derivace_pref("určit","V","",2)
#derivace_pref("nevidím","V","adverb")
derivace_pref("učit","V","",2)
#derivace_pref("ušnice","","")

