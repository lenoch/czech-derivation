import logging

# from desubstantiva import desubstantiva
from deadjektiva import deadjektiva


def derivace(lemma, atributy, vyznamy=set()):
    slovni_druh = atributy.get('k')  # kind, slovní druh, part of speech (POS)
    if slovni_druh is None:
        raise ValueError('Nezadaný slovní druh pro ' + str(lemma))

    if slovni_druh == '2':
        return deadjektiva(lemma, atributy, vyznamy)
    else:
        logging.info('Nepodporovaný slovní druh: %s (%s)', slovni_druh, lemma)


def test():
    pokusy = [
        ('dobrý', dict(k='2', d='1')),  # starý → starší
        ('pěkný', dict(k='2', d='1')),
        ('horší', dict(k='2', d='2')),
    ]

    for lemma, atributy in pokusy:
        print(lemma, zformatovat_atributy(atributy))

        for derivat, atributy_derivatu, vyznamy_derivatu in derivace(
                lemma, atributy):
            print(derivat, zformatovat_atributy(atributy_derivatu),
                  ' '.join(vyznamy_derivatu))
        print('\n')


def zformatovat_atributy(atributy):
    return ' '.join(atribut + '=' + hodnota for atribut, hodnota
                    in sorted(atributy.items()))


if __name__ == '__main__':
    test()
