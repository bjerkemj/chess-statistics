import os
import sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")

from chessDatabase import ChessDatabase

db = ChessDatabase()
db.addGamesFromPortabelGameNotationFile()

assert len(db.getAllGames()) == 2600, \
    f"Database should have 2600 games but was {len(db.getAllGames())}"

assert len(db.filterByMoves(db.getAllGames(), 414)) == 1, \
    f"Database should have 1 game with more than 414 moves but was {len(db.filterByMoves(db.getAllGames(), 414))}"

assert len(db.filterStockfishWhite(db.getAllGames())) == 1301, \
    f"Database should have 1301 games with Stockfish as white but was {len(db.filterStockfishWhite(db.getAllGames()))}"

assert len(db.filterStockfishBlack(db.getAllGames())) == 1299, \
    f"Database should have 1299 games with Stockfish as white but was {len(db.filterStockfishBlack(db.getAllGames()))}"

assert len(db.filterStockfishWon(db.getAllGames())) == 992, \
    f"Database should have 992 games with Stockfish winning but was {len(db.filterStockfishWon(db.getAllGames()))}"

gamesWithStackedFilter = db.getAllGames()
gamesWithStackedFilter = db.filterDrawn(gamesWithStackedFilter)
gamesWithStackedFilter = db.filterStockfishWhite(gamesWithStackedFilter)

assert len(gamesWithStackedFilter) == 601, \
    f"Database should be able to stack filter. Games Stockfish won as white. Should 601 games but was {len(gamesWithStackedFilter)}"

ongoingGames = db.getNumListOngoingGames(db.getAllGames())
elementsAreInts = all([isinstance(gameLength, int) for gameLength in ongoingGames])

assert elementsAreInts, \
    f"getNumListOngoingGames should return a list of ints but it was not a list of ints."