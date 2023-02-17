import os
ROOT = os.path.dirname(os.path.abspath(__file__))

class ChessGame:
    requiredTags = ["Event", "Site", "Date", "Round", "White", "Black", "Result"]
    optionalTags = ["ECO", "Opening", "PlyCount", "WhiteElo", "BlackElo"]


    def __init__(self, pgn: str):
        self.metaData = {}
        self.moves = []
        self.loadPng(pgn)

    
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

            gameDataText = gameDataText[commentEndIndex+(1 if len(self.moves)%2==1 else 2):]

    def savePng(self, saveName: str) -> None:
        with open(os.path.join(ROOT, saveName + ".pgn"), "w") as f:
            for key, value in self.metaData.items():
                f.write(f"[{key} \"{value}\"]\n")
            f.write("\n")

            gameDataText = ""
            for i, moveInfo in enumerate(self.moves):
                if i%2==0:
                    gameDataText += str(int(i/2+1)) + ". "
                gameDataText += f"{moveInfo[0]} "
                gameDataText += "{"
                gameDataText += moveInfo[1]
                gameDataText += "} "

            index = 0
            while index+81<len(gameDataText):
                print(index)
                spaceIndex = gameDataText.rfind(" ", index, index+81)
                gameDataList = list(gameDataText)
                gameDataList[spaceIndex] = "\n"
                gameDataText = "".join(gameDataList)
                index = spaceIndex
            
            f.writelines(gameDataText)
            f.write(self.metaData["Result"] + "\n")


def main():
    cg1 = None
    print(len("{(Nc6) -1.05/30 18s} 35. d4 {(d4) +1.52/28 19s} Bd6 {(Bd6) -1.24/24 14s} 36. h4"))
    print(len("+5.98/27 18s} Qf2+ {(Qf2) -7.85/32 32s} 48. Qd2 {(Qd2) +6.79/28 26s} Qg1 {(Qc5)"))
    with open(os.path.join(ROOT, "oneGame.pgn"), "r") as f:      
        str = ""
        for line in f:
            str += line
        cg1 = ChessGame(str)
        cg1.savePng("saveOneGame")


if __name__ == '__main__':
    main()
