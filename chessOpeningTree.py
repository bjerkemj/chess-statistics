from typing import List
from chessDatabase import ChessDatabase
from chessGame import ChessGame
import os


def color(x): return x % 2  # 0 is white, 1 is black


class Tree:

    def __str__(self) -> str:
        return f'{self.name}_W{self.numGamesWonByWhite}_D{self.numGamesDrawn}_L{self.numGamesWonByBlack}'

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
        self.openingsInTree = openings
        self.chessDatabase = ChessDatabase(
            chessDatabase.getFilteredListOfGamesByOpenings(self.openingsInTree))
        self.color = 0
        self.currentMove = 0
        nextMoves = list(set([game.getMoveByNumber(
            self.currentMove + 1) for game in chessDatabase.getAllGames() if game.getMoveByNumber(
            self.currentMove + 1)]))
        listOfMoveSequences = []
        for move in nextMoves:
            listOfMoveSequences.append({str(self.currentMove + 1): move})
        # print(listOfMoveSequences)
        self.numGamesWonByWhite, self.numGamesDrawn, self.numGamesWonByBlack = chessDatabase.getStatisticsByMoveSequence()
        self.children = [ChessTree(
            self, self.chessDatabase, sequence, depth) for sequence in listOfMoveSequences]


class ChessTree(Tree):

    def __init__(self, parent: Tree, chessDatabase: ChessDatabase, moveSequence: dict, depth: int) -> None:
        self.parent = parent
        self.currentMove = len(moveSequence)
        self.name = moveSequence[str(self.currentMove)]
        if '+' in self.name:
            self.name = self.name.replace('+', 'P')  # P for pluss
        if '-' in self.name:
            self.name = self.name.replace('-', 'CAST')  # CAST for castle
        if '=' in self.name:
            self.name = self.name.replace('=', 'U')  # U for promote
        # print(
        #     f'Making new tree for moveNumber = {self.currentMove} and move = {self.name}')

        self.numGamesWonByWhite, self.numGamesDrawn, self.numGamesWonByBlack = chessDatabase.getStatisticsByMoveSequence(
            moveSequence)
        self.color = color(self.currentMove)
        self.chessDatabase = ChessDatabase(
            chessDatabase.getFilteredListOfGamesByMoveSequence(moveSequence))
        listOfMoveSequences = self.getPossibleNextMoves(moveSequence)
        if self.currentMove <= depth:
            self.children = [ChessTree(
                self, self.chessDatabase, sequence, depth) for sequence in listOfMoveSequences]
        else:
            self.children = None


if __name__ == '__main__':
    depth = 2
    filename = "sicko"
    db = ChessDatabase()
    print(db.getOpeningsPlayedOverNTimes(50))
    tree = OpeningChessTree(chessDatabase=db, depth=depth)
    print('Opening tree made -----------')
