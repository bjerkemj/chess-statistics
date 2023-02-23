import os
import re
ROOT = os.path.dirname(os.path.abspath(__file__))


class ChessGame:
    requiredTags = ["Event", "Site", "Date",
                    "Round", "White", "Black", "Result"]
    optionalTags = ["ECO", "Opening", "PlyCount", "WhiteElo", "BlackElo"]

    def __init__(self, pgn: str):
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
        return self.moves[moveNumber - 1][0]

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
            moveInfo = gameDataText[moveStartIndex:moveEndIndex]

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

    def updateGameData(self) -> None:
        self.stockfishWhite = True if re.search(
            r"\bStockfish\b", self.metaData["White"]) else False
        self.totalMoves = int(self.metaData["PlyCount"])
        if self.metaData["Result"] == "1/2-1/2":
            self.draw = True
            return
        self.whiteWon = True if self.metaData["Result"] == "1-0" else False


def main():
    cg1 = None
    with open(os.path.join(ROOT, "oneGame.pgn"), "r") as f:
        str = ""
        for line in f:
            str += line
        cg1 = ChessGame(str)
        cg1.savePng("saveOneGame")
        print(cg1.getDraw())
        print(cg1.getTotalMoves())
        print(f"metaData:\n {cg1.metaData}")
        print('\n ----------')
        print(f"moves:\n {cg1.moves}")
        print('\n ----------')
        print(f"totalMoves:\n {cg1.totalMoves}")
        print('\n ----------')
        print(cg1.getMoveByNumber(2))


if __name__ == '__main__':
    main()
