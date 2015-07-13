Hnízdování příbuzných slov v češtině
====================================

Cílem projektu je provázat slova a jejich odvozeniny.

Postupuje se od základního (fundujícího) slova k odvozeninám prostřednictvím
afixace s možnou palatalizací a alternací délky.

I přes znalost hláskového vývoje češtiny program slova tvoří procedurami
popisujícími slovotvorbu ze synchronního pohledu.

K čemu by se to hodilo? K automatické statistické analýze slovotvorných
tendencí s využitím korpusu: závisí třeba nějak distribuce tvrdého a měkkého
skloňování desubstantivních adjektiv typu -ný, -ní na základu? Šlo by vytvořit
všechny deriváty a pak si nechat rozpadnout základy podle zakončení, délky,
případně dalších ukazatelů.

Zpracované slovotvorné procesy
==============================

Substantiva
-----------

* konatelská jména typu houb-ař a ryb-ář, případně housl-ista
* přivlastňovací adjektiva od životných základů (ženská i mužská)
* adjektiva typu -ský
* adjektiva typu -ný, -ní
* přechylování (moce) opět od životných základů
* cirkumfixace typu ná-měst-í (s různými předponami)
* substantiva typu hvězd-ice (podobá se to -ík, ale pro feminina?)
* prefixace typu pra-otec, nepřítel, pa-blb, anti-hrdina

Adjektiva
---------

* adverbializace
* adverbializace prefixací (a přichýlením k jmennému skloňování)
* stupňování

  Tady není úplně jasné, jestli by se od stupňovaných podob taky neměly tvořit
  odpovídající adverbia. Mělo by to jen jednu nevýhodu – když by se přesunulo
  všechno stupňování sem, nešlo by přímo derivovat od adverbií. Jenže – existují
  vůbec doklady (Dle korpusu SYN2010 a vlastního porovnávacího kódu - mohu dodat data - bylo zjištěno, že dochází pouze k nepravidelnostem například u slov: raději - rád, dál, dále, déle, šíř, šíře. Asi jediné, co opravdu není od adjektiva je "dříve" a "dýl". Porovnávala jsem 3438 adjektiv v druhém stupni a prvním pádě a přes 67 tisíc lemmat adjektiv s přes 1600 adverbií v druhém stupni.), že by se stupňovala adverbia, která nemají svůj vzor
  v adjektivu? Pak by to bylo jasné, mohl bych to bez obav přesunout, protože
  v programu vždycky jdu jen směrem od fundujících slov k odvozený a stupňování
  adverbií to vlastně trochu kazí.
* imperfektiva typu tenč-i-t, ale i plaš-i-t (rozdílný posun významu) – mělo by
  být i od substantiv (za-koř-en-i-t)
* substantiva typu zed-n-ík
* substantiva typu rad-ost (haha, ne zrovna typickej příklad) stál-ý > stál-ost
* substantiva typu mělč-ina

Verba
-----

* prefixace

Adverbia
--------

Stupňování se prozatím řeší přímo u adverbií, ale pokud se nenajdou stupňovaná
adverbia, která nevznikla od adjektiv, pak bude vhodnější tvořit stupňované
tvary adverbií přímo od adjektiv.

Dál asi nic, od adverbií se už toho zřejmě moc netvoří.

Nezpracované, ale asi proveditelné procesy
==========================================

* desubstantiva typu škol-ák
* desubstantiva typu prasečí (nt-kmen -et-) – ale muší
* desubstantiva typu ok-at-ý, ale skal-n-at-ý
* deminutiva (prosťáček)
* jména mláďat
* deadjektiva typu -ota (drah-ota)
* deadjektiva typu velik-án
* deadjektiva typu stař-ec, hluš-ec
* deadjektiva typu stář-í
* slovesa s tématy -ova- (od substantiv a možná i adjektiv)
* deverbativa typu uč-i-tel, po-kuš-i-tel
* kořenová deverbativa typu (vaz? >) váz-a-t > vaz-ba (root-derivates)
* kol-mo, koň-mo
* led-ov-ý

(Ne)řešené problémy
===================

Měkčení (palatalizace)
----------------------

Procesy jako adverbializace dobrý > dobře se řeší lepením koncovky -ě ke kmeni
dobr-. Všechny morfémy si slovní tvar zachovává v původní podobě, ale zároveň
si vytvoří výslednou „povrchovou“ podobu tak, že spojí morfémy za sebe
(prefixy, kořen, sufixy, koncovku) a nechá nahradit hloubkovou morfematickou
reprezenaci „rě“ za „ře“.

    dobry = Adjektivum(lemma='dobrý')  # automaticky se odtrhne -ý
    dobre = Adverbium(dobry, koncovka='ě')  # spojí morfémy a upraví pravopis

Alternace vokalické délky v základu
-----------------------------------

V některých případech se základ krátí, jindy dlouží. Není vždy jasné, která
varianta základu je bezpříznaková. Třeba příklad
    kůň (koně, …) > koňský
se dá brát i tak, že v lemmatu se dlouží základ „koň“.

Ablaut
------

Synchronně je zřejmě vhodné řešit výjimkami anebo vhodným příznakem (o jaký
stupeň ablautu – redukovaný, o-ový, e-ový, dloužený – jde).

    vést > zá-vod

Alternace e s nulou
-------------------

V případě základu to může být to samé, anebo důsledek zániku jerů.
V zakončeních kdo ví. Výjimky budou asi potřeba, pokud se nenajde nějaká
pravidelnost. Anebo dva/víc kmenů.

    zeď > zd-í-t
