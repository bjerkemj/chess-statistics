#Tinus Alsos og Johan Bjerkem

from chessGame import ChessGame
import os
import math
from typing import List
from pylatex import Document, Section, Subsection, Command, Tabular, TikZ, Axis, Plot, LineBreak, Figure, StandAloneGraphic
from matplotlib import pyplot as plt
from pylatex.utils import italic, NoEscape

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
        dataPoints = []
        for i, game in enumerate(games):
            dataPoints.append((game))
        return dataPoints

    def getMean(self, games: list):
        return round(sum([game.getTotalMoves() for game in games])/len(games), 2)

    def getSd(self, games: list):
        mean = self.getMean(games)
        return round(math.sqrt(sum([abs(game.getTotalMoves() - mean) for game in games])/len(games)), 2)

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

    def createPdf(self, fileName: str = 'report') -> None:
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
        onGoingWon= self.getNumListOngoingGames(gamesStockfishWon)
        onGoingDrawn= self.getNumListOngoingGames(gamesStockfishDrawn)
        onGoingLost = self.getNumListOngoingGames(gamesStockfishLost)

        dataPointsAllGames = self.getDataPoints(onGoing)
        dataPointsStockFishWhiteGames = self.getDataPoints(onGoingWhite)
        dataPointsStockFishBlackGames = self.getDataPoints(onGoingBlack)
        dataPointsStockFishWon= self.getDataPoints(onGoingWon)
        dataPointsStockFishDrawn= self.getDataPoints(onGoingDrawn)
        dataPointsStockFishLost = self.getDataPoints(onGoingLost)

        doc = Document(fileName)
        doc.preamble.append(Command('title', 'Stockfish chess statistics'))
        doc.preamble.append(Command('author', 'Tinus F Alsos and Johan Bjerkem'))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))
        doc.append("In this document i will present tables, graphs and statistics about 2600 chess games played by the chess engine Stockfish. The game information is gathered from the document 'Stockfish_15_64-bit.commented.[2600].pgn'. Hopefully you find the data insightful.")

        with doc.create(Subsection('Tables')):
                doc.append("In the table below you can see the results of the 2600 games that Stockfish played.")
                doc.append(LineBreak())
                doc.append(LineBreak())
                with doc.create(Tabular('l|rrr')) as table:
                    table.add_row(("Color/Result", "Wins", "Draws", "Losses"))
                    table.add_hline()
                    table.add_row(("Any", len(gamesStockfishWon), len(gamesStockfishDrawn), len(gamesStockfishLost)))
                    table.add_row(("White", len(gamesWhiteStockfishWon), len(gamesWhiteStockfishDrawn), len(gamesWhiteStockfishLost)))
                    table.add_row(("Black", len(gamesBlackStockfishWon), len(gamesBlackStockfishDrawn), len(gamesBlackStockfishLost)))

                doc.append(LineBreak())
                doc.append(LineBreak())
                doc.append("The table below shows the mean and standard deviation accompanying Figure 1.")
                doc.append(LineBreak())
                doc.append(LineBreak())
                with doc.create(Tabular('l|rr')) as table:
                    table.add_row(("Color/Result", "Mean", "SD"))
                    table.add_hline()
                    table.add_row(("Any", self.getMean(gamesAll), self.getSd(gamesAll)))
                    table.add_row(("White", self.getMean(gamesStockfishWhite), self.getSd(gamesStockfishWhite)))
                    table.add_row(("Black", self.getMean(gamesStockfishBlack), self.getSd(gamesStockfishBlack)))


        with doc.create(Subsection('Plots')):
                with doc.create(Figure(position='h!')) as allGamesPlot:         
                    plt.plot(dataPointsAllGames, label="any")
                    plt.plot(dataPointsStockFishWhiteGames, label="white")
                    plt.plot(dataPointsStockFishBlackGames, label="black")
                    plt.xlabel("playes")
                    plt.ylabel("games")
                    plt.legend()
                    plt.savefig("allGamesPlot.png")
                    plt.clf()
                    allGamesPlot.add_image("allGamesPlot.png", width='300px')
                    allGamesPlot.add_caption('All games plotted against their length.')

                    plt.hist([game.getTotalMoves() for game in gamesAll], range=(0,250), label="any")
                    plt.xlabel("playes")
                    plt.ylabel("games")
                    plt.savefig("histogram.png")
                    plt.legend()
                    plt.clf()
                    allGamesPlot.add_image("histogram.png", width='300px')
                    allGamesPlot.add_caption('Histogram of all games and their lengths. Looks normally distributed with a longer tail on the right side.')

                    plt.plot(dataPointsStockFishWon, label="won")
                    plt.plot(dataPointsStockFishDrawn, label="drawn")
                    plt.plot(dataPointsStockFishLost, label="lost")
                    plt.xlabel("playes")
                    plt.ylabel("games")
                    plt.legend()
                    plt.savefig("winLossPlot.png")
                    plt.clf()
                    allGamesPlot.add_image("winLossPlot.png", width='300px')
                    allGamesPlot.add_caption('Won, drawn and lost games plotted against their length.')

        doc.generate_pdf(clean_tex=False)
        doc.generate_tex()

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
    # filename = 'TinusTexFile'
    db.createPdf()
    # openings = db.getAllPlayedOpenings()
    # print(openings)
    # print('Bird' in openings)
    # db.addOpeningsPlayedOverNTimesToPDF(filename=filename, n=50)
    # for opening in openings:
    #     new_db = ChessDatabase(db.getFilteredListOfGamesByOpening(opening))
    #     new_db.addOpeningTableToPDF(
    #         filename=filename, opening=opening, depth=0)


if __name__ == '__main__':
    main()
