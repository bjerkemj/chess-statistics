from chessDatabase import ChessDatabase
from pylatex import (
    MultiColumn,
    Table,
    Document,
    Section,
    Subsection,
    Command,
    Tabular,
    Center,
    TikZ,
    Axis,
    Plot,
    LineBreak,
    NewLine,
    Figure,
    StandAloneGraphic,
    NewPage,
)
from pylatex.utils import italic, NoEscape
from matplotlib import pyplot as plt
import numpy as np


class PDFCreator:
    def __init__(self, chessDatabase: ChessDatabase, filename: str) -> None:
        self.doc = Document(filename)
        self.tableNumber = 0
        self.chessDatabase = chessDatabase

    def makeTitle(self, title: str = "Stockfish chess statistics", authors: str = "Tinus F Alsos and Johan Bjerkem"):
        self.doc.preamble.append(Command("title", title))
        self.doc.preamble.append(Command("author", authors))
        self.doc.preamble.append(Command("date", NoEscape(r"\today")))
        self.doc.append(NoEscape(r"\maketitle"))

    

    def createTable(self, size, data, tableCaption: str = ''):
        self.tableNumber += 1
        tableCaption = f'Table {self.tableNumber}: ' + tableCaption
        self.doc.append(NewLine())
        columns = len(size.replace('|', '').replace(' ', ''))
        rows = int(len(data)/columns)
        with self.doc.create(Tabular(size)) as table:
            print(f'Table with catpion: {tableCaption}')
            print(f'Has rows: {rows}')
            print(f'Has columns: {columns}')

            for i in range(rows):
                rowInfo = []
                for j in range(columns):
                    rowInfo.append(data[i * columns + j])
                table.add_row(rowInfo)
                if i == 0:
                    table.add_hline()
            table.add_row([MultiColumn(columns, align='l', data=tableCaption)])
        self.doc.append(NewLine())
        self.doc.append(NewLine())
        

    def createPlot(self, datapoints, label, xlabel, ylabel, filename):
        for i, points in enumerate(datapoints):
            plt.plot(points, label=label[i])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.savefig(filename + ".png")
        plt.clf()

    def addText(self, text: str) -> None:
        self.doc.append(text)
        self.doc.append(NewLine())

    def addSection(self, sectionCaption: str) -> None:
        with self.doc.create(Section(sectionCaption)):
            pass

    def addSubSection(self, subSectionCaption: str) -> None:
        with self.doc.create(Subsection(subSectionCaption)):
            pass

    def createPdfExample(self, db: ChessDatabase):
        database = db.getStatsDictionary()

        self.makeTitle()

        introductionText = "In this document we will present tables, graphs and statistics about 2600 chess games played by the chess engine Stockfish. The game information is gathered from the document 'Stockfish_15_64-bit.commented.[2600].pgn'. Hopefully you find the data insightful."

        sectionCaption = 'Plots and Tables'
        sectionText = "In this section you will see statistics about all the games presented in plots and tables. This means 2600 games where Stockfish was either black or white and where Stockfish won, draw or lost"
        
        subSectionCaption1 = 'Plots'
        subSectionText1 = "Here we present a number of plots from the chess database. This corresponds to task 7."

        subSectionCaption2 = 'Tables'
        subSectionText2 = "Here we present a number og tables from the chess database. This corresponds to task 8."

        sectionCaption2 = "Trees and openings"
        sectionText2 = "In this section, we will display some opening trees and different table statistics for winrates by openings. We hope you enjoy."

        self.addText(introductionText)
        self.addSection(sectionCaption=sectionCaption)
        self.addText(sectionText)
        self.addSubSection(subSectionCaption1)
        self.addText(subSectionText1)

        with self.doc.create(Figure(position="h!")) as allGamesPlot:
            datapoints = [
                database["dataPointsAllGames"],
                database["dataPointsStockFishWhiteGames"],
                database["dataPointsStockFishBlackGames"],
            ]
            labels = ["All games", "Stockfish white", "Stockfish black"]
            self.createPlot(
                datapoints, labels, "turns", "games", "allGamesPlot"
            )
            allGamesPlot.add_image("allGamesPlot.png", width="200px")
            allGamesPlot.add_caption("All games plotted against their length.")

        with self.doc.create(Figure(position="h!")) as histoPlot:
            plt.hist(
                [game.getTotalMoves() for game in database["gamesAll"]],
                range=(0, 250),
                label="any",
            )
            plt.xlabel("turns")
            plt.ylabel("games")
            plt.legend()
            plt.savefig("histogram.png")
            plt.clf()
            histoPlot.add_image("histogram.png", width="200px")
            histoPlot.add_caption(
                "Histogram of all games and their lengths. Looks normally distributed with a longer tail on the right side."
            )


        with self.doc.create(Figure(position="h!")) as winLossPlot:
            datapoints = [
                database["dataPointsStockFishWon"],
                database["dataPointsStockFishDrawn"],
                database["dataPointsStockFishLost"],
            ]
            labels = ["Stockfish won", "Stockfish draw", "Stockfish lost"]
            self.createPlot(datapoints, labels, "turns", "games", "winLossPlot")
            winLossPlot.add_image("winLossPlot.png", width="200px")
            winLossPlot.add_caption("All games plotted against their length.")

        with self.doc.create(Figure(position="h!")) as boxPlot:
            data = [
                [
                    game.getTotalMoves()
                    for game in database["gamesStockfishWon"]
                ],
                [
                    game.getTotalMoves()
                    for game in database["gamesStockfishDrawn"]
                ],
                [
                    game.getTotalMoves()
                    for game in database["gamesStockfishLost"]
                ],
            ]
            plt.boxplot(
                data, patch_artist=True, labels=["Wins", "Drawn", "Losses"]
            )
            plt.savefig("boxplot.png")
            plt.clf()
            boxPlot.add_image("boxplot.png", width="150px")
            boxPlot.add_caption(
                "Boxplots representing the win, drawn and loss statistics of Stockfish."
            )

        self.addSubSection(subSectionCaption2)
        self.addText(subSectionText2)

        tableCaption = "Results of Stockfish's games."


        self.createTable('l|rrr', ["Color/Result", "Wins", "Draws", "Losses", "Any", len(database["gamesStockfishWon"]), len(database["gamesStockfishDrawn"]), len(database["gamesStockfishLost"]), "White", len(database["gamesWhiteStockfishWon"]), len(database["gamesWhiteStockfishDrawn"]), len(database["gamesWhiteStockfishLost"]), "Black", len(database["gamesBlackStockfishWon"]), len(database["gamesBlackStockfishDrawn"]), len(database["gamesBlackStockfishLost"])], tableCaption)
        tableCaption = "Length of games played by stockfish."

        self.createTable(
            "l|rr",
            [
                "Identifier/Statistic",
                "Mean",
                "SD",
                "All games",
                db.getMean(database["gamesAll"]),
                db.getSd(database["gamesAll"]),
                "White",
                db.getMean(database["gamesStockfishWhite"]),
                db.getSd(database["gamesStockfishWhite"]),
                "Black",
                db.getMean(database["gamesStockfishBlack"]),
                db.getSd(database["gamesStockfishBlack"]),
                "Win",
                db.getMean(database["gamesStockfishWon"]),
                db.getSd(database["gamesStockfishWon"]),
                "Draw",
                db.getMean(database["gamesStockfishDrawn"]),
                db.getSd(database["gamesStockfishDrawn"]),
                "Lost",
                db.getMean(database["gamesStockfishLost"]),
                db.getSd(database["gamesStockfishLost"]),
            ], tableCaption
        )

        self.addSection(sectionCaption=sectionCaption2)
        self.addText(sectionText2)

        subsectionCaption = 'Stockfish Opening Winrate'
        numGamesPlayed = 100
        subsectionText = f'We start by displaying the statistics for the openings that are played more than {numGamesPlayed} times.'
        self.addSubSection(subsectionCaption)
        self.addText(subsectionText)
        self.addOpeningsPlayedOverNTimesToPDF(self.chessDatabase, numGamesPlayed)

        subsectionCaption = 'Opening Trees'
        subsectionText = 'We proceed with showing some opening trees to see what the best openings are. The color of a node indicates which color\'s turn it is to move. The edge from a node to another node contains the move that is being made, along with statistics on the winrate of doing that move. It is on the following format: MOVE W:numberOfWinsForWhiteIfMoveIsPlayed, D:numberOfDrawsIfMoveIsPlayed, L:numberOfLossesForWhiteIfMoveIsPlayed. L is equivelant to number of wins for black.'
        moreSubsectionText = 'We can make trees for any opening played in the database used. We start with showing a tree going to move 2 for all openings.'

        self.addSubSection(subSectionCaption=subsectionCaption)
        self.addText(subsectionText)
        self.addText(moreSubsectionText)


    #Må fikses
    def createPNGfromDotFile(filename: str) -> None:
        os.system(f"dot -Tpng {filename}.dot > {filename}.png")
    #Må fikses
    def generateDotFileFromTree(tree: Tree, filename: str, depth: int = 2, rootName: str = None) -> None:
        allText = getDotText(tree, depth, rootName)
        with open(filename + '.dot', 'w') as file:
            file.write(
                "digraph g {\nfontname=\"Helvetica,Arial,sans-serif\"\nnode [fontname=\"Helvetica,Arial,sans-serif\" filledcolor = \"white\" label = \"\" style = \"filled\" shape = \"circle\" ]\nedge [fontname=\"Helvetica,Arial,sans-serif\"]\ngraph [fontsize=30 labelloc=\"t\" label=\"\" splines=true overlap=false rankdir = \"LR\"];\nratio = auto;\n")
            file.write(allText)
            file.write("\n}")
    #Må fikses
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

    def addOpeningsPlayedOverNTimesToPDF(self, chessDatabase: ChessDatabase, n: int = 50) -> None:
        openingsDict = chessDatabase.getOpeningsPlayedOverNTimes(n=n)
        for opening in openingsDict.keys():
            print(opening)
            new_db = ChessDatabase(
                chessDatabase.getFilteredListOfGamesByOpening(opening))
            self.addOpeningTableToPDF(new_db, opening=opening)

    def addOpeningTableToPDF(self, chessDatabase: ChessDatabase, opening: str) -> None:
        statsDictionary = chessDatabase.getStatsDictionary()
        self.createTable('l|rrrr', ["Color", "Wins", "Draws", "Losses", "Total", "Any", statsDictionary["numGamesStockfishWon"],statsDictionary["numGamesStockfishDrawn"],statsDictionary["numGamesStockfishLost"],statsDictionary["numGamesAll"],'White',statsDictionary["numGamesWhiteStockfishWon"],statsDictionary["numGamesWhiteStockfishDrawn"],statsDictionary["numGamesWhiteStockfishLost"],statsDictionary["numGamesWhiteStockfishAll"],'Black',statsDictionary["numGamesBlackStockfishWon"],statsDictionary["numGamesBlackStockfishDrawn"],statsDictionary["numGamesBlackStockfishLost"],statsDictionary["numGamesBlackStockfishAll"]], tableCaption= f'Statistics for opening: {opening}.')
        
    def generate_pdf(self) -> None:
        self.doc.generate_pdf(clean_tex=False)


def main():
    db = ChessDatabase()

    pdf = PDFCreator(chessDatabase = db, filename='test')

    pdf.createPdfExample(db)
    # pdf.addOpeningsPlayedOverNTimesToPDF(db)
    pdf.generate_pdf()
    # pdf.createTable(
    #                 "l|rr",
    #                 [
    #                     "Identifier/Statistic",
    #                     "Mean",
    #                     "SD",
    #                     "All games",
    #                     0,
    #                     1,
    #                     "White",
    #                     2,
    #                     3,
    #                     "Black",
    #                     4,5,
    #                     "Win",
    #                     6,7,
    #                     "Draw",
    #                     8,9,
    #                     "Lost",
    #                     10,11,
    #                 ],
    #             )
    # pdf.generate_pdf()

    # text = ''
    # text2 = ''
    # for i in range(30):
    #     text += 'aaaaaa '
    #     text2 += 'bbbbbb '
    # pdf.addSection('Skrrt')
    # pdf.addText(text)
    # pdf.addSubSection('SubsSkrrrt')
    # pdf.addText(text2)
    # pdf.generate_pdf()


    


if __name__ == "__main__":
    main()
