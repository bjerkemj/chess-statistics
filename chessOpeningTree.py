import random
import string
from typing import List
from chessDatabase import ChessDatabase
from chessGame import ChessGame
import os

import uuid


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
        # nextMoves = list(set([game.getMoveByNumber(
        #     self.currentMove + 1) for game in chessDatabase.getAllGames() if game.getMoveByNumber(
        #     self.currentMove + 1)]))
        # listOfMoveSequences = []
        # for move in nextMoves:
        #     listOfMoveSequences.append({str(self.currentMove + 1): move})
        # print(listOfMoveSequences)
        listOfMoveSequences = self.getPossibleNextMoves(dict())
        self.numGamesWonByWhite, self.numGamesDrawn, self.numGamesWonByBlack = chessDatabase.getStatisticsByMoveSequence()
        self.children = [ChessTree(
            self, self.chessDatabase, sequence, depth) for sequence in listOfMoveSequences]


class ChessTree(Tree):

    def __init__(self, parent: Tree, chessDatabase: ChessDatabase, moveSequence: dict, depth: int) -> None:
        self.parent = parent
        self.currentMove = len(moveSequence)
        # print('New tree ', self.currentMove)
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
