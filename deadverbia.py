#Jsem lama a nejde mi importovat promenná "zmeny" z deadjektiv.

#Odvozování adverbií na základě prefixace a sufixace, na další jsem zatím nenarazil
def adv_derivace(lemma, atributy, vyznamy,zmeny):
        if lemma.endswith('o'): 
            yield 'na' + lemma, atributy, vyznamy
            
        for pravidla in zmeny: 
            #Nejdřív používám rozeznávání posledních třech znaků kvůli případu chý/hý
            if lemma[len(lemma)-3:] in pravidla:
                lemma = lemma[:-3] + pravidla[0]
                yield 'do' + lemma[:-1] + 'a', atributy, vyznamy
                
                if lemma[0] == 'z' or lemma[0] == 's': 
                    yield 'ze' + lemma[:-1] + 'a', atributy, vyznamy
                    
                else: 
                    yield 'z' + lemma[:-1] + 'a', atributy, vyznamy
                    
                yield 'na' + lemma[:-1] + 'o', atributy, vyznamy
                break 
                    
            else:
                if lemma[len(lemma)-2:] in pravidla:
                    lemma = lemma[:-2] + pravidla[0]
                    yield 'do' + lemma[:-1] + 'a', atributy, vyznamy
                    if lemma[0] == 'z' or lemma[0] == 's': 
                        yield 'ze' + lemma[:-1] + 'a', atributy, vyznamy
                        
                    else: 
                        yield 'z' + lemma[:-1] + 'a', atributy, vyznamy
                        
                    yield 'na' + lemma[:-1] + 'o', atributy, vyznamy
                    break
            
def adv_stupnovani(lemma, atributy, vyznamy):
    if atributy.get('d') == '1':
        #Kvůli množství (snad všech) výjimek níže, které mají více variant, jsem udělal komparativ jako seznam
        komparativ=[]
        atributy['d'] = '2'
        if lemma=='dobře': 
            komparativ = ['lépe', 'líp']  
            
        elif lemma=='zle' or lemma=='špatně': 
            komparativ = ['hůře', 'hůř']
            
        elif lemma=='brzy': 
            komparativ = ['dříve', 'dřív']
            
        elif lemma=='dlouze' or lemma=='dlouho': 
            komparativ = ['déle']
        
        elif lemma=='vysoce' or lemma=='vysoko': 
            komparativ = ['výš', 'výše']
            
        elif lemma=='málo': 
            komparativ = ['méně', 'míň']
            
        elif lemma=='těžko' or lemma=='těžce': 
            komparativ = ['tíže', 'tíž']
            
        elif lemma=='snadno' or lemma=='snadně': 
            komparativ = ['snáze', 'snáz', 'snadněji']
            
        elif lemma=='hluboko' or lemma=='hluboce': 
            komparativ = ['hloub', 'blouběji']
            
        elif lemma=='široko' or lemma=='široce': 
            komparativ = ['šíře', 'šíř', 'šířeji']
            
        elif lemma=='úzko' or lemma=='úzce': 
            komparativ = ['úže', 'úžeji']
                
        else:
            if lemma.endswith('ce'): 
                komparativ.append(lemma[:-2] + 'čeji')
                
            elif lemma.endswith('cky'): 
                komparativ.append(lemma[:-3] + 'čtěji')
                
            elif lemma.endswith('sky'): 
                komparativ.append(lemma[:-3] + 'štěji')
                
            elif lemma.endswith('e') or lemma.endswith('ě'): 
                komparativ.append(lemma + 'ji')

         for slovo in komparativ:
            yield slovo, atributy, vyznamy

    if atributy.get('d') == '2':
        atributy['d'] = '3'
        #Pokud nedošlo ke koverzi z 1. stupně, tak se za komparativ vezme vstupní slovo
        if len(komparativ) == 0: 
            komparativ.append(lemma)  
            
        for slovo in komparativ:
            yield 'nej' + slovo, atributy, vyznamy    
    
