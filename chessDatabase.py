from chessGame import ChessGame
import subprocess
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


class ChessDatabase:
    def __init__(self):
        self.games = []

    def getGames(self) -> list:
        return self.games
    
    def getActiveGames(self, playCount: int) -> list:
        return [game for game in self.getGames() if game.getTotalMoves() > playCount]

    def getGamesStockfishWon(self, playCount: int = 0) -> int:
        return sum([game.getStockfishWon() for game in self.getActiveGames(playCount)])

    def getGamesDrawn(self, playCount: int = 0) -> int:
        return sum([game.getDraw() for game in self.getActiveGames(playCount)])

    def getGamesStockfishLost(self, playCount: int = 0) -> int:
        return sum([game.getStockfishLost() for game in self.getActiveGames(playCount)])

    def getGamesStockfishWhiteWin(self, playCount: int = 0) -> int:
        return sum([game.getStockfishWhiteWin() for game in self.getActiveGames(playCount)])

    def getGamesStockfishWhiteLoss(self, playCount: int = 0) -> int:
        return sum([game.getStockfishWhiteLoss() for game in self.getActiveGames(playCount)])

    def getGamesStockfishWhiteDraw(self, playCount: int = 0) -> int:
        return sum([game.getStockfishWhiteDraw() for game in self.getActiveGames(playCount)])

    def getGamesStockfishBlackWin(self, playCount: int = 0) -> int:
        return sum([game.getStockfishBlackWin() for game in self.getActiveGames(playCount)])

    def getGamesStockfishBlackLoss(self, playCount: int = 0) -> int:
        return sum([game.getStockfishBlackLoss() for game in self.getActiveGames(playCount)])

    def getGamesStockfishBlackDraw(self, playCount: int = 0) -> int:
        return sum([game.getStockfishBlackDraw() for game in self.getActiveGames(playCount)])

    def getOngoingList(self):
        activeGames = []
        playCount = 0
        while len(self.getActiveGames(playCount))>0:
            activeGames.append(len(self.getActiveGames(playCount)))
            playCount+=1
        return activeGames
    
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
        ongoing = self.getOngoingList()
        dataPoint = ""

        for i, game in enumerate(ongoing):
            dataPoint += f'({i},{game})'
        print(dataPoint)
                

        with open('sometexfile.tex', 'w') as file:
            file.write('\\documentclass{article}\n')
            file.write('\\title{Stockfish chess statistics}\n')
            file.write('\\author{Johan Bjerkem}\n')
            file.write('\\usepackage{multirow}')
            file.write('\\usepackage{pgfplots}')

            file.write('\\begin{document}\n')
            file.write('\maketitle\n')

            file.write("In this document i will present tables, graphs and statistics about 2600 chess games played by the chess engine Stockfish. The game information is gathered from the document 'Stockfish\\textunderscore15\\textunderscore64-bit.commented.[2600].pgn'. Hopefully you find the data insightful.\\\\\\\\")
            file.write("First we will have a look at the win, loss and draw statistics for Stockfish. The data is presented in a table, where you also can read what color Stockfish played as.\n")

            file.write('\\begin{center}\n')
            file.write('\\begin{tabular}{l|rrr}\n')
            file.write('Color/Result & Wins & Draws & Losses\\\\\n')
            file.write('\hline\n')
            file.write(f'Any & {self.getGamesStockfishWon()} & {self.getGamesDrawn()} & {self.getGamesStockfishLost()}\\\\\n')
            file.write(f'White & {self.getGamesStockfishWhiteWin()} & {self.getGamesStockfishWhiteDraw()} & {self.getGamesStockfishWhiteLoss()}\\\\\n')
            file.write(f'Black & {self.getGamesStockfishBlackWin()} & {self.getGamesStockfishBlackDraw()} & {self.getGamesStockfishBlackLoss()}\\\\\n')
            file.write('\end{tabular}\n')
            file.write('\end{center}\n\n')

            file.write("Below is a graph showing the number of games that is still active after $x$ number of moves.\n\n")

            file.write('\\begin{tikzpicture}\n')
            file.write('\\begin{axis}[\n')
            file.write('\txmin = 0, xmax = 450,\n')
            file.write('\tymin = 0, ymax = 2700,\n')
            file.write('\txtick distance = 50,\n')
            file.write('\tytick distance = 300,\n')
            file.write('\tgrid = both,\n')
            file.write('\tminor tick num = 1,\n')
            file.write('\tmajor grid style = {lightgray},\n')
            file.write('\tminor grid style = {lightgray!25},\n')
            file.write('\twidth = \\textwidth,\n')
            file.write('\theight = 0.5\\textwidth,\n')
            file.write('\txlabel = {$moves$},\n')
            file.write('\tylabel = {$games$},]\n')

            file.write('\\addplot[\n')
            file.write('\tsmooth,\n')
            file.write('\tthick,\n')
            file.write('\tred,\n')
            file.write(']\n')
            file.write('coordinates {\n')
            file.write(dataPoint+"\n")
            file.write('};\n')

            file.write('\\end{axis}\n')
            file.write('\\end{tikzpicture}\n')

            file.write('\\end{document}\n')

        # pip install basictex
        os.system('pdflatex sometexfile.tex')
        os.system('rm sometexfile.aux')
        os.system('rm sometexfile.log')


def main():
    db = ChessDatabase()
    db.addGames()
    db.getGamesStockfishWon()
    print()
    db.createPdf()



if __name__ == '__main__':
    main()
