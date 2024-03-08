import random

nappulaArvot = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
SHAKKIMATTI = 1000
PATTITILANNE = 0
SYVYYS = 2


def etsiRandomSiirto(laillisetSiirrot):
   return laillisetSiirrot[random.randint(0, len(laillisetSiirrot) - 1)]

def etsiParasSiirto(pelitila, laillisetSiirrot):
    vuoroKerroin = 1 if pelitila.valkoisenSiirto else -1
    vastustajanMinMaxPisteet = SHAKKIMATTI
    parasPelaajaSiirto = None
    random.shuffle(laillisetSiirrot)
    for pelaajaSiirto in laillisetSiirrot:
        pelitila.teeSiirto(pelaajaSiirto)
        vastustajanSiirrot = pelitila.haeLaillisetSiirrot()
        if pelitila.pattitilanne:
            vastustajanMaksimiPisteet = PATTITILANNE
        elif pelitila.shakkimatti:
            vastustajanMaksimiPisteet = -SHAKKIMATTI
        else:
            vastustajanMaksimiPisteet = -SHAKKIMATTI
            for vastustajanSiirrot in vastustajanSiirrot:
                pelitila.teeSiirto(vastustajanSiirrot)
                pelitila.haeLaillisetSiirrot()
                if pelitila.shakkimatti:
                    pisteet = -vuoroKerroin * SHAKKIMATTI
                elif pelitila.pattitilanne:
                    pisteet = PATTITILANNE
                else:
                    pisteet = -vuoroKerroin * pisteytaResurssit(pelitila.lauta)
                if pisteet > vastustajanMaksimiPisteet:
                    vastustajanMaksimiPisteet = pisteet
                pelitila.kumoaSiirto()
            if vastustajanMaksimiPisteet < vastustajanMinMaxPisteet:
                vastustajanMinMaxPisteet = vastustajanMaksimiPisteet
                parasPelaajaSiirto = pelaajaSiirto
            pelitila.kumoaSiirto()
    return parasPelaajaSiirto

def etsiParasSiirtoMinMax(pelitila, laillisetSiirrot):
    global seuraavaSiirto
    seuraavaSiirto = None
    etsiSiirtoMinMax(pelitila, laillisetSiirrot, SYVYYS, pelitila.valkoisenSiirto)
    return seuraavaSiirto

def etsiSiirtoMinMax(pelitila, laillisetSiirrot, syvyys, valkoisenVuoro):
    global seuraavaSiirto
    if syvyys == 0:
        return pisteytaResurssit(pelitila.lauta)

    if valkoisenVuoro:
        maksimiPisteet = -SHAKKIMATTI
        for siirto in laillisetSiirrot:
            pelitila.teeSiirto(siirto)
            seuraavaSiirto = pelitila.haeLaillisetSiirrot()
            pisteet = etsiSiirtoMinMax(pelitila, seuraavaSiirto, syvyys -1, False)
            if pisteet > maksimiPisteet:
                maksimiPisteet = pisteet
                if syvyys == SYVYYS:
                    seuraavaSiirto = siirto
            pelitila.kumoaSiirto()
        return maksimiPisteet

    else:
        minimiPisteet = SHAKKIMATTI
        for siirto in laillisetSiirrot:
            pelitila.teeSiirto()
            seuraavaSiirto = pelitila.haeLaillisetSiirrot()
            pisteet = etsiSiirtoMinMax(pelitila, seuraavaSiirto, syvyys - 1, True)
            if pisteet > minimiPisteet:
                minimiPisteet = pisteet
                if syvyys == SYVYYS:
                    seuraavaSiirto = siirto
            pelitila.kumoaSiirto()
        return minimiPisteet


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

