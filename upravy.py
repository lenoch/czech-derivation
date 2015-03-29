import re


def uprava_pravopisu(slovo):
    if 'rě' in slovo:
        return re.sub('rě', 'ře', slovo)
    else:
        return slovo
