# 0: Imports
# ----------
import os
import sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT+"/..")

from chessDatabase import ChessDatabase
import chessOpeningTree

# 1: Tests
# --------


# 1.1 Single game test
# --------
cg1 = None
str = ""
with open(os.path.join(ROOT, "testGame.pgn"), "r") as f:
    for line in f:
        str += line

db = ChessDatabase()
db._addGame(pgn=str)

basicOpeningChessTree = chessOpeningTree.OpeningChessTree(db, depth=1000)

assert basicOpeningChessTree.numGamesWonByWhite == 1, \
    f'Number og games won by white should be 1 but was {basicOpeningChessTree.numGamesWonByWhite}'

assert basicOpeningChessTree.numGamesWonByBlack == 0, \
    f'Number og games won by white should be 0 but was {basicOpeningChessTree.numGamesWonByBlack}'
    
assert basicOpeningChessTree.numGamesDrawn == 0, \
    f'Number og games won by white should be 0 but was {basicOpeningChessTree.numGamesDrawn}'

child = basicOpeningChessTree.children[0]
while not child.isLeaf():
    child = child.children[0]

assert child.currentMove == 99, \
    f'Depth of tree should be 99 but was {child.currentMove}'


# 1.2 All games test
# --------

new_db = ChessDatabase([])

new_db.addGamesFromPortabelGameNotationFile()

sys.setrecursionlimit(10000)
completeOpeningChessTree = chessOpeningTree.OpeningChessTree(new_db, depth = 10000)
sys.setrecursionlimit(1000)

assert completeOpeningChessTree.numGamesWonByWhite == 704, \
    f'Number og games won by white should be 704 but was {completeOpeningChessTree.numGamesWonByWhite}'

assert completeOpeningChessTree.numGamesWonByBlack == 296, \
    f'Number og games won by white should be 296 but was {completeOpeningChessTree.numGamesWonByBlack}'
    
assert completeOpeningChessTree.numGamesDrawn == 1600, \
    f'Number og games won by white should be 1600 but was {completeOpeningChessTree.numGamesDrawn}'

    
maxDepth = 0
children = completeOpeningChessTree.children
leaves = []
while len(children) > 0:
    new_children = []
    maxDepth +=1
    for child in children:
        if child.children:
            new_children += child.children
        else:
            leaves.append(child)
    children = new_children
    if maxDepth == 10:
        childrenDepth10 = children


assert maxDepth == 419, \
    f'The maximum length game should be 419 but was {maxDepth}'


# Test that statistics is correct for leaves
numGamesWonByWhite = 0
numGamesWonByBlack = 0
numGamesDrawn = 0
for leafe in leaves:
    numGamesWonByWhite += leafe.numGamesWonByWhite
    numGamesWonByBlack += leafe.numGamesWonByBlack
    numGamesDrawn += leafe.numGamesDrawn
        
assert numGamesWonByWhite == 704, \
    f'Number of games won by white should be 704 but was {numGamesWonByWhite}'

assert numGamesWonByBlack == 296, \
    f'Number of games won by white should be 296 but was {numGamesWonByBlack}'
    
assert numGamesDrawn == 1600, \
    f'Number of games won by white should be 1600 but was {numGamesDrawn}'
     

# Test that statistics is correct for depth 10 in the tree
numGamesWonByWhite = 0
numGamesWonByBlack = 0
numGamesDrawn = 0
for tree in childrenDepth10:
    numGamesWonByWhite += tree.numGamesWonByWhite
    numGamesWonByBlack += tree.numGamesWonByBlack
    numGamesDrawn += tree.numGamesDrawn

assert numGamesWonByWhite == 704, \
    f'Number og games won by white should be 704 but was {numGamesWonByWhite}'

assert numGamesWonByBlack == 296, \
    f'Number og games won by white should be 296 but was {numGamesWonByBlack}'
    
assert numGamesDrawn == 1600, \
    f'Number og games won by white should be 1600 but was {numGamesDrawn}'


