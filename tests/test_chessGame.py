# 0: Imports
# ----------
import os
import sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")

from chessGame import ChessGame
import filecmp

# 1: Tests
# --------
cg1 = None
str = ""
with open(os.path.join(ROOT, "testGame.pgn"), "r") as f:
    for line in f:
        str += line

cg1 = ChessGame(str)

assert cg1.getStockfishWon() == True, \
    f"Stockfish won should be True but was {cg1.getStockfishWon()}"

assert cg1.getDraw() == False, \
    f"Game drawn should be False but was {cg1.getDraw()}"

assert cg1.getTotalMoves() == 99, \
    f"Game total moves should be 99 but was {cg1.getTotalMoves()}"

assert cg1.getMoveByNumber(4) == "Bg4", \
    f"Game move 4 should be Bg4 but was {cg1.getMoveByNumber()}"

assert cg1.getOpening() == "Bird's opening", \
    f"Game opening should be 'Bird's opening' but was {cg1.getOpening()}"

cg1.savePng("./tests/saveTestGame")
assert filecmp.cmp('./tests/testGame.pgn', './tests/saveTestGame.pgn'), \
    f"The file created should have identical content to the original file"
os.remove("./tests/saveTestGame.pgn")

cg2 = ChessGame(xlsxName="./tests/testGame")

assert cg2.getOpening() == cg1.getOpening(), \
    f"Game loaded from excel's opening should be the same the original games but the opening was {cg2.getOpening()} and should be {cg1.getOpening()}"

assert cg2.getTotalMoves() == cg1.getTotalMoves(), \
    f"Game loaded from excel's opening should be the same the original games but the total moves was {cg2.getTotalMoves()} and should be {cg1.getTotalMoves()}"

assert cg2.getMoveByNumber(1) == cg1.getMoveByNumber(1), \
    f"Game loaded from excel's opening should be the same the original games but the first move was {cg2.getMoveByNumber(1)} and should be {cg1.getMoveByNumber(1)}"

assert cg2.getMoveByNumber(99) == cg1.getMoveByNumber(99), \
    f"Game loaded from excel's opening should be the same the original games but the first move was {cg2.getMoveByNumber(99)} and should be {cg1.getMoveByNumber(99)}"
