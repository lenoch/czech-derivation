Hnízdování příbuzných slov v češtině
====================================

Cílem projektu je provázat slova a jejich odvozeniny.

Postupuje se od základního (fundujícího) slova k odvozeným tvarům
prostřednictvím afixace.

I přes znalost hláskového vývoje češtiny program slova tvoří procedurami
popisujícími slovotvorbu ze synchronního pohledu.

Zpracované slovotvorné procesy
==============================

Substantiva
-----------

Adjektiva
---------

Verba
-----

Adverbia
--------

Stupňování se prozatím řeší přímo u adverbií, ale pokud se nenajdou stupňovaná
adverbia, která nevznikla od adjektiv, pak bude vhodnější tvořit stupňované
tvary adverbií přímo od adjektiv.

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

Ablaut
------

Synchronně je zřejmě vhodné řešit výjimkami.

Alternace e s nulou
-------------------

Podobně (pokud se v některých případech nenajde nějaká pravidelnost).
