import pygame as p
import ShakkiMoottori, ShakkiAI

LAUTA_LEVEYS = LAUTA_KORKEUS = 512
SIIRTO_LOKI_PANEELI_LEVEYS = 250
SIIRTO_LOKI_PANEELI_KORKEUS = LAUTA_KORKEUS
DIMENSION = 8
SQ_SIZE = LAUTA_KORKEUS // DIMENSION
MAX_FPS = 15
IMAGES = {}

def lataaKuvat():
    nappulat = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for nappula in nappulat:
        IMAGES[nappula] = p.transform.scale(p.image.load("images/" + nappula + ".png"),(SQ_SIZE,SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((LAUTA_LEVEYS + SIIRTO_LOKI_PANEELI_LEVEYS, LAUTA_KORKEUS))
    kello = p.time.Clock()
    screen.fill(p.Color("white"))
    siirtoLokiFontti = p.font.SysFont("Arial", 14, False, False)
    pelitila = ShakkiMoottori.PeliTila()
    laillisetSiirrot = pelitila.haeLaillisetSiirrot()
    siirtoTehty = False #Lippu muuttuja, jota käytetään kun siirto tehdään
    animoi = False # Lippu muuttuja

    lataaKuvat()
    kaynnissa = True
    valittuRuutu = () #Pitää kirjaa mihin pelaaja clikkasi viimeksi. tuple (r, l)
    pelaajaKlikit = [] #Pitää kirjaa pelaajan klikeistä[(4,4), (3,4)]
    peliLoppu = False
    pelaaja1 = True #Jos ihminen pelaa valkoista, tämä on True. Jos Ai pelaa valkoista niin tämä on False
    pelaaja2 = False # Sama mutta mustalle
    while kaynnissa:
        ihmisenVuoro = (pelitila.valkoisenSiirto and pelaaja1) or (not pelitila.valkoisenSiirto and pelaaja2)
        for e in p.event.get():
            if e.type == p.QUIT:
                kaynnissa = False

            #Hiiri handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not peliLoppu and ihmisenVuoro:
                    sijainti = p.mouse.get_pos()
                    l = sijainti[0]//SQ_SIZE
                    r = sijainti[1]//SQ_SIZE
                    if valittuRuutu == (r, l) or l >= 8: #käyttäjä clikkasi samaa ruutua kahdesti
                        valittuRuutu = () #poistaa valinnan
                        pelaajaKlikit = []
                    else:
                        valittuRuutu = (r, l)
                        pelaajaKlikit.append(valittuRuutu) #append molemille 1. ja 2. klikille.
                    if len(pelaajaKlikit) == 2: #toisen klikin jälkeen.
                        siirto = ShakkiMoottori.Siirto(pelaajaKlikit[0], pelaajaKlikit[1], pelitila.lauta)
                        print(siirto.haeShakkiNotaatio())
                        for i in range(len(laillisetSiirrot)):
                            if siirto == laillisetSiirrot[i]:
                                pelitila.teeSiirto(laillisetSiirrot[i])
                                siirtoTehty = True
                                animoi = True
                                valittuRuutu = ()  # Resettaa klikit
                                pelaajaKlikit = []
                        if not siirtoTehty:
                            pelaajaKlikit = [valittuRuutu]

            #Näppäin Handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    pelitila.kumoaSiirto()
                    siirtoTehty = True
                    animoi = False
                    peliLoppu = False
                if e.key == p.K_r: #Resetoi pelin kun R näppäintä painaa
                    pelitila = ShakkiMoottori.PeliTila()
                    laillisetSiirrot = pelitila.haeLaillisetSiirrot()
                    valittuRuutu = ()
                    pelaajaKlikit = []
                    siirtoTehty = False
                    animoi = False
                    peliLoppu = False

        #Ai siirto-etsijä logiikka
        if not peliLoppu and not ihmisenVuoro:
            AISiirto = ShakkiAI.etsiParasSiirto(pelitila, laillisetSiirrot)
            if AISiirto is None:
                AISiirto = ShakkiAI.etsiRandomSiirto(laillisetSiirrot)
            pelitila.teeSiirto(AISiirto)
            siirtoTehty = True
            animoi = True


        if siirtoTehty:
            if animoi:
                animoiSiirto(pelitila.siirtoLokikirja[-1], screen, pelitila.lauta, kello)
            laillisetSiirrot = pelitila.haeLaillisetSiirrot()
            siirtoTehty = False
            animoi = False

        piirraPeliTila(screen, pelitila, laillisetSiirrot, valittuRuutu, siirtoLokiFontti)

        if pelitila.shakkimatti or pelitila.pattitilanne:
            peliLoppu = True
            piirraLopetusRuutuTeksti(screen, 'Pattitilanne' if pelitila.pattitilanne else 'Musta voitti Shakkimatilla' if pelitila.valkoisenSiirto else 'Valkoinen voitti Shakkimatilla')



        kello.tick(MAX_FPS)
        p.display.flip()

def piirraPeliTila(screen, pelitila, laillisetSiirrot, valittuRuutu, siirtoLokiFontti):
    piirraLauta(screen)
    korostaRuudut(screen, pelitila, laillisetSiirrot, valittuRuutu)
    piirraNappulat(screen, pelitila.lauta)
    piirraSiirtoLoki(screen, pelitila, siirtoLokiFontti)

def piirraLauta(screen):
    global varit
    varit = [p.Color("white"), p.Color("light blue")]
    for rivi in range(DIMENSION):
        for linja in range(DIMENSION):
            vari = varit[((rivi + linja) % 2)]
            p.draw.rect(screen, vari, p.Rect(linja*SQ_SIZE, rivi*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def korostaRuudut(screen, pelitila, laillisetSiirrot, valittuRuutu):
    if valittuRuutu != ():
        r, l = valittuRuutu
        if pelitila.lauta[r][l][0] == ('w' if pelitila.valkoisenSiirto else 'b'):
            #Korostavalittu
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('purple'))
            screen.blit(s, (l*SQ_SIZE, r*SQ_SIZE))
            #Korosta siirrot siitä ruudusta
            s.fill(p.Color('red'))
            for siirto in laillisetSiirrot:
                if siirto.aloitusRivi == r and siirto.aloitusLinja == l:
                    screen.blit(s, (siirto.lopetusLinja*SQ_SIZE, siirto.lopetusRivi*SQ_SIZE))

def piirraNappulat(screen, lauta):
    for rivi in range(DIMENSION):
        for linja in range(DIMENSION):
            nappula = lauta[rivi][linja]
            if nappula != "--":
                screen.blit(IMAGES[nappula], p.Rect(linja*SQ_SIZE, rivi*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def piirraSiirtoLoki(screen, pelitila, fontti):
    siirtoLokiNelio = p.Rect(LAUTA_LEVEYS, 0, SIIRTO_LOKI_PANEELI_LEVEYS, SIIRTO_LOKI_PANEELI_KORKEUS)
    p.draw.rect(screen, p.Color('Black'), siirtoLokiNelio)
    siirtoLoki = pelitila.siirtoLokikirja
    siirtoTekstit = []
    for i in range(0, len(siirtoLoki), 2):
        siirtoMerkkijono = str(i//2 + 1) + '. ' + str(siirtoLoki[i]) + " "
        if i+1 < len(siirtoLoki):
            siirtoMerkkijono += str(siirtoLoki[i+1]) + "  "
        siirtoTekstit.append(siirtoMerkkijono)

    siirrotPerRivi = 3
    tayte = 5
    riviVali = 2
    tekstiY = tayte
    for i in range(0, len(siirtoTekstit), siirrotPerRivi):
        teksti = ""
        for j in range(siirrotPerRivi):
            if i + j < len(siirtoTekstit):
                teksti += siirtoTekstit[i+j]
        tekstiObjekti = fontti.render(teksti, True, p.Color('White'))
        tekstiPaikka = siirtoLokiNelio.move(tayte, tekstiY)
        screen.blit(tekstiObjekti, tekstiPaikka)
        tekstiY += tekstiObjekti.get_height() + riviVali


def animoiSiirto(siirto, screen, lauta, kello):
    global varit
    dR = siirto.lopetusRivi - siirto.aloitusRivi
    dL = siirto.lopetusLinja - siirto.aloitusLinja
    framesPerRuutu = 10
    frameMaara = (abs(dR) + abs(dL)) * framesPerRuutu
    for frame in range(frameMaara +1):
        r, l = (siirto.aloitusRivi + dR*frame/frameMaara, siirto.aloitusLinja + dL*frame/frameMaara)
        piirraLauta(screen)
        piirraNappulat(screen, lauta)
        vari = varit[(siirto.lopetusRivi + siirto.lopetusLinja) % 2]
        lopetusRuutu = p.Rect(siirto.lopetusLinja*SQ_SIZE, siirto.lopetusRivi*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, vari, lopetusRuutu)
        if siirto.syotyNappula != '--':
            if siirto.onEnpassantSiirto:
                enpassantRivi = siirto.lopetusRivi +1 if siirto.syotyNappula[0] == 'b' else siirto.lopetusRivi - 1
                lopetusRuutu = p.Rect(siirto.lopetusLinja * SQ_SIZE, enpassantRivi * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[siirto.syotyNappula], lopetusRuutu)
            #piirra liikkuva nappula
        screen.blit(IMAGES[siirto.siirrettyNappula], p.Rect(l*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        kello.tick(60)
def piirraLopetusRuutuTeksti(screen, teksti):
    fontti = p.font.SysFont('New York Times', 32, True, False)
    tekstiObjekti = fontti.render(teksti, 0, p.Color('Gray'))
    tekstiPaikka = p.Rect(0, 0, LAUTA_LEVEYS, LAUTA_KORKEUS).move(LAUTA_LEVEYS / 2 - tekstiObjekti.get_width() / 2, LAUTA_KORKEUS / 2 - tekstiObjekti.get_height() / 2)
    screen.blit(tekstiObjekti, tekstiPaikka)
    tekstiObjekti = fontti.render(teksti, 0, p.Color('Black'))
    screen.blit(tekstiObjekti, tekstiPaikka.move(2, 2))



if __name__ == "__main__":
    main()
