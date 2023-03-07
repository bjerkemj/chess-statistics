import os
import re
import xlsxwriter
ROOT = os.path.dirname(os.path.abspath(__file__))

class ChessGame:
    requiredTags = ["Event", "Site", "Date",
                    "Round", "White", "Black", "Result"]
    optionalTags = ["ECO", "Opening", "PlyCount", "WhiteElo", "BlackElo"]

    def __init__(self, pgn: str) ->  None:
        self.metaData = {}
        self.moves = []
        self.stockfishWhite = False
        self.draw = False
        self.whiteWon = False
        self.totalMoves = 0
        self.loadPng(pgn)

    def getStockfishWhite(self) -> bool:
        return self.stockfishWhite

    def getDraw(self) -> bool:
        return self.draw

    def getOpening(self) -> str:
        return self.metaData['Opening']

    def getWhiteWon(self) -> bool:
        return self.whiteWon

    def getTotalMoves(self) -> int:
        return self.totalMoves

    def getMoveByNumber(self, moveNumber: int) -> str:
        if type(moveNumber) == str:
            moveNumber = int(moveNumber)
        return self.moves[moveNumber - 1][0] if moveNumber < self.totalMoves else False

    def getStockfishWon(self) -> bool:
        return self.getStockfishWhite() == self.getWhiteWon() and not self.getDraw()

    def getStockfishLost(self) -> bool:
        return self.getStockfishWhite() != self.getWhiteWon() and not self.getDraw()

    def getStockfishWhiteWin(self) -> bool:
        return self.getStockfishWhite() and self.getStockfishWon()

    def getStockfishWhiteLoss(self) -> bool:
        return self.getStockfishWhite() and self.getStockfishLost()

    def getStockfishWhiteDraw(self) -> bool:
        return self.getStockfishWhite() and self.getDraw()

    def getStockfishBlackWin(self) -> bool:
        return not self.getStockfishWhite() and self.getStockfishWon()

    def getStockfishBlackLoss(self) -> bool:
        return not self.getStockfishWhite() and self.getStockfishLost()

    def getStockfishBlackDraw(self) -> bool:
        return not self.getStockfishWhite() and self.getDraw()

    def loadPng(self, pgn: str) -> None:
        split = pgn.split("\n")
        dataSplitIndex = split.index("")
        metaDataText = " ".join(split[:dataSplitIndex])
        gameDataText = " ".join(split[dataSplitIndex:]).strip()

        for tag in self.requiredTags:
            tagIndex = metaDataText.find(tag)
            firstQuoteIndex = pgn.find("\"", tagIndex)
            secondQuoteIndex = pgn.find("\"", firstQuoteIndex+1)
            self.metaData[tag] = pgn[firstQuoteIndex+1:secondQuoteIndex]

        for tag in self.optionalTags:
            if tag in metaDataText:
                tagIndex = metaDataText.find(tag)
                firstQuoteIndex = pgn.find("\"", tagIndex)
                secondQuoteIndex = pgn.find("\"", firstQuoteIndex+1)
                self.metaData[tag] = pgn[firstQuoteIndex+1:secondQuoteIndex]

        while "{" in gameDataText:
            moveStartIndex = gameDataText.find(" ") + 1
            moveEndIndex = gameDataText.find("{") - 1
            moveInfo = gameDataText[moveStartIndex:moveEndIndex].strip()

            commentStartIndex = gameDataText.find("{") + 1
            commentEndIndex = gameDataText.find("}")
            commentInfo = gameDataText[commentStartIndex:commentEndIndex]

            self.moves.append([moveInfo, commentInfo])

            gameDataText = gameDataText[commentEndIndex +
                                        (1 if len(self.moves) % 2 == 1 else 2):]

        self.updateGameData()

    def savePng(self, saveName: str) -> None:
        with open(os.path.join(ROOT, saveName + ".pgn"), "w") as f:
            for key, value in self.metaData.items():
                f.write(f"[{key} \"{value}\"]\n")
            f.write("\n")

            gameDataText = ""
            for i, moveInfo in enumerate(self.moves):
                if i % 2 == 0:
                    gameDataText += str(int(i/2+1)) + ". "
                gameDataText += f"{moveInfo[0]} "
                gameDataText += "{"
                gameDataText += moveInfo[1]
                gameDataText += "} "

            index = 0
            while index+81 < len(gameDataText):
                spaceIndex = gameDataText.rfind(" ", index, index+81)
                gameDataList = list(gameDataText)
                gameDataList[spaceIndex] = "\n"
                gameDataText = "".join(gameDataList)
                index = spaceIndex

            f.writelines(gameDataText)
            f.write(self.metaData["Result"] + "\n")
        
    def saveXlsx(self, saveName: str) -> None:
        os.system('rm ' + saveName + '.xlsx')
        workbook = xlsxwriter.Workbook(saveName + '.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        for key, value in self.metaData.items():
                worksheet.write(row, 0, key)
                worksheet.write(row, 1, value)
                row += 1
        
        column = 0
        for move in self.moves:
            worksheet.write(row, column, move[0])
            worksheet.write(row, column+1, move[1])
            if column == 0:
                column = 2
            else:
                column = 0
                row+=1                

        workbook.close()

    def updateGameData(self) -> None:
        self.stockfishWhite = True if re.search(
            r"\bStockfish\b", self.metaData["White"]) else False
        self.totalMoves = int(self.metaData["PlyCount"])
        if self.metaData["Result"] == "1/2-1/2":
            self.draw = True
            return
        self.whiteWon = True if self.metaData["Result"] == "1-0" else False

cg = ChessGame("""[Event "CCRL 40/15"]
[Site "CCRL"]
[Date "2022.04.20"]
[Round "820.1.525"]
[White "Stockfish 15 64-bit"]
[Black "Arasan 23.3 64-bit"]
[Result "1-0"]
[ECO "A03"]
[Opening "Bird's opening"]
[PlyCount "99"]
[WhiteElo "3511"]
[BlackElo "3333"]

1. f4 {+0.00/1 0s} d5 {+0.00/1 0s} 2. b3 {+0.00/1 0s} Bg4 {+0.00/1 0s} 3. Bb2
{+0.00/1 0s} Nc6 {+0.00/1 0s} 4. h3 {+0.00/1 0s} Bh5 {+0.00/1 0s} 5. g4      
{+0.00/1 0s} Bg6 {+0.00/1 0s} 6. Nf3 {+0.00/1 0s} h5 {+0.00/1 0s} 7. g5
{+0.00/1 0s} e6 {+0.00/1 0s} 8. e3 {+0.00/1 0s} Nge7 {+0.00/1 0s} 9. Bb5
{-0.36/32 45s} a6 {(h4) +0.59/28 20s} 10. Bxc6+ {(Bxc6) -0.24/30 10s} Nxc6
{(Nxc6) +0.62/28 18s} 11. d3 {(d3) -0.28/29 10s} Qe7 {(h4) +0.74/28 18s} 12.
Qe2 {(Qe2) -0.12/30 17s} O-O-O {(O-O-O) +0.92/27 18s} 13. Qf2 {(Qf2) -0.12/32
29s} f6 {(f6) +0.50/26 20s} 14. Nh4 {(Nc3) -0.07/31 9s} Bf7 {(Bf7) +0.64/28
21s} 15. gxf6 {(gxf6) -0.04/32 14s} gxf6 {(gxf6) +0.59/30 21s} 16. Nc3 {(Nc3)
-0.12/32 13s} Qe8 {(Qd7) +0.43/27 21s} 17. O-O-O {(O-O-O) +0.00/29 19s} e5
{(Rg8) +0.43/25 21s} 18. Rdf1 {(Rdf1) +0.00/33 11s} Be6 {(Be6) +0.23/27 19s}
19. f5 {(Kb1) -0.06/35 65s} Bf7 {(Bf7) +0.14/33 21s} 20. Kb1 {(Ng6) +0.00/34
30s} Rg8 {(Bc5) +0.39/27 42s} 21. Rhg1 {(Rhg1) -0.15/32 8s} Rxg1 {(Bc5)
+0.41/27 22s} 22. Rxg1 {(Rxg1) +0.00/31 12s} Bc5 {(Bc5) +0.34/27 39s} 23. Ng6
{(Bc1) +0.00/36 29s} b6 {(Qd7) +0.07/29 38s} 24. Na4 {(Ne2) +0.06/35 19s} Bd6
{(Bd6) +0.00/29 17s} 25. Nc3 {(Nc3) +0.00/35 10s} Bc5 {(Bc5) +0.00/32 17s} 26.
Bc1 {(Na4) +0.00/40 56s} Qd7 {(Ne7) +0.04/26 17s} 27. Qf3 {(Qf3) +0.00/31 9s}
Kb8 {(Kb8) +0.07/28 17s} 28. Qxh5 {(Qxh5) +0.31/32 16s} Nb4 {(Nb4) +0.17/30
17s} 29. Na4 {(Na4) +0.01/36 26s} Bd6 {(Bd6) +0.16/30 15s} 30. Qg4 {(Bd2)
+0.00/36 33s} Qc6 {(d4) +0.00/25 21s} 31. Qg2 {(Qg2) +0.70/27 9s} b5 {(b5)
+0.37/29 17s} 32. Nb2 {(Nb2) +0.55/30 18s} Qb6 {(Qb6) +0.00/32 17s} 33. Bd2
{(a3) +0.56/31 14s} Bc5 {(a5) -0.46/29 31s} 34. c3 {(Rf1) +1.68/27 13s} Nc6
{(Nc6) -1.05/30 18s} 35. d4 {(d4) +1.52/28 19s} Bd6 {(Bd6) -1.24/24 14s} 36. h4
{(h4) +1.84/28 14s} b4 {(exd4) -1.90/26 13s} 37. dxe5 {(dxe5) +1.77/30 15s}
Nxe5 {(Bxe5) -2.07/26 13s} 38. cxb4 {(cxb4) +1.91/28 15s} d4 {(Nc6) -2.27/28
12s} 39. e4 {(e4) +2.62/28 18s} d3 {(d3) -2.82/28 12s} 40. Rd1 {(h5) +3.13/26
10s} Nc6 {(Nc6) -3.31/25 14s} 41. h5 {(Nxd3) +3.39/25 18s} Bxb4 {(Bxb4)
-3.94/27 24s} 42. Bc1 {(Bc1) +3.50/27 18s} d2 {(d2) -4.34/29 19s} 43. Bxd2
{(Bxd2) +4.00/28 16s} Ba3 {(Bxd2) -4.15/30 16s} 44. Qe2 {(Qf3) +4.17/24 14s}
Kb7 {(Kb7) -5.16/24 17s} 45. Bc1 {(Be3) +4.66/26 20s} Bxb2 {(Bxb2) -5.46/23
16s} 46. Kxb2 {(Kxb2) +4.68/26 25s} Rxd1 {(Bc4) -7.71/27 21s} 47. Qxd1 {(Qxd1)
+5.98/27 18s} Qf2+ {(Qf2) -7.85/32 32s} 48. Qd2 {(Qd2) +6.79/28 26s} Qg1 {(Qc5)
-8.42/35 15s} 49. h6 {(h6) +7.51/26 18s} Bxg6 {(Bg8) -8.21/38 15s} 50. fxg6
{(fxg6) +8.93/27 30s} 1-0""")

cg.saveXlsx("delete")