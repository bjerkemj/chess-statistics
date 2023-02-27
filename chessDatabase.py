#Tinus Alsos og Johan Bjerkem

from chessGame import ChessGame
import os
import math
from typing import List

ROOT = os.path.dirname(os.path.abspath(__file__))

class ChessDatabase:
    def __init__(self, games: List[ChessGame] = []):
        self.games = games
        if not self.games:
            self.addGames()

    def getAllGames(self) -> List[ChessGame]:
        return self.games

    def getTotalMovesOfGames(self, games: List[ChessGame]):
        return [game.getTotalMoves() for game in games]

    def filterByMoves(self, games: List[ChessGame], playCount: int) -> List[ChessGame]:
        return [game for game in games if game.getTotalMoves() > playCount]

    def filterStockfishWon(self, games: List[ChessGame]) -> List[ChessGame]:
        return [game for game in games if game.getStockfishWon()]

    def filterDrawn(self, games: List[ChessGame]) -> List[ChessGame]:
        return [game for game in games if game.getDraw()]

    def filterStockfishLost(self, games: List[ChessGame]) -> List[ChessGame]:
        return [game for game in games if game.getStockfishLost()]

    def filterStockfishWhite(self, games: List[ChessGame]) -> List[ChessGame]:
        return [game for game in games if game.getStockfishWhite()]

    def filterStockfishBlack(self, games: List[ChessGame]) -> List[ChessGame]:
        return [game for game in games if not game.getStockfishWhite()]

    def getNumListOngoingGames(self, games: List[ChessGame]) -> List[int]:
        activeGames = []
        playCount = 0
        while True:
            filteredGames = self.filterByMoves(games, playCount)
            activeGames.append(len(filteredGames))
            playCount += 1
            if len(filteredGames) == 0:
                break
        return activeGames

    def getDataPoints(self, games: List[ChessGame]) -> str:
        dataPoints = ""
        for i, game in enumerate(games):
            dataPoints += f'({i},{game})'
        return dataPoints

    def getMean(self, games: list):
        return round(sum(games)/len(games), 2)

    def getSd(self, games: list):
        mean = self.getMean(games)
        return round(math.sqrt(sum([abs(game - mean) for game in games])/len(games)), 2)

    def _addGame(self, pgn: str) -> None:
        self.games.append(ChessGame(pgn))

    def addGames(self, fileName: str = "Stockfish_15_64-bit.commented.[2600].pgn") -> None:
        with open(os.path.join(ROOT, fileName), "r") as f:
            fileText = "".join(f.readlines()).strip()
            metaDataGameInfoSplit = fileText.split("\n\n")
            for i in range(0, len(metaDataGameInfoSplit), 2):
                gameInfo = "\n\n".join(metaDataGameInfoSplit[i:i+2])
                self._addGame(gameInfo)

    def getAllPlayedOpenings(self) -> List[str]:
        return list(set([game.getOpening() for game in self.games]))

    def getOpeningsPlayedOverNTimes(self, n: int) -> List[str]:
        allOpenings = self.getAllPlayedOpenings()
        openingsDict = {}
        for opening in allOpenings:
            numPlayed = len(self.getFilteredListOfGamesByOpening(opening))
            if numPlayed >= n:
                openingsDict[opening] = numPlayed
        return openingsDict

    def getFilteredListOfGamesByMoveSequence(self, moveSequence: dict) -> List[ChessGame]:
        if len(moveSequence) == 0:
            return self.games
        return [game for game in self.games if all([game.getMoveByNumber(moveNumber) == move for moveNumber, move in moveSequence.items()])]

    def getFilteredListOfGamesByOpening(self, opening: str) -> List[ChessGame]:
        return [game for game in self.games if game.getOpening() == opening]

    def getFilteredListOfGamesByOpenings(self, openings: List[str]) -> List[ChessGame]:
        if not openings:
            return self.getAllGames()
        return [game for game in self.games if game.getOpening() in openings]

    def getStatisticsByMoveSequence(self, moveSequence: dict = {}) -> tuple:
        games = self.getFilteredListOfGamesByMoveSequence(
            moveSequence=moveSequence)
        numGames = len(games)
        # print(f'numGames = {numGames}')
        gamesWonByWhite = [game for game in games if game.getWhiteWon()]
        numGamesWonByWhite = len(gamesWonByWhite)
        gamesDrawn = [game for game in games if game.getDraw()]
        numGamesDrawn = len(gamesDrawn)
        numGamesWonByBlack = numGames - numGamesDrawn - numGamesWonByWhite
        # print(f'numGamesDrawn = {numGamesDrawn}')
        # print(f'numGamesBlackWon = {numGamesWonByBlack}')

        return numGamesWonByWhite, numGamesDrawn, numGamesWonByBlack

    def getStatsDictionary(self) -> dict:
        gamesAll = self.getAllGames()
        gamesStockfishWhite = self.filterStockfishWhite(gamesAll)
        gamesStockfishBlack = self.filterStockfishBlack(gamesAll)

        gamesStockfishWon = self.filterStockfishWon(gamesAll)
        gamesStockfishDrawn = self.filterDrawn(gamesAll)
        gamesStockfishLost = self.filterStockfishLost(gamesAll)

        gamesWhiteStockfishWon = self.filterStockfishWhite(gamesStockfishWon)
        gamesWhiteStockfishDrawn = self.filterStockfishWhite(
            gamesStockfishDrawn)
        gamesWhiteStockfishLost = self.filterStockfishWhite(gamesStockfishLost)
        numWhiteStockfishAll = len(gamesWhiteStockfishDrawn) + \
            len(gamesWhiteStockfishLost) + len(gamesWhiteStockfishWon)

        gamesBlackStockfishWon = self.filterStockfishBlack(gamesStockfishWon)
        gamesBlackStockfishDrawn = self.filterStockfishBlack(
            gamesStockfishDrawn)
        gamesBlackStockfishLost = self.filterStockfishBlack(gamesStockfishLost)
        numBlackStockfishAll = len(gamesBlackStockfishDrawn) + \
            len(gamesBlackStockfishLost) + len(gamesBlackStockfishWon)

        onGoing = self.getNumListOngoingGames(gamesAll)
        onGoingWhite = self.getNumListOngoingGames(gamesStockfishWhite)
        onGoingBlack = self.getNumListOngoingGames(gamesStockfishBlack)

        dataPointsAllGames = self.getDataPoints(onGoing)
        dataPointsStockFishWhiteGames = self.getDataPoints(onGoingWhite)
        dataPointsStockFishBlackGames = self.getDataPoints(onGoingBlack)

        statsDictionary = {'gamesAll': gamesAll, 'gamesStockfishWhite': gamesStockfishWhite, 'gamesStockfishBlack': gamesStockfishBlack, 'gamesStockfishWon': gamesStockfishWon, 'gamesStockfishDrawn': gamesStockfishDrawn, 'gamesStockfishLost': gamesStockfishLost, 'gamesWhiteStockfishWon': gamesWhiteStockfishWon, 'gamesWhiteStockfishDrawn': gamesWhiteStockfishDrawn, 'gamesWhiteStockfishLost': gamesWhiteStockfishLost, 'gamesBlackStockfishWon': gamesBlackStockfishWon, 'gamesBlackStockfishDrawn': gamesBlackStockfishDrawn, 'gamesBlackStockfishLost': gamesBlackStockfishLost, 'onGoing': onGoing, 'onGoingWhite': onGoingWhite, 'onGoingBlack': onGoingBlack,
                           'dataPointsAllGames': dataPointsAllGames, 'dataPointsStockFishWhiteGames': dataPointsStockFishWhiteGames, 'dataPointsStockFishBlackGames': dataPointsStockFishBlackGames, 'numGamesAll': len(gamesAll), 'numGamesStockfishWon': len(gamesStockfishWon), 'numGamesStockfishDrawn': len(gamesStockfishDrawn), 'numGamesStockfishLost': len(gamesStockfishLost), 'numGamesWhiteStockfishWon': len(gamesWhiteStockfishWon), 'numGamesWhiteStockfishDrawn': len(gamesWhiteStockfishDrawn), 'numGamesWhiteStockfishLost': len(gamesWhiteStockfishLost), 'numGamesWhiteStockfishAll': numWhiteStockfishAll, 'numGamesBlackStockfishAll': numBlackStockfishAll, 'numGamesBlackStockfishWon': len(gamesBlackStockfishWon), 'numGamesBlackStockfishDrawn': len(gamesBlackStockfishDrawn), 'numGamesBlackStockfishLost': len(gamesBlackStockfishLost)}
        return statsDictionary

    def createPdf(self, fileName: str = 'sometexfile') -> None:
        gamesAll = self.getAllGames()
        gamesStockfishWhite = self.filterStockfishWhite(gamesAll)
        gamesStockfishBlack = self.filterStockfishBlack(gamesAll)

        gamesStockfishWon = self.filterStockfishWon(gamesAll)
        gamesStockfishDrawn = self.filterDrawn(gamesAll)
        gamesStockfishLost = self.filterStockfishLost(gamesAll)

        gamesWhiteStockfishWon = self.filterStockfishWhite(gamesStockfishWon)
        gamesWhiteStockfishDrawn = self.filterStockfishWhite(
            gamesStockfishDrawn)
        gamesWhiteStockfishLost = self.filterStockfishWhite(gamesStockfishLost)

        gamesBlackStockfishWon = self.filterStockfishBlack(gamesStockfishWon)
        gamesBlackStockfishDrawn = self.filterStockfishBlack(
            gamesStockfishDrawn)
        gamesBlackStockfishLost = self.filterStockfishBlack(gamesStockfishLost)

        onGoing = self.getNumListOngoingGames(gamesAll)
        onGoingWhite = self.getNumListOngoingGames(gamesStockfishWhite)
        onGoingBlack = self.getNumListOngoingGames(gamesStockfishBlack)

        dataPointsAllGames = self.getDataPoints(onGoing)
        dataPointsStockFishWhiteGames = self.getDataPoints(onGoingWhite)
        dataPointsStockFishBlackGames = self.getDataPoints(onGoingBlack)

        with open(fileName + '.tex', 'w') as file:
            file.write('\\documentclass{article}\n')
            file.write('\\title{Stockfish chess statistics}\n')
            file.write('\\author{Johan Bjerkem and Tinus F Alsos}\n')
            file.write('\\usepackage{multirow}')
            file.write('\\usepackage{pgfplots}')

            file.write('\\begin{document}\n')
            file.write('\maketitle\n')

            file.write(
                "In this document i will present tables, graphs and statistics about 2600 chess games played by the chess engine Stockfish. The game information is gathered from the document 'Stockfish\\textunderscore15\\textunderscore64-bit.commented.[2600].pgn'. Hopefully you find the data insightful.\\\\\\\\")
            file.write("First we will have a look at the win, loss and draw statistics for Stockfish. The data is presented in a table, where you also can read what color Stockfish played as.\n")

            file.write('\\begin{center}\n')
            file.write('\\begin{tabular}{l|rrr}\n')
            file.write('Color/Result & Wins & Draws & Losses\\\\\n')
            file.write('\hline\n')
            file.write(
                f'Any & {len(gamesStockfishWon)} & {len(gamesStockfishDrawn)} & {len(gamesStockfishLost)}\\\\\n')
            file.write(
                f'White & {len(gamesWhiteStockfishWon)} & {len(gamesWhiteStockfishDrawn)} & {len(gamesWhiteStockfishLost)}\\\\\n')
            file.write(
                f'Black & {len(gamesBlackStockfishWon)} & {len(gamesBlackStockfishDrawn)} & {len(gamesBlackStockfishLost)}\\\\\n')
            file.write('\end{tabular}\n')
            file.write('\end{center}\n\n')

            file.write(
                "Below is a graph showing the number of games that is still active after $x$ number of moves.\n\n")

            file.write('\\begin{figure}')
            file.write('\\begin {tikzpicture}\n')
            file.write('\\begin{axis}[\n')
            file.write('\txmin = 0, xmax = 425,\n')
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
            file.write(dataPointsAllGames + "\n")
            file.write('};\n')

            file.write('\\end{axis}\n')
            file.write('\\end{tikzpicture}\n')
            file.write('\caption{Mean moves: ' + str(self.getMean(onGoing)
                                                     ) + ', SD: ' + str(self.getSd(onGoing)) + '}\n')
            file.write('\end{figure}\n')

            file.write(
                "Below is a graph showing the number of games that is still active after $x$ number of moves.\n\n")

            file.write('\\begin{figure}')
            file.write('\\begin {tikzpicture}\n')
            file.write('\\begin{axis}[\n')
            file.write('\txmin = 0, xmax = 425,\n')
            file.write('\tymin = 0, ymax = 1350,\n')
            file.write('\txtick distance = 50,\n')
            file.write('\tytick distance = 150,\n')
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
            file.write('\tblue,\n')
            file.write(']\n')
            file.write('coordinates {\n')
            file.write(dataPointsStockFishWhiteGames + "\n")
            file.write('};\n')
            file.write('\\addlegendentry{Stockfish white}\n')

            file.write('\\addplot[\n')
            file.write('\tsmooth,\n')
            file.write('\tthick,\n')
            file.write('\tblack,\n')
            file.write(']\n')
            file.write('coordinates {\n')
            file.write(dataPointsStockFishBlackGames + "\n")
            file.write('};\n')
            file.write('\\addlegendentry{Stockfish Black}\n')

            # file.write('\include{dice.pgn}\n')

            file.write('\\end{axis}\n')
            file.write('\\end{tikzpicture}\n')
            # file.write('\caption{Mean moves: ' + str(self.getMean(self.getTotalMoves())) + ', SD: ' + str(self.getSd(self.getTotalMoves())) + '}\n')
            file.write('\end{figure}\n')

            file.write('\\end{document}\n')

        # pip install basictex
        # os.system('pdflatex sometexfile.tex')
        # os.system('rm sometexfile.aux')
        # os.system('rm sometexfile.log')

    def addOpeningTableToPDF(self, filename: str, opening: str, depth: int = 0) -> None:
        statsDictionary = self.getStatsDictionary()
        with open(filename + '.tex', 'r') as file:
            lines = file.readlines()
            endLine = lines.pop()

        with open(filename + '.tex', 'w') as file:
            file.writelines(lines)
            file.write('Here comes another table!!\n\n')
            file.write('\\begin{table}[h!]\n')
            file.write('\\centering\n')
            file.write('\\begin{tabular}{l|rrrr}\n')
            file.write('Color/Result & Wins & Draws & Losses & Total\\\\\n')
            file.write('\hline\n')
            file.write(
                f'Any & {statsDictionary["numGamesStockfishWon"]} & {statsDictionary["numGamesStockfishDrawn"]} & {statsDictionary["numGamesStockfishLost"]} & {statsDictionary["numGamesAll"]}\\\\\n')
            file.write(
                f'White & {statsDictionary["numGamesWhiteStockfishWon"]} & {statsDictionary["numGamesWhiteStockfishDrawn"]} & {statsDictionary["numGamesWhiteStockfishLost"]} & {statsDictionary["numGamesWhiteStockfishAll"]}\\\\\n')
            file.write(
                f'Black & {statsDictionary["numGamesBlackStockfishWon"]} & {statsDictionary["numGamesBlackStockfishDrawn"]} & {statsDictionary["numGamesBlackStockfishLost"]} & {statsDictionary["numGamesBlackStockfishAll"]}\\\\\n')
            file.write('\end{tabular}\n')
            file.write(
                '\caption{Statistics for Stockfish when opening is: ' + opening + '}\n')
            file.write('\end{table}\n')
            file.write(endLine)

    def addOpeningsPlayedOverNTimesToPDF(self, filename: str, n=int) -> None:
        openingsDict = self.getOpeningsPlayedOverNTimes(n=n)
        for opening in openingsDict.keys():
            new_db = ChessDatabase(
                self.getFilteredListOfGamesByOpening(opening))
            new_db.addOpeningTableToPDF(
                filename=filename, opening=opening, depth=0)


def main():
    db = ChessDatabase()
    print()
    filename = 'TinusTexFile'
    db.createPdf(filename)
    openings = db.getAllPlayedOpenings()
    print(openings)
    print('Bird' in openings)
    db.addOpeningsPlayedOverNTimesToPDF(filename=filename, n=50)
    # for opening in openings:
    #     new_db = ChessDatabase(db.getFilteredListOfGamesByOpening(opening))
    #     new_db.addOpeningTableToPDF(
    #         filename=filename, opening=opening, depth=0)


if __name__ == '__main__':
    main()
