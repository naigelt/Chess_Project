import random

nappulaArvot = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
SHAKKIMATTI = 1000
PATTITILANNE = 0
SYVYYS = 2


def etsiRandomSiirto(laillisetSiirrot):
   return laillisetSiirrot[random.randint(0, len(laillisetSiirrot) - 1)]

def etsiParasSiirto(pelitila, laillisetSiirrot):
    global seuraavaSiirto
    seuraavaSiirto = None
    random.shuffle(laillisetSiirrot)
    etsiSiirtoNegaMaxAlphaBeta(pelitila, laillisetSiirrot, SYVYYS, -SHAKKIMATTI, SHAKKIMATTI, 1 if pelitila.valkoisenSiirto else -1)
    return seuraavaSiirto


def etsiSiirtoNegaMaxAlphaBeta(pelitila, laillisetSiirrot, syvyys, alpha, beta, siirtoKerroin):
    global seuraavaSiirto
    if syvyys == 0:
        return siirtoKerroin * pisteTaulu(pelitila)

    # siirto järjestäminen -
    maksimiPisteet = -SHAKKIMATTI
    for siirto in laillisetSiirrot:
        pelitila.teeSiirto(siirto)
        seuraavaSiirto = pelitila.haeLaillisetSiirrot()
        pisteet = -etsiSiirtoNegaMaxAlphaBeta(pelitila, seuraavaSiirto, syvyys - 1, -beta, -alpha, -siirtoKerroin)
        if pisteet > maksimiPisteet:
            maksimiPisteet = pisteet
            if syvyys == SYVYYS:
                seuraavaSiirto = siirto
        pelitila.kumoaSiirto()
        if maksimiPisteet > alpha: #karsiminen tässä
            alpha = maksimiPisteet
        if alpha >= beta:
            break
    return maksimiPisteet

#Postiiviset pisteet ovat hyvä valkoiselle, negatiiviset hyvä mustalle
def pisteTaulu(pelitila):
    if pelitila.shakkimatti:
        if pelitila.valkoisenSiirto:
            return -SHAKKIMATTI # musta voittaa
        else:
            return SHAKKIMATTI #Valkoinen voittaa
    elif pelitila.pattitilanne:
        return PATTITILANNE


    pisteet = 0
    for rivi in pelitila.lauta:
        for ruutu in rivi:
            if ruutu[0] == 'w':
                pisteet += nappulaArvot[ruutu[1]]
            elif ruutu[0] == 'b':
                pisteet -= nappulaArvot[ruutu[1]]
    return pisteet

def pisteytaResurssit(lauta):
    pisteet = 0
    for rivi in lauta:
        for ruutu in rivi:
            if ruutu[0] == 'w':
                pisteet += nappulaArvot[ruutu[1]]
            elif ruutu[0] == 'b':
                pisteet -= nappulaArvot[ruutu[1]]

    return pisteet

