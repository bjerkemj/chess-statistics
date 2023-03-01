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


def treeTraverselByLevel(tree: Tree, depth: int = 2) -> None:
    dic = {}
    run = True
    for i in range(0, depth + 1):
        dic[str(i)] = []
    children = [tree]
    while run:
        new_children = []
        for child in children:
            if child.isLeaf():
                continue
            else:
                dic[str(child.currentMove)].append(str(child))
                new_children += child.children
        if len(new_children) == 0:
            run = False
        else:
            children = new_children
            print('Begninning new loop')
    print(dic)

    for level, trees in dic.items():
        print(f'Move {level}')
        print(trees)


def generateDotFileFromTree(tree: Tree, filename: str, depth: int = 2, rootName: str = None) -> None:
    allText = getDotText(tree, depth, rootName)
    with open(filename + '.dot', 'w') as file:
        file.write(
            "digraph g {\nfontname=\"Helvetica,Arial,sans-serif\"\nnode [fontname=\"Helvetica,Arial,sans-serif\" filledcolor = \"white\" label = \"\" style = \"filled\" shape = \"circle\" ]\nedge [fontname=\"Helvetica,Arial,sans-serif\"]\ngraph [fontsize=30 labelloc=\"t\" label=\"\" splines=true overlap=false rankdir = \"LR\"];\nratio = auto;\n")
        file.write(allText)
        file.write("\n}")


def getColor(tree: Tree) -> str:
    color = tree.color
    return '\"black\"' if color == 1 else '\"white\"'


def addNode(string: str, tree: Tree) -> str:
    string += f'\"{str(tree)}\" [style = \"filled\" fillcolor = {getColor(tree)}];\n'
    string += f'{str(tree.parent)} -> {str(tree)} [label = \"{str(tree)}\"];\n'
    return string


def addRoot(string: str, tree: Tree, name: str = None) -> str:
    # print(type(string))
    # print(type(str(tree)))
    # print(str(tree))
    # print(type(string))
    # print(type(f'\"{str(tree)}\" [style = \"filled\" label = \"root\"];'))
    if not name:
        name = 'root'
    string += f'\"{str(tree)}\" [style = \"filled\" fillcolor = \"white\" label = \"{name}\"];\n'
    return string


def getDotText(tree: Tree, depth: int, rootName: str) -> str:
    string = ""
    children = tree.children
    string = addRoot(string, tree=tree, name=rootName)
    run = True
    counter = 0
    while run:
        print(f"count = {counter}")
        new_children = []
        for child in children:
            string = addNode(string, child)
            if child.isLeaf():
                continue
            else:
                new_children += child.children
        if len(new_children) == 0:
            run = False
        else:
            children = new_children
        counter += 1
    return string


def createPNGfromDotFile(filename: str) -> None:
    os.system(f"dot -Tpng {filename}.dot > {filename}.png")


if __name__ == '__main__':
    depth = 1
    filename = "leggo"
    db = ChessDatabase()
    print(db.getOpeningsPlayedOverNTimes(50))
    tree = OpeningChessTree(chessDatabase=db, depth=depth)
    print('Opening tree made -----------')
    # for child in tree.children:
    #     print(str(child))
    # print(str(tree))
    # treeTraverselByLevel(tree, depth=depth)
    generateDotFileFromTree(tree=tree, filename=filename, depth=depth)
    createPNGfromDotFile(filename)
    # print(str(tree.children[1]))

    depth2 = 3
    filename2 = "english_opening"
    db2 = ChessDatabase(db.getFilteredListOfGamesByOpening('English opening'))
    tree2 = OpeningChessTree(chessDatabase=db2, depth=depth2)
    generateDotFileFromTree(tree=tree2, filename=filename2,
                            depth=depth2, rootName='English opening')
    createPNGfromDotFile(filename2)
