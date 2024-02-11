
class PeliTila():
    def __init__(self):
        #lauta on 8x8 2d lista. Jos kerkiaa  niin muokataan pythonin numpy listaan.
        self.lauta = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.siirtoFunktiot = {'p': self.haeSotilasSiirrot, 'R': self.haeTorninSiirrot, 'N': self.haeHevosenSiirrot,
                               'B': self.haeLahettiSiirrot, 'Q': self.haeKuningatarSiirrot, 'K': self.haeKuningasSiirrot}

        self.valkoisenSiirto = True
        self.siirtoLokikirja = []
        self.valkoisenKuninkaanSijainti = (7, 4)
        self.mustanKuninkaanSijainti = (0,4)
        self.shakkiMatti = False
        self.pattitilanne = False

    def teeSiirto(self, siirto):
        self.lauta[siirto.aloitusRivi][siirto.aloitusLinja] = "--"
        self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.siirrettyNappula
        self.siirtoLokikirja.append(siirto) #lisää siirron siirtoLokikirjaan.
        self.valkoisenSiirto = not self.valkoisenSiirto #vaihtaa vuoroa.
        # Päivitetään kuninkaan sijainti, jos sitä on siirretty
        if siirto.siirrettyNappula == 'wK':
            self.valkoisenKuninkaanSijainti = (siirto.lopetusRivi, siirto.lopetusLinja)
        elif siirto.siirrettyNappula == 'bK':
            self.mustanKuninkaanSijainti = (siirto.lopetusRivi, siirto.lopetusLinja)


    def kumoaSiirto(self):
        if len(self.siirtoLokikirja) != 0:
            siirto = self.siirtoLokikirja.pop()
            self.lauta[siirto.aloitusRivi][siirto.aloitusLinja] = siirto.siirrettyNappula
            self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.syotyNappula
            self.valkoisenSiirto = not self.valkoisenSiirto
            # Päivitä kuninkaan sijainti tarvittaessa
            if siirto.siirrettyNappula == 'wK':
                self.valkoisenKuninkaanSijainti = (siirto.aloitusRivi, siirto.aloitusLinja)
            elif siirto.siirrettyNappula == 'bK':
                self.mustanKuninkaanSijainti = (siirto.aloitusRivi, siirto.aloitusLinja)


    def haeLaillisetSiirrot(self):
        # 1) Generoidaan kaikki mahdolliset siirrot
        siirrot = self.haeKaikkiSiirrot()
        # 2) Tee jokainen mahdollinen siirto
        for i in range(len(siirrot)-1, -1, -1): # Lista käydään läpi takaperin bugien välttämiseksi
            self.teeSiirto(siirrot[i])
            # 3) Generoidaan jokainen vastustajan mahdollinen siirto
            # 4) Tarkista jokaisen vastustajan siirto ja hyökkääkö hän kuningastasi kohti
            self.valkoisenSiirto = not self.valkoisenSiirto
            if self.shakissa():
                siirrot.remove(siirrot[i]) # 5) Jos he hyökkäävät kuningasta vastaan, se ei ole validi siirto
            self.valkoisenSiirto = not self.valkoisenSiirto
            self.kumoaSiirto()
        if len(siirrot) == 0: # Joko shakkimatti tai pattitilanne
            if self.shakissa():
                self.shakkiMatti = True
            else:
                self.pattitilanne = True
        else:
            self.shakkiMatti = False
            self.pattitilanne = False

        return siirrot

    '''
    Tutkitaan onko tämänhetkinen pelaaja shakissa
    '''
    def shakissa(self):
        if self.valkoisenSiirto:
            return self.ruutuHyökkäyksenAlaisena(self.valkoisenKuninkaanSijainti[0], self.valkoisenKuninkaanSijainti[1])
        else:
            return self.ruutuHyökkäyksenAlaisena(self.mustanKuninkaanSijainti[0], self.mustanKuninkaanSijainti[1])

    '''
    Tutkitaan voiko vihollinen hyökätä kohtaan r,l
    '''
    def ruutuHyökkäyksenAlaisena(self, r, l):
        self.valkoisenSiirto = not self.valkoisenSiirto # Vaihdetaan vastustajan vuoroksi
        vastustajanSiirrot = self.haeKaikkiSiirrot()
        self.valkoisenSiirto = not self.valkoisenSiirto # Vaihdetaan vuoro takaisin
        for siirto in vastustajanSiirrot:
            if siirto.lopetusRivi == r and siirto.lopetusLinja == l: # Ruutu on hyökkäyksen alaisena
                return True
        return False


    def haeKaikkiSiirrot(self):
        siirrot = []
        for r in range(len(self.lauta)): # rivien määrä
            for l in range(len(self.lauta[r])): #linjojen määrä jokaisessa rivissä
                turn = self.lauta[r][l][0]
                if (turn == "w" and self.valkoisenSiirto) or (turn == "b" and not self.valkoisenSiirto):
                    nappula = self.lauta[r][l][1]
                    self.siirtoFunktiot[nappula](r, l, siirrot)
        return siirrot

    def haeSotilasSiirrot(self, r, l, siirrot):

        if self.valkoisenSiirto: #Valkoisen siirrot
            if self.lauta[r-1][l] == "--":
                siirrot.append(Siirto((r, l), (r-1, l), self.lauta))
                if r == 6 and self.lauta[r-2][l] == "--":
                    siirrot.append(Siirto((r, l),(r-2, l),self.lauta))
            if l - 1 >= 0: #Syönnit vasemmalle
                if self.lauta[r-1][l-1][0] == 'b': # nappula on musta
                    siirrot.append(Siirto((r, l),(r-1, l-1), self.lauta))
            if l + 1 <= 7: #Syönnit oikealle
                if self.lauta[r-1][l+1][0] == 'b':
                    siirrot.append(Siirto((r, l),(r-1, l+1), self.lauta))

        else: # Mustan Siirrot
            if self.lauta[r + 1][l] == "--": #Yhden ruudun siirto
                siirrot.append(Siirto((r, l), (r+1, l), self.lauta))
                if r == 1 and self.lauta[r + 2][l] == "--": #Kahden ruudun siirto
                    siirrot.append(Siirto((r, l),(r+2, l), self.lauta))
                #Syönnit
                if l - 1 >= 0:
                    if self.lauta[r + 1][l-1][0] == 'w': #Syönti Vase
                        siirrot.append(Siirto((r, l),(r +1, l - 1), self.lauta))
                    if l + 1 <= 7: # Syönti oikea
                        if self.lauta[r + 1][l + 1][0] == 'w':
                            siirrot.append(Siirto((r, l),(r + 1, l + 1), self.lauta))
        # pitää lisätä sotilaan promo kuningattareksi yms.




    def haeTorninSiirrot(self, r, l, siirrot):
        suunnat = ((-1, 0), (0, -1), (1, 0), (0, 1))
        vastustajanVari = "b" if self.valkoisenSiirto else "w"
        for s in suunnat:
            for i in range(1, 8):
                lopetusRivi = r + s[0] * i
                lopetusLinja = l + s[1] * i
                if 0 <= lopetusRivi < 8 and 0 <= lopetusLinja < 8:
                    lopetusRuutu = self.lauta[lopetusRivi][lopetusLinja]
                    if lopetusRuutu == "--":
                        siirrot.append(Siirto((r, l), (lopetusRivi, lopetusLinja), self.lauta))
                    elif lopetusRuutu[0] == vastustajanVari:
                        siirrot.append(Siirto((r, l), (lopetusRivi, lopetusLinja), self.lauta))
                        break
                    else:
                        break
                else:
                    break




    def haeLahettiSiirrot(self, r, l, siirrot):
        suunnat = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        vastustajanVari = "b" if self.valkoisenSiirto else "w"
        for s in suunnat:
            for i in range(1, 8):
                lopetusRivi = r + s[0] * i
                lopetusLinja = l + s[1] * i
                if 0 <= lopetusRivi < 8 and 0 <= lopetusLinja < 8:
                    lopetusRuutu = self.lauta[lopetusRivi][lopetusLinja]
                    if lopetusRuutu == "--":
                        siirrot.append(Siirto((r, l), (lopetusRivi, lopetusLinja), self.lauta))
                    elif lopetusRuutu[0] == vastustajanVari:
                        siirrot.append(Siirto((r, l), (lopetusRivi, lopetusLinja), self.lauta))
                        break
                    else:
                        break
                else:
                    break


    def haeHevosenSiirrot(self, r, l, siirrot):
        hevosenSuunnat = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        omaVari = "w" if self.valkoisenSiirto else "b"
        for s in hevosenSuunnat:
            lopetusRivi = r + s[0]
            lopetusLinja = l + s[1]
            if 0 <= lopetusRivi < 8 and 0 <= lopetusLinja < 8:
                lopetusRuutu = self.lauta[lopetusRivi][lopetusLinja]
                if lopetusRuutu[0] != omaVari:
                    siirrot.append(Siirto((r, l), (lopetusRivi, lopetusLinja), self.lauta))

    def haeKuningatarSiirrot(self, r, l, siirrot):
        self.haeLahettiSiirrot(r, l, siirrot)
        self.haeTorninSiirrot(r, l, siirrot)

    def haeKuningasSiirrot(self, r, l, siirrot):
        kuningasSuunnat = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        omaVari = "w" if self.valkoisenSiirto else "b"
        for i in range(8):
            lopetusRivi = r + kuningasSuunnat[i][0]
            lopetusLinja = l + kuningasSuunnat[i][1]
            if 0 <= lopetusRivi < 8 and 0 <= lopetusLinja < 8:
                lopetusRuutu = self.lauta[lopetusRivi][lopetusLinja]
                if lopetusRuutu[0] != omaVari:
                    siirrot.append(Siirto((r, l), (lopetusRivi, lopetusLinja), self.lauta))



