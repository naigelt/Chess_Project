class PeliTila:
    def __init__(self):
        """
        Board is an 8x8 2d list, each element in list has 2 characters.
        The first character represents the color of the piece: 'b' or 'w'.
        The second character represents the type of the piece: 'R', 'N', 'B', 'Q', 'K' or 'p'.
        "--" represents an empty space with no piece.
        """
        self.lauta = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.siirtoFunktiot = {"p": self.haeSotilasSiirrot, "R": self.haeTorniSiirrot, "N": self.haeHevonenSiirrot,
                              "B": self.haeLahettiSiirrot, "Q": self.haeKuningatarSiirrot, "K": self.haeKuningasSiirrot}
        self.valkoiseSiirto = True
        self.siirtoLoki = []
        self.valkoisenKuninkaanSijainti = (7, 4)
        self.mustanKuninkaanSijainti = (0, 4)
        self.shakkimatti = False
        self.pattitilanne = False
        self.onShakissa = False
        self.kiinnitykset = []
        self.shakit = []
        self.enPassantMahdollinen = ()  # coordinates for the square where en-passant capture is possible
        self.enpassantMahdollinenLoki = [self.enPassantMahdollinen]
        self.nykyisetCastlingOikeudet = CastleOikeudet(True, True, True, True)
        self.castleOikeusLoki = [CastleOikeudet(self.nykyisetCastlingOikeudet.wks, self.nykyisetCastlingOikeudet.bks,
                                                self.nykyisetCastlingOikeudet.wqs, self.nykyisetCastlingOikeudet.bqs)]

    def teeSiirto(self, siirto):

        self.lauta[siirto.aloitusRivi][siirto.aloitusLinja] = "--"
        self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.siirrettyNappula
        self.siirtoLoki.append(siirto)  # log the move so we can undo it later
        self.valkoiseSiirto = not self.valkoiseSiirto  # switch players
        # update king's location if moved
        if siirto.siirrettyNappula == "wK":
            self.valkoisenKuninkaanSijainti = (siirto.lopetusRivi, siirto.lopetusLinja)
        elif siirto.siirrettyNappula == "bK":
            self.mustanKuninkaanSijainti = (siirto.lopetusRivi, siirto.lopetusLinja)

        # pawn promotion
        if siirto.onSotilasYlennys:
            # if not is_AI:
            #    promoted_piece = input("Promote to Q, R, B, or N:") #take this to UI later
            #    self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_piece
            # else:
            self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.siirrettyNappula[0] + "Q"

        # enpassant move
        if siirto.onEnpassantSiirto:
            self.lauta[siirto.aloitusRivi][siirto.lopetusLinja] = "--"  # capturing the pawn

        # update enpassant_possible variable
        if siirto.siirrettyNappula[1] == "p" and abs(siirto.aloitusRivi - siirto.lopetusRivi) == 2:  # only on 2 square pawn advance
            self.enPassantMahdollinen = ((siirto.aloitusRivi + siirto.lopetusRivi) // 2, siirto.aloitusLinja)
        else:
            self.enPassantMahdollinen = ()

        # castle move
        if siirto.onCastleSiirto:
            if siirto.lopetusLinja - siirto.aloitusLinja == 2:  # king-side castle move
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja - 1] = self.lauta[siirto.lopetusRivi][
                    siirto.lopetusLinja + 1]  # moves the rook to its new square
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja + 1] = '--'  # erase old rook
            else:  # queen-side castle move
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja + 1] = self.lauta[siirto.lopetusRivi][
                    siirto.lopetusLinja - 2]  # moves the rook to its new square
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja - 2] = '--'  # erase old rook

        self.enpassantMahdollinenLoki.append(self.enPassantMahdollinen)

        # update castling rights - whenever it is a rook or king move
        self.paivitaCastleOikeudet(siirto)
        self.castleOikeusLoki.append(CastleOikeudet(self.nykyisetCastlingOikeudet.wks, self.nykyisetCastlingOikeudet.bks,
                                                    self.nykyisetCastlingOikeudet.wqs, self.nykyisetCastlingOikeudet.bqs))

    def kumoaSiirto(self):
        """
        Undo the last siirto
        """
        if len(self.siirtoLoki) != 0:  # make sure that there is a siirto to undo
            siirto = self.siirtoLoki.pop()
            self.lauta[siirto.aloitusRivi][siirto.aloitusLinja] = siirto.siirrettyNappula
            self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = siirto.syotyNappula
            self.valkoiseSiirto = not self.valkoiseSiirto  # swap players
            # update the king's position if needed
            if siirto.siirrettyNappula == "wK":
                self.valkoisenKuninkaanSijainti = (siirto.aloitusRivi, siirto.aloitusLinja)
            elif siirto.siirrettyNappula == "bK":
                self.mustanKuninkaanSijainti = (siirto.aloitusRivi, siirto.aloitusLinja)
            # undo en passant siirto
            if siirto.onEnpassantSiirto:
                self.lauta[siirto.lopetusRivi][siirto.lopetusLinja] = "--"  # leave landing square blank
                self.lauta[siirto.aloitusRivi][siirto.lopetusLinja] = siirto.syotyNappula

            self.enpassantMahdollinenLoki.pop()
            self.enPassantMahdollinen = self.enpassantMahdollinenLoki[-1]

            # undo castle rights
            self.castleOikeusLoki.pop()  # get rid of the new castle rights from the siirto we are undoing
            self.nykyisetCastlingOikeudet = self.castleOikeusLoki[
                -1]  # set the current castle rights to the last one in the list
            # undo the castle siirto
            if siirto.onCastleSiirto:
                if siirto.lopetusLinja - siirto.aloitusLinja == 2:  # king-side
                    self.lauta[siirto.lopetusRivi][siirto.lopetusLinja + 1] = self.lauta[siirto.lopetusRivi][siirto.lopetusLinja - 1]
                    self.lauta[siirto.lopetusRivi][siirto.lopetusLinja - 1] = '--'
                else:  # queen-side
                    self.lauta[siirto.lopetusRivi][siirto.lopetusLinja - 2] = self.lauta[siirto.lopetusRivi][siirto.lopetusLinja + 1]
                    self.lauta[siirto.lopetusRivi][siirto.lopetusLinja + 1] = '--'
            self.shakkimatti = False
            self.pattitilanne = False

    def paivitaCastleOikeudet(self, siirto):
        """
        Update the castle rights given the move
        """
        if siirto.syotyNappula == "wR":
            if siirto.lopetusLinja == 0:  # left rook
                self.nykyisetCastlingOikeudet.wqs = False
            elif siirto.lopetusLinja == 7:  # right rook
                self.nykyisetCastlingOikeudet.wks = False
        elif siirto.syotyNappula == "bR":
            if siirto.lopetusLinja == 0:  # left rook
                self.nykyisetCastlingOikeudet.bqs = False
            elif siirto.lopetusLinja == 7:  # right rook
                self.nykyisetCastlingOikeudet.bks = False

        if siirto.siirrettyNappula == 'wK':
            self.nykyisetCastlingOikeudet.wqs = False
            self.nykyisetCastlingOikeudet.wks = False
        elif siirto.siirrettyNappula == 'bK':
            self.nykyisetCastlingOikeudet.bqs = False
            self.nykyisetCastlingOikeudet.bks = False
        elif siirto.siirrettyNappula == 'wR':
            if siirto.aloitusRivi == 7:
                if siirto.aloitusLinja == 0:  # left rook
                    self.nykyisetCastlingOikeudet.wqs = False
                elif siirto.aloitusLinja == 7:  # right rook
                    self.nykyisetCastlingOikeudet.wks = False
        elif siirto.siirrettyNappula == 'bR':
            if siirto.aloitusRivi == 0:
                if siirto.aloitusLinja == 0:  # left rook
                    self.nykyisetCastlingOikeudet.bqs = False
                elif siirto.aloitusLinja == 7:  # right rook
                    self.nykyisetCastlingOikeudet.bks = False

    def haeLaillisetSiirrot(self):
        """
        All siirrot considering checks.
        """
        tempCastleOikeudet = CastleOikeudet(self.nykyisetCastlingOikeudet.wks, self.nykyisetCastlingOikeudet.bks,
                                            self.nykyisetCastlingOikeudet.wqs, self.nykyisetCastlingOikeudet.bqs)
        # advanced algorithm
        siirrot = []
        self.onShakissa, self.kiinnitykset, self.shakit = self.haeShakitJaKiinnitykset()

        if self.valkoiseSiirto:
            kuninkaanRivi = self.valkoisenKuninkaanSijainti[0]
            kuninkaanLinja = self.valkoisenKuninkaanSijainti[1]
        else:
            kuninkaanRivi = self.mustanKuninkaanSijainti[0]
            kuninkaanLinja = self.mustanKuninkaanSijainti[1]
        if self.onShakissa:
            if len(self.shakit) == 1:  # only 1 shakki, block the shakki or move the king
                siirrot = self.haeKaikkiSiirrot()
                # to block the shakki you must put a piece into one of the squares between the enemy piece and your king
                shakki = self.shakit[0]  # shakki information
                shakkiRivi = shakki[0]
                shakkiLinja = shakki[1]
                nappulaTarkastus = self.lauta[shakkiRivi][shakkiLinja]
                laillisetRuudut = []  # squares that pieces can move to
                # if knight, must capture the knight or move your king, other pieces can be blocked
                if nappulaTarkastus[1] == "N":
                    laillisetRuudut = [(shakkiRivi, shakkiLinja)]
                else:
                    for i in range(1, 8):
                        laillinenRuutu = (kuninkaanRivi + shakki[2] * i,
                                        kuninkaanLinja + shakki[3] * i)  # shakki[2] and shakki[3] are the shakki directions
                        laillisetRuudut.append(laillinenRuutu)
                        if laillinenRuutu[0] == shakkiRivi and laillinenRuutu[
                            1] == shakkiLinja:  # once you get to piece and shakki
                            break
                # get rid of any siirrot that don't block shakki or move king
                for i in range(len(siirrot) - 1, -1, -1):  # iterate through the list backwards when removing elements
                    if siirrot[i].siirrettyNappula[1] != "K":  # move doesn't move king so it must block or capture
                        if not (siirrot[i].lopetusRivi,
                                siirrot[i].lopetusLinja) in laillisetRuudut:  # move doesn't block or capture piece
                            siirrot.remove(siirrot[i])
            else:  # double shakki, king has to move
                self.haeKuningasSiirrot(kuninkaanRivi, kuninkaanLinja, siirrot)
        else:  # not in shakki - all siirrot are fine
            siirrot = self.haeKaikkiSiirrot()
            if self.valkoiseSiirto:
                self.haeCastleSiirrot(self.valkoisenKuninkaanSijainti[0], self.valkoisenKuninkaanSijainti[1], siirrot)
            else:
                self.haeCastleSiirrot(self.mustanKuninkaanSijainti[0], self.mustanKuninkaanSijainti[1], siirrot)

        if len(siirrot) == 0:
            if self.shakissaFunktio():
                self.shakkimatti = True
            else:
                # TODO stalemate on repeated siirrot
                self.pattitilanne = True
        else:
            self.shakkimatti = False
            self.pattitilanne = False

        self.nykyisetCastlingOikeudet = tempCastleOikeudet
        return siirrot

    def shakissaFunktio(self):
        """
        Determine if a current player is in check
        """
        if self.valkoiseSiirto:
            return self.ruutuHyokkauksenAlla(self.valkoisenKuninkaanSijainti[0], self.valkoisenKuninkaanSijainti[1])
        else:
            return self.ruutuHyokkauksenAlla(self.mustanKuninkaanSijainti[0], self.mustanKuninkaanSijainti[1])

    def ruutuHyokkauksenAlla(self, rivi, linja):
        """
        Determine if enemy can attack the square row col
        """
        self.valkoiseSiirto = not self.valkoiseSiirto  # switch to opponent's point of view
        vastustajanSiirrot = self.haeKaikkiSiirrot()
        self.valkoiseSiirto = not self.valkoiseSiirto
        for siirto in vastustajanSiirrot:
            if siirto.lopetusRivi == rivi and siirto.lopetusLinja == linja:  # square is under attack
                return True
        return False

    def haeKaikkiSiirrot(self):
        """
        All siirrot without considering checks.
        """
        siirrot = []
        for rivi in range(len(self.lauta)):
            for linja in range(len(self.lauta[rivi])):
                vuoro = self.lauta[rivi][linja][0]
                if (vuoro == "w" and self.valkoiseSiirto) or (vuoro == "b" and not self.valkoiseSiirto):
                    nappula = self.lauta[rivi][linja][1]
                    self.siirtoFunktiot[nappula](rivi, linja, siirrot)  # calls appropriate move function based on nappula type
        return siirrot

    def haeShakitJaKiinnitykset(self):
        kiinnitykset = []  # squares pinned and the suunta its pinned from
        shakit = []  # squares where enemy is applying a check
        onShakissa = False
        if self.valkoiseSiirto:
            vastustajanVari = "b"
            liittolaisenVari = "w"
            aloitusRivi = self.valkoisenKuninkaanSijainti[0]
            aloitusLinja = self.valkoisenKuninkaanSijainti[1]
        else:
            vastustajanVari = "w"
            liittolaisenVari = "b"
            aloitusRivi = self.mustanKuninkaanSijainti[0]
            aloitusLinja = self.mustanKuninkaanSijainti[1]
        # check outwards from king for kiinnitykset and shakit, keep track of kiinnitykset
        suunnat = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(suunnat)):
            suunta = suunnat[j]
            mahdollinenKiinnitys = ()  # reset possible kiinnitykset
            for i in range(1, 8):
                lopetusRivi = aloitusRivi + suunta[0] * i
                lopetusLinja = aloitusLinja + suunta[1] * i
                if 0 <= lopetusRivi <= 7 and 0 <= lopetusLinja <= 7:
                    lopetusNappula = self.lauta[lopetusRivi][lopetusLinja]
                    if lopetusNappula[0] == liittolaisenVari and lopetusNappula[1] != "K":
                        if mahdollinenKiinnitys == ():  # first allied piece could be pinned
                            mahdollinenKiinnitys = (lopetusRivi, lopetusLinja, suunta[0], suunta[1])
                        else:  # 2nd allied piece - no check or pin from this suunta
                            break
                    elif lopetusNappula[0] == vastustajanVari:
                        vastustajanTyyppi = lopetusNappula[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any suunta and piece is a queen
                        # 5.) any suunta 1 square away and piece is a king
                        if (0 <= j <= 3 and vastustajanTyyppi == "R") or (4 <= j <= 7 and vastustajanTyyppi == "B") or (
                                i == 1 and vastustajanTyyppi == "p" and (
                                (vastustajanVari == "w" and 6 <= j <= 7) or (vastustajanVari == "b" and 4 <= j <= 5))) or (
                                vastustajanTyyppi == "Q") or (i == 1 and vastustajanTyyppi == "K"):
                            if mahdollinenKiinnitys == ():  # no piece blocking, so check
                                onShakissa = True
                                shakit.append((lopetusRivi, lopetusLinja, suunta[0], suunta[1]))
                                break
                            else:  # piece blocking so pin
                                kiinnitykset.append(mahdollinenKiinnitys)
                                break
                        else:  # enemy piece not applying shakit
                            break
                else:
                    break  # off board
        # check for knight shakit
        knightSiirrot = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for siirto in knightSiirrot:
            lopetusRivi = aloitusRivi + siirto[0]
            lopetusLinja = aloitusLinja + siirto[1]
            if 0 <= lopetusRivi <= 7 and 0 <= lopetusLinja <= 7:
                lopetusNappula = self.lauta[lopetusRivi][lopetusLinja]
                if lopetusNappula[0] == vastustajanVari and lopetusNappula[1] == "N":  # enemy knight attacking a king
                    onShakissa = True
                    shakit.append((lopetusRivi, lopetusLinja, siirto[0], siirto[1]))
        return onShakissa, kiinnitykset, shakit

    def haeSotilasSiirrot(self, rivi, linja, siirrot):
        """
        Get all the pawn moves for the pawn located at row, col and add the moves to the list.
        """
        nappulaKiinnitetty = False
        kiinitysSuunta = ()
        for i in range(len(self.kiinnitykset) - 1, -1, -1):
            if self.kiinnitykset[i][0] == rivi and self.kiinnitykset[i][1] == linja:
                nappulaKiinnitetty = True
                kiinitysSuunta = (self.kiinnitykset[i][2], self.kiinnitykset[i][3])
                self.kiinnitykset.remove(self.kiinnitykset[i])
                break

        if self.valkoiseSiirto:
            siirtoMaara = -1
            aloitusRivi = 6
            vastustajanVari = "b"
            kuninkaanRivi, kuninkaanLinja = self.valkoisenKuninkaanSijainti
        else:
            siirtoMaara = 1
            aloitusRivi = 1
            vastustajanVari = "w"
            kuninkaanRivi, kuninkaanLinja = self.mustanKuninkaanSijainti

        if self.lauta[rivi + siirtoMaara][linja] == "--":  # 1 ruutu pawn advance
            if not nappulaKiinnitetty or kiinitysSuunta == (siirtoMaara, 0):
                siirrot.append(Siirto((rivi, linja), (rivi + siirtoMaara, linja), self.lauta))
                if rivi == aloitusRivi and self.lauta[rivi + 2 * siirtoMaara][linja] == "--":  # 2 ruutu pawn advance
                    siirrot.append(Siirto((rivi, linja), (rivi + 2 * siirtoMaara, linja), self.lauta))
        if linja - 1 >= 0:  # capture to the left
            if not nappulaKiinnitetty or kiinitysSuunta == (siirtoMaara, -1):
                if self.lauta[rivi + siirtoMaara][linja - 1][0] == vastustajanVari:
                    siirrot.append(Siirto((rivi, linja), (rivi + siirtoMaara, linja - 1), self.lauta))
                if (rivi + siirtoMaara, linja - 1) == self.enPassantMahdollinen:
                    hyokkaavaNappula = blokkaavaNappula = False
                    if kuninkaanRivi == rivi:
                        if kuninkaanLinja < linja:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            alueenSisalla = range(kuninkaanLinja + 1, linja - 1)
                            alueenUlkona = range(linja + 1, 8)
                        else:  # king right of the pawn
                            alueenSisalla = range(kuninkaanLinja - 1, linja, -1)
                            alueenUlkona = range(linja - 2, -1, -1)
                        for i in alueenSisalla:
                            if self.lauta[rivi][i] != "--":  # some piece beside en-passant pawn blocks
                                blokkaavaNappula = True
                        for i in alueenUlkona:
                            ruutu = self.lauta[rivi][i]
                            if ruutu[0] == vastustajanVari and (ruutu[1] == "R" or ruutu[1] == "Q"):
                                hyokkaavaNappula = True
                            elif ruutu != "--":
                                blokkaavaNappula = True
                    if not hyokkaavaNappula or blokkaavaNappula:
                        siirrot.append(Siirto((rivi, linja), (rivi + siirtoMaara, linja - 1), self.lauta, onEnpassantSiirto=True))
        if linja + 1 <= 7:  # capture to the right
            if not nappulaKiinnitetty or kiinitysSuunta == (siirtoMaara, +1):
                if self.lauta[rivi + siirtoMaara][linja + 1][0] == vastustajanVari:
                    siirrot.append(Siirto((rivi, linja), (rivi + siirtoMaara, linja + 1), self.lauta))
                if (rivi + siirtoMaara, linja + 1) == self.enPassantMahdollinen:
                    hyokkaavaNappula = blokkaavaNappula = False
                    if kuninkaanRivi == rivi:
                        if kuninkaanLinja < linja:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            alueenSisalla = range(kuninkaanLinja + 1, linja)
                            alueenUlkona = range(linja + 2, 8)
                        else:  # king right of the pawn
                            alueenSisalla = range(kuninkaanLinja - 1, linja + 1, -1)
                            alueenUlkona = range(linja - 1, -1, -1)
                        for i in alueenSisalla:
                            if self.lauta[rivi][i] != "--":  # some piece beside en-passant pawn blocks
                                blokkaavaNappula = True
                        for i in alueenUlkona:
                            ruutu = self.lauta[rivi][i]
                            if ruutu[0] == vastustajanVari and (ruutu[1] == "R" or ruutu[1] == "Q"):
                                hyokkaavaNappula = True
                            elif ruutu != "--":
                                blokkaavaNappula = True
                    if not hyokkaavaNappula or blokkaavaNappula:
                        siirrot.append(Siirto((rivi, linja), (rivi + siirtoMaara, linja + 1), self.lauta, onEnpassantSiirto=True))

    def haeTorniSiirrot(self, rivi, linja, siirrot):
        """
        Get all the rook moves for the rook located at row, col and add the moves to the list.
        """
        nappulaKiinnitetty = False
        kiinnitysSuunta = ()
        for i in range(len(self.kiinnitykset) - 1, -1, -1):
            if self.kiinnitykset[i][0] == rivi and self.kiinnitykset[i][1] == linja:
                nappulaKiinnitetty = True
                kiinnitysSuunta = (self.kiinnitykset[i][2], self.kiinnitykset[i][3])
                if self.lauta[rivi][linja][
                    1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.kiinnitykset.remove(self.kiinnitykset[i])
                break

        suunnat = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        vastustajanVari = "b" if self.valkoiseSiirto else "w"
        for suunta in suunnat:
            for i in range(1, 8):
                lopetusRivi = rivi + suunta[0] * i
                lopetusLinja = linja + suunta[1] * i
                if 0 <= lopetusRivi <= 7 and 0 <= lopetusLinja <= 7:  # check for possible moves only in boundaries of the board
                    if not nappulaKiinnitetty or kiinnitysSuunta == suunta or kiinnitysSuunta == (
                            -suunta[0], -suunta[1]):
                        end_piece = self.lauta[lopetusRivi][lopetusLinja]
                        if end_piece == "--":  # empty space is valid
                            siirrot.append(Siirto((rivi, linja), (lopetusRivi, lopetusLinja), self.lauta))
                        elif end_piece[0] == vastustajanVari:  # capture enemy piece
                            siirrot.append(Siirto((rivi, linja), (lopetusRivi, lopetusLinja), self.lauta))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break


    def haeHevonenSiirrot(self, rivi, linja, siirrot):
        """
        Get all the knight moves for the knight located at row col and add the moves to the list.
        """
        nappulaKiinnitetty = False
        for i in range(len(self.kiinnitykset) - 1, -1, -1):
            if self.kiinnitykset[i][0] == rivi and self.kiinnitykset[i][1] == linja:
                nappulaKiinnitetty = True
                self.kiinnitykset.remove(self.kiinnitykset[i])
                break

        knightSiirrot = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                        (1, -2))  # up/left up/right right/up right/down down/left down/right left/up left/down
        liittolaisenVari = "w" if self.valkoiseSiirto else "b"
        for siirto in knightSiirrot:
            lopetusRivi = rivi + siirto[0]
            lopetusLinja = linja + siirto[1]
            if 0 <= lopetusRivi <= 7 and 0 <= lopetusLinja <= 7:
                if not nappulaKiinnitetty:
                    lopetusNappula = self.lauta[lopetusRivi][lopetusLinja]
                    if lopetusNappula[0] != liittolaisenVari:  # so its either enemy piece or empty square
                        siirrot.append(Siirto((rivi, linja), (lopetusRivi, lopetusLinja), self.lauta))

    def haeLahettiSiirrot(self, rivi, linja, siirrot):
        """
        Get all the bishop moves for the bishop located at row col and add the moves to the list.
        """
        nappulaKiinnitetty = False
        kiinnitysSuunta = ()
        for i in range(len(self.kiinnitykset) - 1, -1, -1):
            if self.kiinnitykset[i][0] == rivi and self.kiinnitykset[i][1] == linja:
                nappulaKiinnitetty = True
                kiinnitysSuunta = (self.kiinnitykset[i][2], self.kiinnitykset[i][3])
                self.kiinnitykset.remove(self.kiinnitykset[i])
                break

        suunnat = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # diagonals: up/left up/right down/right down/left
        vastustajanVari = "b" if self.valkoiseSiirto else "w"
        for suunta in suunnat:
            for i in range(1, 8):
                lopetuRivi = rivi + suunta[0] * i
                lopetusLinja = linja + suunta[1] * i
                if 0 <= lopetuRivi <= 7 and 0 <= lopetusLinja <= 7:  # check if the move is on board
                    if not nappulaKiinnitetty or kiinnitysSuunta == suunta or kiinnitysSuunta == (
                            -suunta[0], -suunta[1]):
                        lopetusNappula = self.lauta[lopetuRivi][lopetusLinja]
                        if lopetusNappula == "--":  # empty space is valid
                            siirrot.append(Siirto((rivi, linja), (lopetuRivi, lopetusLinja), self.lauta))
                        elif lopetusNappula[0] == vastustajanVari:  # capture enemy piece
                            siirrot.append(Siirto((rivi, linja), (lopetuRivi, lopetusLinja), self.lauta))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def haeKuningatarSiirrot(self, rivi, linja, siirrot):
        """
        Get all the queen moves for the queen located at row col and add the moves to the list.
        """
        self.haeLahettiSiirrot(rivi, linja, siirrot)
        self.haeTorniSiirrot(rivi, linja, siirrot)

    def haeKuningasSiirrot(self, rivi, linja, siirrot):
        """
        Get all the king moves for the king located at row col and add the moves to the list.
        """
        riviSiirrot = (-1, -1, -1, 0, 0, 1, 1, 1)
        linjaSiirrot = (-1, 0, 1, -1, 1, -1, 0, 1)
        liittolaisenVari = "w" if self.valkoiseSiirto else "b"
        for i in range(8):
            lopetusRivi = rivi + riviSiirrot[i]
            lopetusLinja = linja + linjaSiirrot[i]
            if 0 <= lopetusRivi <= 7 and 0 <= lopetusLinja <= 7:
                lopetusNappula = self.lauta[lopetusRivi][lopetusLinja]
                if lopetusNappula[0] != liittolaisenVari:  # not an ally piece - empty or enemy
                    # place king on end square and check for shakit
                    if liittolaisenVari == "w":
                        self.valkoisenKuninkaanSijainti = (lopetusRivi, lopetusLinja)
                    else:
                        self.mustanKuninkaanSijainti = (lopetusRivi, lopetusLinja)
                    onShakisssa, kiinnitykset, shakit = self.haeShakitJaKiinnitykset()
                    if not onShakisssa:
                        siirrot.append(Siirto((rivi, linja), (lopetusRivi, lopetusLinja), self.lauta))
                    # place king back on original location
                    if liittolaisenVari == "w":
                        self.valkoisenKuninkaanSijainti = (rivi, linja)
                    else:
                        self.mustanKuninkaanSijainti = (rivi, linja)

    def haeCastleSiirrot(self, rivi, linja, siirrot):
        """
        Generate all valid castle moves for the king at (row, col) and add them to the list of moves.
        """
        if self.ruutuHyokkauksenAlla(rivi, linja):
            return  # can't castle while in check
        if (self.valkoiseSiirto and self.nykyisetCastlingOikeudet.wks) or (
                not self.valkoiseSiirto and self.nykyisetCastlingOikeudet.bks):
            self.haeKuninkaanPuolenCastleSiirrot(rivi, linja, siirrot)
        if (self.valkoiseSiirto and self.nykyisetCastlingOikeudet.wqs) or (
                not self.valkoiseSiirto and self.nykyisetCastlingOikeudet.bqs):
            self.haeKuningattarenPuolenCastleSiirrot(rivi, linja, siirrot)

    def haeKuninkaanPuolenCastleSiirrot(self, rivi, linja, siirrot):
        if self.lauta[rivi][linja + 1] == '--' and self.lauta[rivi][linja + 2] == '--':
            if not self.ruutuHyokkauksenAlla(rivi, linja + 1) and not self.ruutuHyokkauksenAlla(rivi, linja + 2):
                siirrot.append(Siirto((rivi, linja), (rivi, linja + 2), self.lauta, onCastleSiirto=True))

    def haeKuningattarenPuolenCastleSiirrot(self, rivi, linja, siirrot):
        if self.lauta[rivi][linja - 1] == '--' and self.lauta[rivi][linja - 2] == '--' and self.lauta[rivi][linja - 3] == '--':
            if not self.ruutuHyokkauksenAlla(rivi, linja - 1) and not self.ruutuHyokkauksenAlla(rivi, linja - 2):
                siirrot.append(Siirto((rivi, linja), (rivi, linja - 2), self.lauta, onCastleSiirto=True))


class CastleOikeudet:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Siirto:
    # in chess, fields on the board are described by two symbols, one of them being number between 1-8 (which is corresponding to rows)
    # and the second one being a letter between a-f (corresponding to columns), in order to use this notation we need to map our [row][col] coordinates
    # to match the ones used in the original chess game
    arvorRiveiksi = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rivitArvoiksi = {v: k for k, v in arvorRiveiksi.items()}
    kolumnitLinjoiksi = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    linjatKolumneiksi = {v: k for k, v in kolumnitLinjoiksi.items()}

    def __init__(self, aloitusRuutu, lopetusRuutu, lauta, onEnpassantSiirto=False, onCastleSiirto=False):
        self.aloitusRivi = aloitusRuutu[0]
        self.aloitusLinja = aloitusRuutu[1]
        self.lopetusRivi = lopetusRuutu[0]
        self.lopetusLinja = lopetusRuutu[1]
        self.siirrettyNappula = lauta[self.aloitusRivi][self.aloitusLinja]
        self.syotyNappula = lauta[self.lopetusRivi][self.lopetusLinja]
        # pawn promotion
        self.onSotilasYlennys = (self.siirrettyNappula == "wp" and self.lopetusRivi == 0) or (
                self.siirrettyNappula == "bp" and self.lopetusRivi == 7)
        # en passant
        self.onEnpassantSiirto = onEnpassantSiirto
        if self.onEnpassantSiirto:
            self.syotyNappula = "wp" if self.siirrettyNappula == "bp" else "bp"
        # castle move
        self.onCastleSiirto = onCastleSiirto

        self.onSyoty = self.syotyNappula != "--"
        self.siirtoID = self.aloitusRivi * 1000 + self.aloitusLinja * 100 + self.lopetusRivi * 10 + self.lopetusLinja

    def __eq__(self, other):
        """
        Overriding the equals method.
        """
        if isinstance(other, Siirto):
            return self.siirtoID == other.siirtoID
        return False

    def haeShakkiNotaatio(self):
        if self.onSotilasYlennys:
            return self.haeArvotJaKolumnit(self.lopetusRivi, self.lopetusLinja) + "Q"
        if self.onCastleSiirto:
            if self.lopetusLinja == 1:
                return "0-0-0"
            else:
                return "0-0"
        if self.onEnpassantSiirto:
            return self.haeArvotJaKolumnit(self.aloitusRivi, self.aloitusLinja)[0] + "x" + self.haeArvotJaKolumnit(self.lopetusRivi,
                                                                                                                   self.lopetusLinja) + " e.p."
        if self.syotyNappula != "--":
            if self.siirrettyNappula[1] == "p":
                return self.haeArvotJaKolumnit(self.aloitusRivi, self.aloitusLinja)[0] + "x" + self.haeArvotJaKolumnit(self.lopetusRivi,
                                                                                                                       self.lopetusLinja)
            else:
                return self.siirrettyNappula[1] + "x" + self.haeArvotJaKolumnit(self.lopetusRivi, self.lopetusLinja)
        else:
            if self.siirrettyNappula[1] == "p":
                return self.haeArvotJaKolumnit(self.lopetusRivi, self.lopetusLinja)
            else:
                return self.siirrettyNappula[1] + self.haeArvotJaKolumnit(self.lopetusRivi, self.lopetusLinja)

        # TODO Disambiguating moves

    def haeArvotJaKolumnit(self, rivi, linja):
        return self.linjatKolumneiksi[linja] + self.rivitArvoiksi[rivi]

    def __str__(self):
        if self.onCastleSiirto:
            return "0-0" if self.lopetusLinja == 6 else "0-0-0"

        lopetusRuutu = self.haeArvotJaKolumnit(self.lopetusRivi, self.lopetusLinja)

        if self.siirrettyNappula[1] == "p":
            if self.onSyoty:
                return self.linjatKolumneiksi[self.aloitusLinja] + "x" + lopetusRuutu
            else:
                return lopetusRuutu + "Q" if self.onSotilasYlennys else lopetusRuutu

        siirtoMerkkijono = self.siirrettyNappula[1]
        if self.onSyoty:
            siirtoMerkkijono += "x"
        return siirtoMerkkijono + lopetusRuutu
