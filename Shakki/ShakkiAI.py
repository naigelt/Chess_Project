"""
Handling the AI moves.
"""
import random

nappulaArvo = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knightArvot = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
               [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
               [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
               [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
               [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
               [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
               [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
               [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

lahettiArvot = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

torniArvot = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
              [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
              [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
              [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
              [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
              [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
              [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
              [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

kuningatarArvot = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                   [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                   [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                   [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                   [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                   [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                   [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                   [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

sotilasArvot = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

nappulaSijaintiArvo = {"wN": knightArvot,
                         "bN": knightArvot[::-1],
                         "wB": lahettiArvot,
                         "bB": lahettiArvot[::-1],
                         "wQ": kuningatarArvot,
                         "bQ": kuningatarArvot[::-1],
                         "wR": torniArvot,
                         "bR": torniArvot[::-1],
                         "wp": sotilasArvot,
                         "bp": sotilasArvot[::-1]}

SHAKKIMATTI = 1000
PATTITILANNE = 0
SYVYYS = 3


def haeParasSiirto(pelitila, laillisetSiirrot, palaaJonoon):
    global seuraavaSiirto
    seuraavaSiirto = None
    random.shuffle(laillisetSiirrot)
    haeSiirtoNegaMaxAlphaBeta(pelitila, laillisetSiirrot, SYVYYS, -SHAKKIMATTI, SHAKKIMATTI,
                              1 if pelitila.valkoiseSiirto else -1)
    palaaJonoon.put(seuraavaSiirto)


def haeSiirtoNegaMaxAlphaBeta(pelitila, laillisetSiirrot, syvyys, alpha, beta, vuoroKerroin):
    global seuraavaSiirto
    if syvyys == 0:
        return vuoroKerroin * pisteTaulu(pelitila)
    maksimiPisteet = -SHAKKIMATTI
    for siirto in laillisetSiirrot:
        pelitila.teeSiirto(siirto)
        seuraavaSiirto = pelitila.haeLaillisetSiirrot()
        pisteet = -haeSiirtoNegaMaxAlphaBeta(pelitila, seuraavaSiirto, syvyys - 1, -beta, -alpha, -vuoroKerroin)
        if pisteet > maksimiPisteet:
            maksimiPisteet = pisteet
            if syvyys == SYVYYS:
                seuraavaSiirto = siirto
        pelitila.kumoaSiirto()
        if maksimiPisteet > alpha:
            alpha = maksimiPisteet
        if alpha >= beta:
            break
    return maksimiPisteet


def pisteTaulu(pelitila):
    """
    Score the board. A positive pisteet is good for white, a negative pisteet is good for black.
    """
    if pelitila.shakkimatti:
        if pelitila.valkoiseSiirto:
            return -SHAKKIMATTI  # black wins
        else:
            return SHAKKIMATTI  # white wins
    elif pelitila.pattitilanne:
        return PATTITILANNE
    pisteet = 0
    for rivi in range(len(pelitila.lauta)):
        for linja in range(len(pelitila.lauta[rivi])):
            nappula = pelitila.lauta[rivi][linja]
            if nappula != "--":
                nappulanSijaintiArvo = 0
                if nappula[1] != "K":
                    nappulanSijaintiArvo = nappulaSijaintiArvo[nappula][rivi][linja]
                if nappula[0] == "w":
                    pisteet += nappulaArvo[nappula[1]] + nappulanSijaintiArvo
                if nappula[0] == "b":
                    pisteet -= nappulaArvo[nappula[1]] + nappulanSijaintiArvo

    return pisteet


def etsiRandomSiirto(laillisetSiirrot):
    """
    Picks and returns a random valid move.
    """
    return random.choice(laillisetSiirrot)