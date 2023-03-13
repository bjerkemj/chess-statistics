from chessGame import ChessGame
import os
import math
from typing import List
ROOT = os.path.dirname(os.path.abspath(__file__))

class ChessDatabase:
    def __init__(self, games: List[ChessGame] = []) -> None:
        self.games = games

    def getAllGames(self) -> List[ChessGame]:
        return self.games

    def getTotalMovesOfGames(self, games: List[ChessGame]) -> int:
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

    def getMean(self, games: list) -> float:
        return round(sum([game.getTotalMoves() for game in games])/len(games), 2)

    def getSd(self, games: list) -> float:
        mean = self.getMean(games)
        return round(math.sqrt(sum([abs(game.getTotalMoves() - mean) for game in games])/len(games)), 2)

    def _addGame(self, pgn: str) -> None:
        self.games.append(ChessGame(pgn))

    def addGamesFromPortabelGameNotationFile(self, fileName: str = "Stockfish_15_64-bit.commented.[2600].pgn") -> None:
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
    
    def filterDatabaseMoveSequence(self, moveSequence: dict) -> None:
        if moveSequence:
            self.games = [game for game in self.games if all([game.getMoveByNumber(moveNumber) == move for moveNumber, move in moveSequence.items()])]

    def getFilteredListOfGamesByOpening(self, opening: str) -> List[ChessGame]:
        return [game for game in self.games if game.getOpening() == opening]

    def getFilteredListOfGamesByOpenings(self, openings: List[str]) -> List[ChessGame]:
        if not openings:
            return self.getAllGames()
        return [game for game in self.games if game.getOpening() in openings]
    
    def filterDatabaseByOpenings(self, openings: List[str]) -> None:
        if not openings:
            pass
        else:
            self.games = [game for game in self.games if game.getOpening() in openings]

    def getStatisticsByMoveSequence(self, moveSequence: dict = {}) -> tuple:
        games = self.getFilteredListOfGamesByMoveSequence(
            moveSequence=moveSequence)
        numGames = len(games)
        gamesWonByWhite = [game for game in games if game.getWhiteWon()]
        numGamesWonByWhite = len(gamesWonByWhite)
        gamesDrawn = [game for game in games if game.getDraw()]
        numGamesDrawn = len(gamesDrawn)
        numGamesWonByBlack = numGames - numGamesDrawn - numGamesWonByWhite
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
        onGoingWon= self.getNumListOngoingGames(gamesStockfishWon)
        onGoingDrawn= self.getNumListOngoingGames(gamesStockfishDrawn)
        onGoingLost = self.getNumListOngoingGames(gamesStockfishLost)

        dataPointsAllGames = self.getDataPoints(onGoing)
        dataPointsStockFishWhiteGames = self.getDataPoints(onGoingWhite)
        dataPointsStockFishBlackGames = self.getDataPoints(onGoingBlack)
        dataPointsStockFishWon= self.getDataPoints(onGoingWon)
        dataPointsStockFishDrawn= self.getDataPoints(onGoingDrawn)
        dataPointsStockFishLost = self.getDataPoints(onGoingLost)

        statsDictionary = {'gamesAll': gamesAll, 'gamesStockfishWhite': gamesStockfishWhite, 'gamesStockfishBlack': gamesStockfishBlack, 'gamesStockfishWon': gamesStockfishWon, 'gamesStockfishDrawn': gamesStockfishDrawn, 'gamesStockfishLost': gamesStockfishLost, 'gamesWhiteStockfishWon': gamesWhiteStockfishWon, 'gamesWhiteStockfishDrawn': gamesWhiteStockfishDrawn, 'gamesWhiteStockfishLost': gamesWhiteStockfishLost, 'gamesBlackStockfishWon': gamesBlackStockfishWon, 'gamesBlackStockfishDrawn': gamesBlackStockfishDrawn, 'gamesBlackStockfishLost': gamesBlackStockfishLost, 'onGoing': onGoing, 'onGoingWhite': onGoingWhite, 'onGoingBlack': onGoingBlack,
                           'dataPointsAllGames': dataPointsAllGames, 'dataPointsStockFishWhiteGames': dataPointsStockFishWhiteGames, 'dataPointsStockFishBlackGames': dataPointsStockFishBlackGames, 'dataPointsStockFishWon': dataPointsStockFishWon, 'dataPointsStockFishDrawn': dataPointsStockFishDrawn, 'dataPointsStockFishLost': dataPointsStockFishLost, 'numGamesAll': len(gamesAll), 'numGamesStockfishWon': len(gamesStockfishWon), 'numGamesStockfishDrawn': len(gamesStockfishDrawn), 'numGamesStockfishLost': len(gamesStockfishLost), 'numGamesWhiteStockfishWon': len(gamesWhiteStockfishWon), 'numGamesWhiteStockfishDrawn': len(gamesWhiteStockfishDrawn), 'numGamesWhiteStockfishLost': len(gamesWhiteStockfishLost), 'numGamesWhiteStockfishAll': numWhiteStockfishAll, 'numGamesBlackStockfishAll': numBlackStockfishAll, 'numGamesBlackStockfishWon': len(gamesBlackStockfishWon), 'numGamesBlackStockfishDrawn': len(gamesBlackStockfishDrawn), 'numGamesBlackStockfishLost': len(gamesBlackStockfishLost)}
        return statsDictionary
    
if __name__ == '__main__':
    db = ChessDatabase()
    db.addGamesFromPortabelGameNotationFile()
    print(max(db.getTotalMovesOfGames(db.games)))
    print(len([game for game in db.games if game.whiteWon]))
    print(len([game for game in db.games if game.draw]))
    print(len([game for game in db.games if not game.draw and not game.whiteWon]))


