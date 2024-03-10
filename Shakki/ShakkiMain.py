import pygame as p
import ShakkiMoottori, ShakkiAI
import sys
from multiprocessing import Process, Queue

LAUTA_LEVEYS = LAUTA_KORKEUS = 512
SIIRTO_LOKI_PANEELI_LEVEYS = 250
SIIRTO_LOKI_PANEELI_KORKEUS = LAUTA_KORKEUS
ULOTTUVUUS = 8
RUUTU_KOKO = LAUTA_KORKEUS // ULOTTUVUUS
MAX_FPS = 15
KUVAT = {}


def lataaKuvat():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        KUVAT[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (RUUTU_KOKO, RUUTU_KOKO))


def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init()
    naytto = p.display.set_mode((LAUTA_LEVEYS + SIIRTO_LOKI_PANEELI_LEVEYS, LAUTA_KORKEUS))
    kello = p.time.Clock()
    naytto.fill(p.Color("white"))
    pelitila = ShakkiMoottori.PeliTila()
    laillisetSiirrot = pelitila.haeLaillisetSiirrot()
    siirtoTehty = False  # flag variable for when a siirto is made
    animoi = False  # flag variable for when we should animoi a siirto
    lataaKuvat()  # do this only once before while loop
    kaynnissa = True
    ruutuValittu = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(rivi,linja))
    pelaajaKlikit = []  # this will keep track of player clicks (two tuples)
    peliLoppu = False
    aiAjattelee = False
    siirtoKumottu = False
    siirtoHakijaProsessi = None
    siirtoLokiFontti = p.font.SysFont("Arial", 14, False, False)
    pelaaja1 = False  # if a human is playing white, then this will be True, else False
    pelaaja2 = True  # if a hyman is playing white, then this will be True, else False

    while kaynnissa:
        ihmisenVuoro = (pelitila.valkoiseSiirto and pelaaja1) or (not pelitila.valkoiseSiirto and pelaaja2)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not peliLoppu:
                    sijainti = p.mouse.get_pos()  # (x, y) sijainti of the mouse
                    linja = sijainti[0] // RUUTU_KOKO
                    rivi = sijainti[1] // RUUTU_KOKO
                    if ruutuValittu == (rivi, linja) or linja >= 8:  # user clicked the same square twice
                        ruutuValittu = ()  # deselect
                        pelaajaKlikit = []  # clear clicks
                    else:
                        ruutuValittu = (rivi, linja)
                        pelaajaKlikit.append(ruutuValittu)  # append for both 1st and 2nd click
                    if len(pelaajaKlikit) == 2 and ihmisenVuoro:  # after 2nd click
                        siirto = ShakkiMoottori.Siirto(pelaajaKlikit[0], pelaajaKlikit[1], pelitila.lauta)
                        for i in range(len(laillisetSiirrot)):
                            if siirto == laillisetSiirrot[i]:
                                pelitila.teeSiirto(laillisetSiirrot[i])
                                siirtoTehty = True
                                animoi = True
                                ruutuValittu = ()  # reset user clicks
                                pelaajaKlikit = []
                        if not siirtoTehty:
                            pelaajaKlikit = [ruutuValittu]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    pelitila.kumoaSiirto()
                    siirtoTehty = True
                    animoi = False
                    peliLoppu = False
                    if aiAjattelee:
                        siirtoHakijaProsessi.terminate()
                        aiAjattelee = False
                    siirtoKumottu = True
                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    pelitila = ShakkiMoottori.PeliTila()
                    laillisetSiirrot = pelitila.haeLaillisetSiirrot()
                    ruutuValittu = ()
                    pelaajaKlikit = []
                    siirtoTehty = False
                    animoi = False
                    peliLoppu = False
                    if aiAjattelee:
                        siirtoHakijaProsessi.terminate()
                        aiAjattelee = False
                    siirtoKumottu = True

        # AI siirto finder
        if not peliLoppu and not ihmisenVuoro and not siirtoKumottu:
            if not aiAjattelee:
                aiAjattelee = True
                palaaJonoon = Queue()  # used to pass data between threads
                siirtoHakijaProsessi = Process(target=ShakkiAI.haeParasSiirto, args=(pelitila, laillisetSiirrot, palaaJonoon))
                siirtoHakijaProsessi.start()

            if not siirtoHakijaProsessi.is_alive():
                aiSiirto = palaaJonoon.get()
                if aiSiirto is None:
                    aiSiirto = ShakkiAI.etsiRandomSiirto(laillisetSiirrot)
                pelitila.teeSiirto(aiSiirto)
                siirtoTehty = True
                animoi = True
                aiAjattelee = False

        if siirtoTehty:
            if animoi:
                animoiSiirto(pelitila.siirtoLoki[-1], naytto, pelitila.lauta, kello)
            laillisetSiirrot = pelitila.haeLaillisetSiirrot()
            siirtoTehty = False
            animoi = False
            siirtoKumottu = False

        piirraPelitila(naytto, pelitila, laillisetSiirrot, ruutuValittu)

        if not peliLoppu:
            piirraSiirtoLoki(naytto, pelitila, siirtoLokiFontti)

        if pelitila.shakkimatti:
            peliLoppu = True
            if pelitila.valkoiseSiirto:
                piirraLopetusTeksti(naytto, "Black wins by checkmate")
            else:
                piirraLopetusTeksti(naytto, "White wins by checkmate")

        elif pelitila.pattitilanne:
            peliLoppu = True
            piirraLopetusTeksti(naytto, "Stalemate")

        kello.tick(MAX_FPS)
        p.display.flip()


