
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
        self.siirtoLoki = []
        self.valkoisenSiirto = True
        self.valkoisenKuninkaanSijainti = (7, 4)
        self.mustanKuninkaanSijainti = (0, 4)
        self.shakissa = False
        self.kiinnitykset = []
        self.shakit = []
        self.shakkiMatti = False
        self.staleMate = False
        self.enpassantMahdollinen = ()


    def teeSiirto(self, siirto):
        self.lauta[siirto.aloitusRivi][siirto.aloitusLinja] = "--"
        self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.siirrettyNappula
        self.siirtoLoki.append(siirto) #lisää siirron siirtoLokikirjaan.
        self.valkoisenSiirto = not self.valkoisenSiirto #vaihtaa vuoroa.
        # Päivitetään kuninkaan sijainti, jos sitä on siirretty
        if siirto.siirrettyNappula == 'wK':
            self.valkoisenKuninkaanSijainti = (siirto.lopetusRivi, siirto.lopetusLinja)
        elif siirto.siirrettyNappula == 'bK':
            self.mustanKuninkaanSijainti = (siirto.lopetusRivi, siirto.lopetusLinja)

        #Sotilas ylennys
        if siirto.sotilasYlennys:
            #ylennettyNappula = input("Ylennä joko Q, R, B tai N:")
            self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.siirrettyNappula[0] + 'Q'

        #Enpassant siirto
        if siirto.onEnpassantSiirto:
            self.lauta[siirto.aloitusRivi][siirto.lopetusLinja] = '--' #Syö Sotilaan

        #Päivitä enpassantMahdollinen muuttujaa
        if siirto.siirrettyNappula[1] == 'p' and abs(siirto.aloitusRivi - siirto.lopetusRivi) == 2: #vain 2 ruudun edennyt sotilas
            self.enpassantMahdollinen = ((siirto.aloitusRivi + siirto.lopetusRivi)//2, siirto.aloitusLinja)
        else:
            self.enpassantMahdollinen = ()



    def kumoaSiirto(self):
        if len(self.siirtoLoki) != 0:
            siirto = self.siirtoLoki.pop()
            self.lauta[siirto.aloitusRivi][siirto.aloitusLinja] = siirto.siirrettyNappula
            self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.syotyNappula
            self.valkoisenSiirto = not self.valkoisenSiirto
            # Päivitä kuninkaan sijainti tarvittaessa
            if siirto.siirrettyNappula == 'wK':
                self.valkoisenKuninkaanSijainti = (siirto.aloitusRivi, siirto.aloitusLinja)
            elif siirto.siirrettyNappula == 'bK':
                self.mustanKuninkaanSijainti = (siirto.aloitusRivi, siirto.aloitusLinja)
            #peruuta enpassant siirto
            if siirto.onEnpassantSiirto:
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = '--' #jätä lopetus ruutu tyhjäksi
                self.lauta[siirto.aloitusRivi][siirto.lopetusLinja] = siirto.syotyNappula
                self.enpassantMahdollinen = (siirto.lopetusRivi, siirto.lopetusLinja)
            # peruuta kahden ruudun sotilas siirto
            if siirto.siirrettyNappula[1] == 'p' and abs(siirto.aloitusRivi - siirto.lopetusRivi) == 2:
                self.enpassantMahdollinen = ()



    def haeLaillisetSiirrot(self):
        # 1) Generoidaan kaikki mahdolliset siirrot
        siirrot = []
        self.shakissa, self.kiinnitykset, self.shakit = self.kiinnityksetJaShakit()
        if self.valkoisenSiirto:
            kuninkaanRivi = self.valkoisenKuninkaanSijainti[0]
            kuninkaanLinja = self.valkoisenKuninkaanSijainti[1]
        else:
            kuninkaanRivi = self.mustanKuninkaanSijainti[0]
            kuninkaanLinja = self.mustanKuninkaanSijainti[1]
        if self.shakissa:
            if len(self.shakit) == 1:
                siirrot = self.haeKaikkiSiirrot()
                shakki = self.shakit[0]
                haeRivi = shakki[0]
                haeLinja = shakki[1]
                kiinnityksenTarkistus = self.lauta[haeRivi][haeLinja]
                laillisetRuudut = []
                if kiinnityksenTarkistus[1] == 'N':
                    laillisetRuudut = [(haeRivi, haeLinja)]
                else:
                    for i in range(1, 8):
                        laillinenRuutu = (kuninkaanRivi + shakki[2] * i, kuninkaanLinja + shakki[3] * i)
                        laillisetRuudut.append(laillinenRuutu)
                        if laillinenRuutu[0] == haeRivi and laillinenRuutu[1] == haeLinja:
                            break
                for i in range(len(siirrot) - 1, -1, -1):
                    if siirrot[i].siirrettyNappula[1] != 'K':
                        if not (siirrot[i].lopetusRivi, siirrot[i].lopetusLinja) in laillisetRuudut:
                            siirrot.remove(siirrot[i])
            else:
                self.haeKuningasSiirrot(kuninkaanRivi, kuninkaanLinja, siirrot)
        else:
            siirrot = self.haeKaikkiSiirrot()

        if len(siirrot) == 0:
            if self.shakissa:
                self.shakissa = True
            else:
                self.staleMate = True
        else:
            self.shakissa = False
            self.staleMate = False
        return siirrot




    def haeKaikkiSiirrot(self):
        siirrot = []
        for r in range(len(self.lauta)): # rivien määrä
            for l in range(len(self.lauta[r])): #linjojen määrä jokaisessa rivissä
                turn = self.lauta[r][l][0]
                if (turn == 'w' and self.valkoisenSiirto) or (turn == 'b' and not self.valkoisenSiirto):
                    nappula = self.lauta[r][l][1]
                    self.siirtoFunktiot[nappula](r, l, siirrot)
        return siirrot





    def haeSotilasSiirrot(self, r, l, siirrot):
        nappulaKiinnitetty = False
        nappulanSuunta = ()
        for i in range(len(self.kiinnitykset)-1, -1, -1):
            if self.kiinnitykset[i][0] == r and self.kiinnitykset[i][1] == l:
                nappulaKiinnitetty = True
                nappulanSuunta = (self.kiinnitykset[i][2], self.kiinnitykset[i][3])
                self.kiinnitykset.remove(self.kiinnitykset[i])
                break

        if self.valkoisenSiirto:
            siirtoMaara = -1
            aloitusRivi = 6
            takaRivi = 0
            vihollisenVari = 'b'

        else:
            siirtoMaara = 1
            aloitusRivi = 1
            takaRivi = 7
            vihollisenVari = 'w'
        sotilasYlennys = False

        if self.lauta[r+siirtoMaara][l] == "--": # yhden ruudun siirto
            if not nappulaKiinnitetty or nappulanSuunta == (siirtoMaara, 0):
                if r+siirtoMaara == takaRivi:
                    sotilasYlennys = True
                siirrot.append(Siirto((r, l), (r+siirtoMaara, l), self.lauta, sotilasYlennys=sotilasYlennys))
                if r == aloitusRivi and self.lauta[r+2*siirtoMaara][l] == "--": # kahden ruudun siirto
                    siirrot.append(Siirto((r, l), (r+2*siirtoMaara, l), self.lauta))
        if l-1 >= 0: # Syönti vasemmalle
            if not nappulaKiinnitetty or nappulanSuunta == (siirtoMaara, -1):
                if self.lauta[r + siirtoMaara][l-1][0] == vihollisenVari:
                    if r+ siirtoMaara == takaRivi: # Jos nappula pääsee loppu riville ja on sotilas = ylennys
                        sotilasYlennys = True
                    siirrot.append(Siirto((r, l), (r+siirtoMaara, l-1), self.lauta, sotilasYlennys=sotilasYlennys))
                if (r + siirtoMaara, l-1) == self.enpassantMahdollinen:
                    siirrot.append(Siirto((r, l), (r+siirtoMaara, l-1), self.lauta, onEnpassantSiirto=True))
        if l+1 <= 7: #Syönti oikealle
            if not nappulaKiinnitetty or nappulanSuunta == (siirtoMaara, 1):
                if self.lauta[r + siirtoMaara][l +1][0] == vihollisenVari:
                    if r + siirtoMaara == takaRivi:
                        sotilasYlennys = True
                    siirrot.append(Siirto((r, l), (r+siirtoMaara, l+1), self.lauta, sotilasYlennys=sotilasYlennys))
                if (r + siirtoMaara, l +1) == self.enpassantMahdollinen:
                    siirrot.append(Siirto((r, l), (r+siirtoMaara, l+1), self.lauta, onEnpassantSiirto=True))




    def haeTorninSiirrot(self, r, l, siirrot):
        nappulaKiinnitetty = False
        nappulanSuunta = ()
        for i in range(len(self.kiinnitykset)-1, -1, -1):
            if self.kiinnitykset[i][0] == r and self.kiinnitykset[i][1] == l:
                nappulaKiinnitetty = True
                nappulanSuunta = (self.kiinnitykset[i][2], self.kiinnitykset[i][3])
                if self.lauta[r][l][1] != 'Q':
                    self.kiinnitykset.remove(self.kiinnitykset[i])
                break
        suunnat = ((-1, 0), (0, -1), (1, 0), (0, 1))
        vastustajanVari = "b" if self.valkoisenSiirto else "w"
        for s in suunnat:
            for i in range(1, 8):
                lopetusRivi = r + s[0] * i
                lopetusLinja = l + s[1] * i
                if 0 <= lopetusRivi < 8 and 0 <= lopetusLinja < 8:
                    if not nappulaKiinnitetty or nappulanSuunta == s or nappulanSuunta == (-s[0], -s[1]):
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
        nappulaKiinnitetty = False
        nappulanSuunta = ()
        for i in range(len(self.kiinnitykset) -1, -1, -1):
            if self.kiinnitykset[i][0] == r and self.kiinnitykset[i][1] == l:
                nappulaKiinnitetty = True
                nappulanSuunta = (self.kiinnitykset[i][2], self.kiinnitykset[i][3])
                self.kiinnitykset.remove(self.kiinnitykset[i])
                break
        suunnat = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        vastustajanVari = "b" if self.valkoisenSiirto else "w"
        for s in suunnat:
            for i in range(1, 8):
                lopetusRivi = r + s[0] * i
                lopetusLinja = l + s[1] * i
                if 0 <= lopetusRivi < 8 and 0 <= lopetusLinja < 8:
                    if not nappulaKiinnitetty or nappulanSuunta == s or nappulanSuunta == (-s[0], -s[1]):
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
        nappulaKiinnitetty = False
        for i in range(len(self.kiinnitykset) -1, -1, -1):
            if self.kiinnitykset[i][0] == r and self.kiinnitykset[i][1] == l:
                nappulaKiinnitetty = True
                self.kiinnitykset.remove(self.kiinnitykset[i])
                break
        hevosenSuunnat = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        liittolaisenVari = "w" if self.valkoisenSiirto else "b"
        for m in hevosenSuunnat:
            lopetusRivi = r + m[0]
            lopetusLinja = l + m[1]
            if 0 <= lopetusRivi < 8 and 0 <= lopetusLinja < 8:
                if not nappulaKiinnitetty:
                    lopetusRuutu = self.lauta[lopetusRivi][lopetusLinja] #onko lopetusRUutu = endPiece?? 32:50
                    if lopetusRuutu[0] != liittolaisenVari:
                        siirrot.append(Siirto((r, l), (lopetusRivi, lopetusLinja), self.lauta))

    def haeKuningatarSiirrot(self, r, l, siirrot):
        self.haeLahettiSiirrot(r, l, siirrot)
        self.haeTorninSiirrot(r, l, siirrot)

    def haeKuningasSiirrot(self, r, l, siirrot):
        riviSiirrot = (-1, -1, -1, 0, 0, 1, 1, 1)
        linjaSiirrot = (-1, 0, 1, -1, 1, -1, 0, 1)
        liittolaisenVari = "w" if self.valkoisenSiirto else "b"
        for i in range(8):
            lopetusRivi = r + riviSiirrot[i]
            lopetusLinja = l + linjaSiirrot[i]
            if 0 <= lopetusRivi < 8 and 0 <= lopetusLinja < 8:
                lopetusRuutu = self.lauta[lopetusRivi][lopetusLinja]
                if lopetusRuutu[0] != liittolaisenVari:
                    if liittolaisenVari == 'w':
                        self.valkoisenKuninkaanSijainti = (lopetusRivi, lopetusLinja)
                    else:
                        self.mustanKuninkaanSijainti = (lopetusRivi, lopetusLinja)
                    shakissa, kiinnitykset, shakit = self.kiinnityksetJaShakit()
                    if not shakissa:
                        siirrot.append(Siirto((r, l), (lopetusRivi, lopetusLinja), self.lauta))
                    if liittolaisenVari == 'w':
                        self.valkoisenKuninkaanSijainti = (r, l)
                    else:
                        self.mustanKuninkaanSijainti = (r, l)


    def kiinnityksetJaShakit(self):
        kiinnitykset = []
        shakit = []
        shakissa = False
        if self.valkoisenSiirto:
            vastustajanVari = 'b'
            liittolaisenVari = 'w'
            aloitusRivi = self.valkoisenKuninkaanSijainti[0]
            aloitusLinja = self.valkoisenKuninkaanSijainti[1]
        else:
            vastustajanVari = 'w'
            liittolaisenVari = 'b'
            aloitusRivi = self.mustanKuninkaanSijainti[0]
            aloitusLinja = self.mustanKuninkaanSijainti[1]
        suunnat = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(suunnat)):
            s = suunnat[j]
            mahdKiinnitys = ()
            for i in range(1, 8):
                lopetusRivi = aloitusRivi + s[0] * i
                lopetusLinja = aloitusLinja + s[1] * i
                if 0 <= lopetusRivi < 8 and 0 <= lopetusLinja < 8:
                    lopetusRuutu = self.lauta[lopetusRivi][lopetusLinja]
                    if lopetusRuutu[0] == liittolaisenVari:
                        if mahdKiinnitys == ():
                            mahdKiinnitys = (lopetusRivi, lopetusLinja, s[0], s[1])
                        else:
                            break
                    elif lopetusRuutu[0] == vastustajanVari:
                        tyyppi = lopetusRuutu[1] #tähän asti ok
                        if (0 <= j <= 3 and tyyppi == 'R') or \
                                (4 <= j <= 7 and tyyppi == 'B') or \
                                (i == 1 and tyyppi == 'p' and ((vastustajanVari == 'w' and 6 <= j <= 7) or (vastustajanVari == 'b' and 4 <= j <= 5))) or \
                                (tyyppi == 'Q') or (i == 1 and tyyppi == 'K'):
                            if mahdKiinnitys == ():
                                shakissa = True
                                shakit.append((lopetusRivi, lopetusLinja, s[0], s[1]))
                                break
                            else:
                                kiinnitykset.append(mahdKiinnitys)
                                break
                        else:
                            break
                else:
                    break
        hevosenSiirrot = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in hevosenSiirrot:
            lopetusRivi = aloitusRivi + m[0]
            lopetusLinja = aloitusLinja + m[1]
            if 0 <= lopetusRivi < 8 and 0 <= lopetusLinja < 8:
                lopetusRuutu = self.lauta[lopetusRivi][lopetusLinja]
                if lopetusRuutu[0] == vastustajanVari and lopetusRuutu[1] == 'N':
                    shakissa = True
                    shakit.append((lopetusRivi, lopetusLinja, m[0], m[1]))
        return shakissa, kiinnitykset, shakit



