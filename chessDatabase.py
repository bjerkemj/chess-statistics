from chessGame import ChessGame
import subprocess
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


class ChessDatabase:
    def __init__(self):
        self.games = []

    def getGames(self) -> list:
        return self.games

    def getGamesStockfishWon(self) -> int:
        return sum([game.getStockfishWon() for game in self.getGames()])

    def getGamesDrawn(self) -> int:
        return sum([game.getDraw() for game in self.getGames()])

    def getGamesStockfishLost(self) -> int:
        return sum([game.getStockfishLost() for game in self.getGames()])

    def getGamesStockfishWhiteWin(self) -> int:
        return sum([game.getStockfishWhiteWin() for game in self.getGames()])

    def getGamesStockfishWhiteLoss(self) -> int:
        return sum([game.getStockfishWhiteLoss() for game in self.getGames()])

    def getGamesStockfishWhiteDraw(self) -> int:
        return sum([game.getStockfishWhiteDraw() for game in self.getGames()])

    def getGamesStockfishBlackWin(self) -> int:
        return sum([game.getStockfishBlackWin() for game in self.getGames()])

    def getGamesStockfishBlackLoss(self) -> int:
        return sum([game.getStockfishBlackLoss() for game in self.getGames()])

    def getGamesStockfishBlackDraw(self) -> int:
        return sum([game.getStockfishBlackDraw() for game in self.getGames()])

    def addGame(self, pgn: str) -> None:
        self.games.append(ChessGame(pgn))

    def addGames(self, fileName: str = "Stockfish_15_64-bit.commented.[2600].pgn") -> None:
        with open(os.path.join(ROOT, fileName), "r") as f:
            fileText = "".join(f.readlines()).strip()
            metaDataGameInfoSplit = fileText.split("\n\n")
            for i in range(0, len(metaDataGameInfoSplit), 2):
                gameInfo = "\n\n".join(metaDataGameInfoSplit[i:i+2])
                self.addGame(gameInfo)

    def createPdf(self):
        with open('sometexfile.tex', 'w') as file:
            file.write('\\documentclass{article}\n')
            file.write('\\title{Stockfish chess statistics}\n')
            file.write('\\author{Johan Bjerkem}\n')
            file.write('\\usepackage{multirow}')
            file.write('\\usepackage{pgfplots}')

            file.write('\\begin{document}\n')
            file.write('\maketitle\n')

            file.write('\\begin{tabular}{l|rrr}\n')
            file.write('Color/Result & Wins & Draws & Losses\\\\\n')
            file.write('\hline\n')
            file.write(f'Any & {self.getGamesStockfishWon()} & {self.getGamesDrawn()} & {self.getGamesStockfishLost()}\\\\\n')
            file.write(f'White & {self.getGamesStockfishWhiteWin()} & {self.getGamesStockfishWhiteDraw()} & {self.getGamesStockfishWhiteLoss()}\\\\\n')
            file.write(f'Black & {self.getGamesStockfishBlackWin()} & {self.getGamesStockfishBlackDraw()} & {self.getGamesStockfishBlackLoss()}\\\\\n')
            file.write('\end{tabular}\n\\\\')

            file.write('\\begin{tikzpicture}\n')
            file.write('\\begin{axis}\n')
            file.write('\\addplot[color=red]{exp(x)};\n')
            file.write('\\end{axis}\n')
            file.write('\\end{tikzpicture}\n')

            file.write('\nBruh!\n')
            file.write('\\end{document}\n')

        # pip install basictex
        os.system('pdflatex sometexfile.tex')
        os.system('rm sometexfile.aux')
        os.system('rm sometexfile.log')
        print(f"\\\\")


def main():
    db = ChessDatabase()
    db.addGames()
    db.getGamesStockfishWon()
    print(f"Wins: {db.getGamesStockfishWon()}")
    print(f"Draws: {db.getGamesDrawn()}")
    print(f"Losses: {db.getGamesStockfishLost()}")
    print()
    print(f"White wins: {db.getGamesStockfishWhiteWin()}")
    print(f"White draws: {db.getGamesStockfishWhiteDraw()}")
    print(f"White losses: {db.getGamesStockfishWhiteLoss()}")
    print()
    print(f"Black wins: {db.getGamesStockfishBlackWin()}")
    print(f"Black draws: {db.getGamesStockfishBlackDraw()}")
    print(f"Black losses: {db.getGamesStockfishBlackLoss()}")
    print()
    db.createPdf()


if __name__ == '__main__':
    main()
