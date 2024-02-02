
class PeliTila():
    def __init__(self):
        #lauta on 8x8 2d lista. Jos kerkiaa  niin muokataan pythonin numpy listaan.
        self.lauta = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bp", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.siirtoFunktiot = {'p': self.haeSotilasSiirrot, 'R': self.haeTorninSiirrot, 'N': self.haeHevosenSiirrot,
                               'B': self.haeLahettiSiirrot, 'Q': self.haeKuningatarSiirrot, 'K': self.haeKuningasSiirrot}

        self.valkoisenSiirto = True
        self.siirtoLokikirja = []

    def teeSiirto(self, siirto):
        self.lauta[siirto.aloitusRivi][siirto.aloitusLinja] = "--"
        self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.siirrettyNappula
        self.siirtoLokikirja.append(siirto) #lisää siirron siirtoLokikirjaan.
        self.valkoisenSiirto = not self.valkoisenSiirto #vaihtaa vuoroa.

    def kumoaSiirto(self):
        if len(self.siirtoLokikirja) != 0:
            siirto = self.siirtoLokikirja.pop()
            self.lauta[siirto.aloitusRivi][siirto.aloitusLinja] = siirto.siirrettyNappula
            self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.syotyNappula
            self.valkoisenSiirto = not self.valkoisenSiirto

    def haeLaillisetSiirrot(self):
        return self.haeKaikkiSiirrot()

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



    def haeTorninSiirrot(self, r, l, siirrot):
        pass

    def haeLahettiSiirrot(self, r, l, siirrot):
        pass

    def haeHevosenSiirrot(self, r, l, siirrot):
        pass

    def haeKuningatarSiirrot(self, r, l, siirrot):
        pass
    def haeKuningasSiirrot(self, r, l, siirrot):
        pass


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
