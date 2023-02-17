import subprocess, os
ROOT = os.path.dirname(os.path.abspath(__file__))

from chessGame import ChessGame

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
    with open('sometexfile.tex','w') as file:
        file.write('\\documentclass{article}\n')
        file.write('\\begin{document}\n')
        file.write('Hello Palo Alto!\n')
        file.write('\\end{document}\n')
    
    x  = subprocess.call('pdflatex sometexfile.tex')
    if x != 0:
        print('Exit-code not 0, check result!')
    else:
        os.system('start sometexfile.pdf')


if __name__ == '__main__':
    main()
