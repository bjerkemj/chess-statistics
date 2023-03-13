import random
import string
from typing import List
from chessDatabase import ChessDatabase


def color(x): return x % 2  # 0 is white, 1 is black

def getRandomID() -> str:
    randomString = ''.join(random.choice(string.ascii_letters) for i in range(random.randint(10, 20)))
    return randomString


class Tree:

    def __str__(self) -> str:
        return f'{self.name}W{self.numGamesWonByWhite}D{self.numGamesDrawn}L{self.numGamesWonByBlack}_{self.id}'

    def getPossibleNextMoves(self, moveSequence: dict) -> List[dict]:
        games = self.chessDatabase.getAllGames()
        nextMoves = list(set([game.getMoveByNumber(
            self.currentMove + 1) for game in games if game.getMoveByNumber(
            self.currentMove + 1)]))
        listOfMoveSequences = []
        for move in nextMoves:
            moveSequenceSoFar = moveSequence.copy()
            moveSequenceSoFar[str(self.currentMove + 1)] = move
            listOfMoveSequences.append(moveSequenceSoFar)
        return listOfMoveSequences

    def isLeaf(self) -> bool:
        return not self.children


class OpeningChessTree(Tree):

    def __init__(self, chessDatabase: ChessDatabase, openings: List[str] = None, depth: int = 1) -> None:
        self.name = "root"
        self.parent = None
        self.id = getRandomID()
        self.openingsInTree = openings
        self.chessDatabase = ChessDatabase(
            chessDatabase.getFilteredListOfGamesByOpenings(self.openingsInTree))
        self.color = 0
        self.currentMove = 0
        listOfMoveSequences = self.getPossibleNextMoves(dict())
        self.numGamesWonByWhite, self.numGamesDrawn, self.numGamesWonByBlack = chessDatabase.getStatisticsByMoveSequence()
        self.children = [ChessTree(
            self, self.chessDatabase, sequence, depth) for sequence in listOfMoveSequences]


class ChessTree(Tree):

    def __init__(self, parent: Tree, chessDatabase: ChessDatabase, moveSequence: dict, depth: int) -> None:
        self.parent = parent
        self.currentMove = len(moveSequence)
        self.id = getRandomID()
        self.name = moveSequence[str(self.currentMove)]
        if '+' in self.name:
            self.name = self.name.replace('+', 'C')  # C for check
        if '#' in self.name:
            self.name = self.name.replace('#', 'CM') # CM for check mate
        if '-' in self.name:
            self.name = self.name.replace('O-O-O', 'QCastle')  # Qcastle for queenside castle
            self.name = self.name.replace('O-O', 'KCastle') # KCastle for Kindside castle
        if '=' in self.name:
            self.name = self.name.replace('=', 'P')  # P for promote
        self.numGamesWonByWhite, self.numGamesDrawn, self.numGamesWonByBlack = chessDatabase.getStatisticsByMoveSequence(
            moveSequence)
        self.color = color(self.currentMove)
        self.chessDatabase = ChessDatabase(
            chessDatabase.getFilteredListOfGamesByMoveSequence(moveSequence))
        listOfMoveSequences = self.getPossibleNextMoves(moveSequence)
        if self.currentMove <= depth and len(listOfMoveSequences) > 0:
            self.children = [ChessTree(
                self, self.chessDatabase, sequence, depth) for sequence in listOfMoveSequences]
        else:
            self.children = None


