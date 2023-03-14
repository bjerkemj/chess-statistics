import filecmp
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

db.saveGamesToPortableGameNotationFile("./tests/saveTestGames")

assert filecmp.cmp('Stockfish_15_64-bit.commented.[2600].pgn', "./tests/saveTestGames.pgn"), \
    f"The file created should have identical content to the original file"

os.remove("./tests/saveTestGames.pgn")


gamesWithStackedFilter = db.getAllGames()
gamesWithStackedFilter = db.filterDrawn(gamesWithStackedFilter)
gamesWithStackedFilter = db.filterStockfishWhite(gamesWithStackedFilter)

assert len(gamesWithStackedFilter) == 601, \
    f"Database should be able to stack filter. Games Stockfish won as white. Should be 601 games but was {len(gamesWithStackedFilter)}"

ongoingGames = db.getNumListOngoingGames(db.getAllGames())
elementsAreInts = all([isinstance(gameLength, int) for gameLength in ongoingGames])

assert elementsAreInts, \
    f"getNumListOngoingGames should return a list of ints but it was not a list of ints."

db.filterDatabaseByOpenings(["QGA"])

assert len(db.getAllGames()) == 30, \
    f"Database should have 30 games with the QGA opening but was {len(db.getAllGames())}"

assert db.getAllGames()[0].getOpening() == "QGA", \
    f"Databases first game should have opening QGA opening but was {db.getAllGames()[0].getOpening()}"

playedOpenings = db.getAllPlayedOpenings()

assert isinstance(playedOpenings, list), \
    f"Database function getAllPlayedOpenings should return a list but was {type(playedOpenings)}"

assert len(playedOpenings) == 1, \
    f"Database should contain 1 played opening but was {len(playedOpenings)}"