def piirraPelitila(naytto, pelitila, laillisetSiirrot, ruutuValittu):
    """
    Responsible for all the graphics within current game state.
    """
    piirraLauta(naytto)  # draw squares on the board
    korostaRuudut(naytto, pelitila, laillisetSiirrot, ruutuValittu)
    piirraNappulat(naytto, pelitila.lauta)  # draw pieces on top of those squares


def piirraLauta(naytto):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global varit
    varit = [p.Color("white"), p.Color("gray")]
    for rivi in range(ULOTTUVUUS):
        for linja in range(ULOTTUVUUS):
            color = varit[((rivi + linja) % 2)]
            p.draw.rect(naytto, color, p.Rect(linja * RUUTU_KOKO, rivi * RUUTU_KOKO, RUUTU_KOKO, RUUTU_KOKO))


def korostaRuudut(naytto, pelitila, laillisetSiirrot, ruutuValittu):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(pelitila.siirtoLoki)) > 0:
        viimeSiirto = pelitila.siirtoLoki[-1]
        s = p.Surface((RUUTU_KOKO, RUUTU_KOKO))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        naytto.blit(s, (viimeSiirto.lopetusLinja * RUUTU_KOKO, viimeSiirto.lopetusRivi * RUUTU_KOKO))
    if ruutuValittu != ():
        rivi, linja = ruutuValittu
        if pelitila.lauta[rivi][linja][0] == (
                'w' if pelitila.valkoiseSiirto else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((RUUTU_KOKO, RUUTU_KOKO))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            naytto.blit(s, (linja * RUUTU_KOKO, rivi * RUUTU_KOKO))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for siirto in laillisetSiirrot:
                if siirto.aloitusRivi == rivi and siirto.aloitusLinja == linja:
                    naytto.blit(s, (siirto.lopetusLinja * RUUTU_KOKO, siirto.lopetusRivi * RUUTU_KOKO))


def piirraNappulat(naytto, lauta):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for rivi in range(ULOTTUVUUS):
        for linja in range(ULOTTUVUUS):
            nappula = lauta[rivi][linja]
            if nappula != "--":
                naytto.blit(KUVAT[nappula], p.Rect(linja * RUUTU_KOKO, rivi * RUUTU_KOKO, RUUTU_KOKO, RUUTU_KOKO))


def piirraSiirtoLoki(naytto, pelitila, fontti):
    """
    Draws the move log.

    """
    siirtoLokiNelio = p.Rect(LAUTA_LEVEYS, 0, SIIRTO_LOKI_PANEELI_LEVEYS, SIIRTO_LOKI_PANEELI_KORKEUS)
    p.draw.rect(naytto, p.Color('black'), siirtoLokiNelio)
    siirtoLoki = pelitila.siirtoLoki
    siirtoTekstit = []
    for i in range(0, len(siirtoLoki), 2):
        siirtoMerkkijono = str(i // 2 + 1) + '. ' + str(siirtoLoki[i]) + " "
        if i + 1 < len(siirtoLoki):
            siirtoMerkkijono += str(siirtoLoki[i + 1]) + "  "
        siirtoTekstit.append(siirtoMerkkijono)

    siirrotPerRivi = 3
    tayte = 5
    rivivali = 2
    tekstiY = tayte
    for i in range(0, len(siirtoTekstit), siirrotPerRivi):
        teksti = ""
        for j in range(siirrotPerRivi):
            if i + j < len(siirtoTekstit):
                teksti += siirtoTekstit[i + j]

        tekstiObjekti = fontti.render(teksti, True, p.Color('white'))
        tekstiSijainti = siirtoLokiNelio.move(tayte, tekstiY)
        naytto.blit(tekstiObjekti, tekstiSijainti)
        tekstiY += tekstiObjekti.get_height() + rivivali


def piirraLopetusTeksti(naytto, teksti):
    fontti = p.font.SysFont("Helvetica", 32, True, False)
    tekstiObjekti = fontti.render(teksti, False, p.Color("gray"))
    tekstiSijainti = p.Rect(0, 0, LAUTA_LEVEYS, LAUTA_KORKEUS).move(LAUTA_LEVEYS / 2 - tekstiObjekti.get_width() / 2,
                                                                   LAUTA_KORKEUS / 2 - tekstiObjekti.get_height() / 2)
    naytto.blit(tekstiObjekti, tekstiSijainti)
    tekstiObjekti = fontti.render(teksti, False, p.Color('black'))
    naytto.blit(tekstiObjekti, tekstiSijainti.move(2, 2))


def animoiSiirto(siirto, naytto, lauta, kello):
    """
    Animating a move
    """
    global varit
    sRivi = siirto.lopetusRivi - siirto.aloitusRivi
    sLinja = siirto.lopetusLinja - siirto.aloitusLinja
    framesPerNelio = 10  # frames to move one square
    frameMaara = (abs(sRivi) + abs(sLinja)) * framesPerNelio
    for frame in range(frameMaara + 1):
        rivi, linja = (siirto.aloitusRivi + sRivi * frame / frameMaara, siirto.aloitusLinja + sLinja * frame / frameMaara)
        piirraLauta(naytto)
        piirraNappulat(naytto, lauta)
        # erase the piece moved from its ending square
        vari = varit[(siirto.lopetusRivi + siirto.lopetusLinja) % 2]
        lopetusRuutu = p.Rect(siirto.lopetusLinja * RUUTU_KOKO, siirto.lopetusRivi * RUUTU_KOKO, RUUTU_KOKO, RUUTU_KOKO)
        p.draw.rect(naytto, vari, lopetusRuutu)
        # draw captured piece onto rectangle
        if siirto.syotyNappula != '--':
            if siirto.onEnpassantSiirto:
                enpassantRivi = siirto.lopetusRivi + 1 if siirto.syotyNappula[0] == 'b' else siirto.lopetusRivi - 1
                lopetusRuutu = p.Rect(siirto.lopetusLinja * RUUTU_KOKO, enpassantRivi * RUUTU_KOKO, RUUTU_KOKO, RUUTU_KOKO)
            naytto.blit(KUVAT[siirto.syotyNappula], lopetusRuutu)
        # draw moving piece
        naytto.blit(KUVAT[siirto.siirrettyNappula], p.Rect(linja * RUUTU_KOKO, rivi * RUUTU_KOKO, RUUTU_KOKO, RUUTU_KOKO))
        p.display.flip()
        kello.tick(60)


if __name__ == "__main__":
    main()
