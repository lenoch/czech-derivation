from itertools import chain
# import logging

from upravy import uprava_pravopisu


def deadjektiva(lemma, atributy, vyznamy):
    return chain(
        stupnovani(lemma, dict(atributy), set(vyznamy)),
        mladost(lemma, dict(atributy), set(vyznamy)),
    )


def stupnovani(lemma, atributy, vyznamy):
    stupen = atributy.get('d')  # degree, stupeň
    if stupen is None:
        raise ValueError('Nezadaný stupeň pro ' + str(lemma))
    elif stupen == '1':
        if lemma.endswith('ý'):
            komparativ = uprava_pravopisu(lemma[:-1] + 'ější')
            atributy['d'] = '2'
            yield (komparativ, atributy, vyznamy)
            for vysledek in stupnovani(komparativ, atributy, vyznamy):
                yield vysledek
    elif stupen == '2':
        atributy['d'] = '3'
        yield ('nej' + lemma, atributy, vyznamy)

def mladost(lemma, atributy, vyznamy):
    if atributy.get('d') == '1' and lemma.endswith('ý'):
        del atributy['d']
        atributy.update(k='1', g='F')  # genus, jmenný rod
        yield lemma[:-1] + 'ost', atributy, vyznamy
        
def adverbializace(lemma, atributy, vyznamy):
    zmeny=[('dý','dě'),('rý','ře'),('bý','bě'),('vý','vě'),('mý','mě'),\
    ('sý','se'),('pý','pě'),('tý','tě'),('lý','le'),('ný','ně'),('ní','ně'),\
    ('chý','še'),('hý','ze'),('ský','sky'),('cký','cky'),('ký','ce')]  
    
    if atributy.get('d') ==  '1':
        atributy['k'] = '6'     
        yield lemma[:-1] + 'o', atributy, vyznamy
        
        #Kvůli ský/cký/chý používám dva cykly. 
        #První na rozeznávání posledních tří znaků, druhý na poslední dva znaky
        #Do pravidla se v kazdem cyklu ulozi nektera z dvojic ve zmenach
        
        for pravidla in zmeny:
            if lemma[len(lemma)-3:] in pravidla:
                yield lemma[:len(lemma)-3] + pravidla[1], atributy, vyznamy
                break  
            
                #Breakuju kvůli pravidlům na "ký" a "hý", která se znovu aplikovala 
                #i pro na už jednou zpracovaná "cký/ský" popř. "chý"
            
            else:
                if lemma[len(lemma)-2:] in pravidla: 
                    yield lemma[:-2] + pravidla[1], atributy, vyznamy    
