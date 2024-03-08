
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
        self.shakkimatti = False
        self.pattitilanne = False
        self.enpassantMahdollinen = ()
        self.enPassantMahdollinenLoki = [self.enpassantMahdollinen]
        self.nykyinenCastleOikeus = CastleOikeudet(True, True, True, True)
        self.castleOikeusLoki = [CastleOikeudet(self.nykyinenCastleOikeus.wks, self.nykyinenCastleOikeus.bks,
                                                self.nykyinenCastleOikeus.wqs, self.nykyinenCastleOikeus.bqs)]

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
            # Sotilas ylennys
        if siirto.onSotilasYlennys:
            # ylennettyNappula = input("Ylennä joko Q, R, B tai N:")
            self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.siirrettyNappula[0] + 'Q'
            # Enpassant siirto
        if siirto.onEnpassantSiirto:
            self.lauta[siirto.aloitusRivi][siirto.lopetusLinja] = '--'  # Syö Sotilaan
            # Päivitä enpassant Mahdollinen muuttujaa
        if siirto.siirrettyNappula[1] == 'p' and abs(siirto.aloitusRivi - siirto.lopetusRivi) == 2:  # vain 2 ruudun edennyt sotilas
            self.enpassantMahdollinen = ((siirto.aloitusRivi + siirto.lopetusRivi) // 2, siirto.aloitusLinja)
        else:
            self.enpassantMahdollinen = ()

        #Castle Siirto
        if siirto.onCastleSiirto:
            if siirto.lopetusLinja - siirto.aloitusLinja == 2: # Kuninkaan puolen castle siirto
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja-1] = self.lauta[siirto.lopetusRivi][siirto.lopetusLinja+1] #Kopio Tornin uuteen ruutuun
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja+1] = '--'
            else: # Kuningattaren puolen Castle siirto
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja+1] = self.lauta[siirto.lopetusRivi][siirto.lopetusLinja-2] # Kopio tornin uuteen ruutuun
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja-2] = '--'

        #Päivitä Castling oikeudet - kun torni tai kuningas tekee siirron
        self.paivitaCastleOikeudet(siirto)
        self.castleOikeusLoki.append(CastleOikeudet(self.nykyinenCastleOikeus.wks, self.nykyinenCastleOikeus.bks,
                                                self.nykyinenCastleOikeus.wqs, self.nykyinenCastleOikeus.bqs))
        self.enPassantMahdollinenLoki.append(self.enpassantMahdollinen)
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
            #kumoa Enpassant
            if siirto.onEnpassantSiirto:
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = '--'  # jätä lopetus ruutu tyhjäksi
                self.lauta[siirto.aloitusRivi][siirto.lopetusLinja] = siirto.syotyNappula
            self.enPassantMahdollinenLoki.pop()
            self.enpassantMahdollinen = self.enPassantMahdollinenLoki[-1]


            #Peruuta Castlin oikeudet
            self.castleOikeusLoki.pop() #Poistamme uudet castle oikeudet siirrosta minkä teemme
            self.nykyinenCastleOikeus = self.castleOikeusLoki[-1] #Palautamme aikaisemmat castle oikeudet listasta
            #Peruuta Castle siirto
            if siirto.onCastleSiirto:
                if siirto.lopetusLinja - siirto.aloitusLinja == 2:
                    self.lauta[siirto.lopetusRivi][siirto.lopetusLinja+1] = self.lauta[siirto.lopetusRivi][siirto.lopetusLinja-1]
                    self.lauta[siirto.lopetusRivi][siirto.lopetusLinja-1] = '--'
                else: # Kuningattaren puoli
                    self.lauta[siirto.lopetusRivi][siirto.lopetusLinja-2] = self.lauta[siirto.lopetusRivi][siirto.lopetusLinja+1]
                    self.lauta[siirto.lopetusRivi][siirto.lopetusLinja + 1] = '--'

            self.shakkimatti = False
            self.pattitilanne = False

    def paivitaCastleOikeudet(self, siirto):
        if siirto.siirrettyNappula == 'wK':
            self.nykyinenCastleOikeus.wks = False
            self.nykyinenCastleOikeus.wqs = False
        elif siirto.siirrettyNappula == 'bK':
            self.nykyinenCastleOikeus.bks = False
            self.nykyinenCastleOikeus.wks = False
        elif siirto.siirrettyNappula == 'wR':
            if siirto.aloitusRivi == 7:
                if siirto.aloitusLinja == 0: #Vasen torni
                    self.nykyinenCastleOikeus.wqs = False
                elif siirto.aloitusLinja == 7:#Oikea Torni
                    self.nykyinenCastleOikeus.wks = False
        elif siirto.siirrettyNappula == 'bR':
            if siirto.aloitusRivi == 0:
                if siirto.aloitusLinja == 0: #Vasen torni
                    self.nykyinenCastleOikeus.bqs = False
                elif siirto.aloitusLinja == 7:#Oikea Torni
                    self.nykyinenCastleOikeus.bks = False

    def haeLaillisetSiirrot(self):
        tempEnpassantMahdollinen = self.enpassantMahdollinen
        tempCastleOikeus = CastleOikeudet(self.nykyinenCastleOikeus.wks, self.nykyinenCastleOikeus.bks,
                                          self.nykyinenCastleOikeus.wqs, self.nykyinenCastleOikeus.bqs) # Kopio tämänhetkiset castle oikeudet
        # 1) Generoidaan kaikki mahdolliset siirrot
        siirrot = self.haeKaikkiSiirrot()
        if self.valkoisenSiirto:
            self.haeCastleSiirrot(self.valkoisenKuninkaanSijainti[0], self.valkoisenKuninkaanSijainti[1], siirrot)
        else:
            self.haeCastleSiirrot(self.mustanKuninkaanSijainti[0], self.mustanKuninkaanSijainti[1], siirrot)
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
                self.shakkimatti = True
            else:
                self.pattitilanne = True
        else:
            self.shakkimatti = False
            self.pattitilanne = False
        self.enpassantMahdollinen = tempEnpassantMahdollinen
        self.nykyinenCastleOikeus = tempCastleOikeus

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
                elif (r-1, l-1) == self.enpassantMahdollinen:
                    siirrot.append(Siirto((r, l),(r-1, l-1), self.lauta, onEnpassantSiirto=True))
            if l + 1 <= 7: #Syönnit oikealle
                if self.lauta[r-1][l+1][0] == 'b':
                    siirrot.append(Siirto((r, l),(r-1, l+1), self.lauta))
                elif (r - 1, l + 1) == self.enpassantMahdollinen:
                    siirrot.append(Siirto((r, l), (r - 1, l + 1), self.lauta, onEnpassantSiirto=True))

        else: # Mustan Siirrot
            if self.lauta[r + 1][l] == "--": #Yhden ruudun siirto
                siirrot.append(Siirto((r, l), (r+1, l), self.lauta))
                if r == 1 and self.lauta[r + 2][l] == "--": #Kahden ruudun siirto
                    siirrot.append(Siirto((r, l),(r+2, l), self.lauta))
            #Syönnit
            if l - 1 >= 0:
                if self.lauta[r + 1][l-1][0] == 'w': #Syönti Vase
                    siirrot.append(Siirto((r, l),(r +1, l - 1), self.lauta))
                elif (r + 1, l - 1) == self.enpassantMahdollinen:
                    siirrot.append(Siirto((r, l), (r + 1, l - 1), self.lauta, onEnpassantSiirto=True))
            if l + 1 <= 7: # Syönti oikea
                if self.lauta[r + 1][l + 1][0] == 'w':
                    siirrot.append(Siirto((r, l),(r + 1, l + 1), self.lauta))
                elif (r + 1, l + 1) == self.enpassantMahdollinen:
                    siirrot.append(Siirto((r, l), (r + 1, l + 1), self.lauta, onEnpassantSiirto=True))
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

    def haeCastleSiirrot(self, r, l, siirrot):
        if self.ruutuHyökkäyksenAlaisena(r, l):
            return # EI voi castleta jos on shakissa
        if (self.valkoisenSiirto and self.nykyinenCastleOikeus.wks) or (not self.valkoisenSiirto and self.nykyinenCastleOikeus.bks):
            self.haeKuninkaanPuolenCastleSiirrot(r, l, siirrot)
        if (self.valkoisenSiirto and self.nykyinenCastleOikeus.wqs) or (not self.valkoisenSiirto and self.nykyinenCastleOikeus.bqs):
            self.haeKuningattarenPuolenCastleSiirrot(r, l, siirrot)

    def haeKuninkaanPuolenCastleSiirrot(self, r, l, siirrot):
        if self.lauta[r][l+1] == '--' and self.lauta[r][l+2] == '--':
            if not self.ruutuHyökkäyksenAlaisena(r, l+1) and not self.ruutuHyökkäyksenAlaisena(r, l+2):
                siirrot.append(Siirto((r, l), (r, l+2), self.lauta, onCastleSiirto=True))


    def haeKuningattarenPuolenCastleSiirrot(self, r, l, siirrot):
        if self.lauta[r][l-1] == '--' and self.lauta[r][l-2] == '--' and self.lauta[r][l-3]:
            if not self.ruutuHyökkäyksenAlaisena(r, l - 1) and not self.ruutuHyökkäyksenAlaisena(r, l - 2):
                siirrot.append(Siirto((r, l), (r, l - 2), self.lauta, onCastleSiirto=True))