class Siirto():
    #Muutos jotta saadaan konekielestä listan rivit ja linjat oikein, esim 8,8 listasta eli rivit ja lingat on A8.
    rivitArvoiksi = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    arvotRiveiksi = {v: k for k, v in rivitArvoiksi.items()} #Tämä rivi kääntään arvot takaisin päin

    sarakkeistaLinjoiksi = {"a": 0, "b": 1, "c": 2, "d": 3,
                            "e": 4, "f": 5, "g": 6, "h": 7}
    linjoistaSarakkeiksi = {v: k for k, v in sarakkeistaLinjoiksi.items()}



    def __init__(self, aloitusRuutu, lopetusRuutu, lauta):
        self.aloitusRivi = aloitusRuutu[0]
        self.aloitusLinja = aloitusRuutu[1]
        self.lopetusRivi = lopetusRuutu[0]
        self.lopetusLinja = lopetusRuutu[1]
        self.siirrettyNappula = lauta[self.aloitusRivi][self.aloitusLinja]
        self.syotyNappula = lauta[self.lopetusRivi][self.lopetusLinja]
        self.siirtoID = self.aloitusRivi * 1000 + self.aloitusLinja * 100 + self.lopetusRivi * 10 + self.lopetusLinja


    def __eq__(self, other):
        if isinstance(other, Siirto):
            return self.siirtoID == other.siirtoID
        return False


    def haeShakkiNotaatio(self):
        return self.haeRiviJaSarake(self.aloitusRivi, self.aloitusLinja) + self.haeRiviJaSarake(self.lopetusRivi, self.lopetusLinja)

    def haeRiviJaSarake(self, rivi, linja):
        return self.linjoistaSarakkeiksi[linja] + self.arvotRiveiksi[rivi]
