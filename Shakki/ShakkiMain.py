import pygame as p
import ShakkiMoottori

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def lataaKuvat():
    nappulat = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for nappula in nappulat:
        IMAGES[nappula] = p.transform.scale(p.image.load("images/" + nappula + ".png"),(SQ_SIZE,SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    kello = p.time.Clock()
    screen.fill(p.Color("white"))
    pelitila = ShakkiMoottori.PeliTila()
    laillisetSiirrot = pelitila.haeLaillisetSiirrot()
    siirtoTehty = False #Lippu muuttuja, jota käytetään kun siirto tehdään

    lataaKuvat()
    kaynnissa = True
    valittuRuutu = () #Pitää kirjaa mihin pelaaja clikkasi viimeksi. tuple (rivi, linja)
    pelaajaKlikit = [] #Pitää kirjaa pelaajan klikeistä[(4,4), (3,4)]

    while kaynnissa:
        for e in p.event.get():
            if e.type == p.QUIT:
                kaynnissa = False

            #Hiiri handler
            elif e.type == p.MOUSEBUTTONDOWN:
                sijainti = p.mouse.get_pos()
                linja = sijainti[0]//SQ_SIZE
                rivi = sijainti[1]//SQ_SIZE
                if valittuRuutu == (rivi, linja): #käyttäjä clikkasi samaa ruutua kahdesti, jotta voi undo liikkeitä
                    valittuRuutu = () #poistaa valinnan
                    pelaajaKlikit = []
                else:
                    valittuRuutu = (rivi, linja)
                    pelaajaKlikit.append(valittuRuutu) #append molemille 1. ja 2. klikille.
                if len(pelaajaKlikit) == 2: #toisen klikin jälkeen.
                    siirto = ShakkiMoottori.Siirto(pelaajaKlikit[0], pelaajaKlikit[1], pelitila.lauta)
                    print(siirto.haeShakkiNotaatio())
                    for i in range(len(laillisetSiirrot)):
                        if siirto == laillisetSiirrot[i]:
                            pelitila.teeSiirto(laillisetSiirrot[i])
                            siirtoTehty = True
                            valittuRuutu = ()  # Resettaa klikit
                            pelaajaKlikit = []
                    if not siirtoTehty:
                        pelaajaKlikit = [valittuRuutu]

            #Näppäin Handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    pelitila.kumoaSiirto()
                    siirtoTehty = True

        if siirtoTehty:
            laillisetSiirrot = pelitila.haeLaillisetSiirrot()
            siirtoTehty = False

        piirraPeliTila(screen, pelitila)
        kello.tick(MAX_FPS)
        p.display.flip()

def piirraPeliTila(screen, pelitila):
    piirraRuutu(screen)
    piirraNappulat(screen, pelitila.lauta)

def piirraRuutu(screen):
    varit = [p.Color("white"), p.Color("dark green")]
    for rivi in range(DIMENSION):
        for linja in range(DIMENSION):
            vari = varit[((rivi + linja) % 2)]
            p.draw.rect(screen, vari, p.Rect(linja*SQ_SIZE, rivi*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def piirraNappulat(screen, lauta):
    for rivi in range(DIMENSION):
        for linja in range(DIMENSION):
            nappula = lauta[rivi][linja]
            if nappula != "--":
                screen.blit(IMAGES[nappula], p.Rect(linja*SQ_SIZE, rivi*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()