class CastleOikeudet():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs




class Siirto():
    #Muutos jotta saadaan konekielestä listan rivit ja linjat oikein, esim 8,8 listasta eli rivit ja lingat on A8.
    rivitArvoiksi = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    arvotRiveiksi = {v: k for k, v in rivitArvoiksi.items()} #Tämä rivi kääntään arvot takaisin päin

    sarakkeistaLinjoiksi = {"a": 0, "b": 1, "c": 2, "d": 3,
                            "e": 4, "f": 5, "g": 6, "h": 7}
    linjoistaSarakkeiksi = {v: k for k, v in sarakkeistaLinjoiksi.items()}



    def __init__(self, aloitusRuutu, lopetusRuutu, lauta, onEnpassantSiirto=False, onCastleSiirto=False):
        self.aloitusRivi = aloitusRuutu[0]
        self.aloitusLinja = aloitusRuutu[1]
        self.lopetusRivi = lopetusRuutu[0]
        self.lopetusLinja = lopetusRuutu[1]
        self.siirrettyNappula = lauta[self.aloitusRivi][self.aloitusLinja]
        self.syotyNappula = lauta[self.lopetusRivi][self.lopetusLinja]
        #Sotilas ylennys
        self.onSotilasYlennys = (self.siirrettyNappula == 'wp' and self.lopetusRivi == 0) or (self.siirrettyNappula == 'bp' and self.lopetusRivi == 7)
        #Enpassant
        self.onEnpassantSiirto = onEnpassantSiirto
        if self.onEnpassantSiirto:
            self.syotyNappula = 'wp' if self.siirrettyNappula == 'bp' else 'bp'
        #Castle Siirto
        self.onCastleSiirto = onCastleSiirto
        self.onSyoty = self.syotyNappula != '--'

        self.siirtoID = self.aloitusRivi * 1000 + self.aloitusLinja * 100 + self.lopetusRivi * 10 + self.lopetusLinja


    def __eq__(self, other):
        if isinstance(other, Siirto):
            return self.siirtoID == other.siirtoID
        return False


    def haeShakkiNotaatio(self):
        return self.haeRiviJaSarake(self.aloitusRivi, self.aloitusLinja) + self.haeRiviJaSarake(self.lopetusRivi, self.lopetusLinja)

    def haeRiviJaSarake(self, rivi, linja):
        return self.linjoistaSarakkeiksi[linja] + self.arvotRiveiksi[rivi]

    def __str__(self):
        #Castle siirto
        if self.onCastleSiirto:
            return "O-O" if self.lopetusLinja == 6 else "O-O-O"

        lopetusRuutu = self.haeRiviJaSarake(self.lopetusRivi, self.lopetusLinja)

        if self.siirrettyNappula[1] == 'p':
            if self.onSyoty:
                return self.linjoistaSarakkeiksi[self.aloitusLinja] + "x" + lopetusRuutu
            else:
                return lopetusRuutu

        siirtoMerkkijono = self.siirrettyNappula[1]
        if self.onSyoty:
            siirtoMerkkijono += 'x'
        return siirtoMerkkijono + lopetusRuutu