class Siirto():
    #Muutos jotta saadaan konekielestä listan rivit ja linjat oikein, esim 8,8 listasta eli rivit ja lingat on A8.
    rivitArvoiksi = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    arvotRiveiksi = {v: k for k, v in rivitArvoiksi.items()} #Tämä rivi kääntään arvot takaisin päin

    sarakkeistaLinjoiksi = {"a": 0, "b": 1, "c": 2, "d": 3,
                            "e": 4, "f": 5, "g": 6, "h": 7}
    linjoistaSarakkeiksi = {v: k for k, v in sarakkeistaLinjoiksi.items()}



    def __init__(self, aloitusRuutu, lopetusRuutu, lauta, onEnpassantSiirto = False, sotilasYlennys = False):
        self.aloitusRivi = aloitusRuutu[0]
        self.aloitusLinja = aloitusRuutu[1]
        self.lopetusRivi = lopetusRuutu[0]
        self.lopetusLinja = lopetusRuutu[1]
        self.siirrettyNappula = lauta[self.aloitusRivi][self.aloitusLinja]
        self.syotyNappula = lauta[self.lopetusRivi][self.lopetusLinja]
        self.sotilasYlennys = sotilasYlennys
        self.onEnpassantSiirto = onEnpassantSiirto
        if self.onEnpassantSiirto:
            self.syotyNappula = 'wp' if self.siirrettyNappula == 'bp' else 'bp'
        self.siirtoID = self.aloitusRivi * 1000 + self.aloitusLinja * 100 + self.lopetusRivi * 10 + self.lopetusLinja


    def __eq__(self, other):
        if isinstance(other, Siirto):
            return self.siirtoID == other.siirtoID
        return False


    def haeShakkiNotaatio(self):
        return self.haeRiviJaSarake(self.aloitusRivi, self.aloitusLinja) + self.haeRiviJaSarake(self.lopetusRivi, self.lopetusLinja)

    def haeRiviJaSarake(self, rivi, linja):
        return self.linjoistaSarakkeiksi[linja] + self.arvotRiveiksi[rivi]
