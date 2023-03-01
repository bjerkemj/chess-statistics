from chessDatabase import ChessDatabase
from pylatex import (
    Document,
    Section,
    Subsection,
    Command,
    Tabular,
    TikZ,
    Axis,
    Plot,
    LineBreak,
    Figure,
    StandAloneGraphic,
    NewPage,
)
from pylatex.utils import italic, NoEscape
from matplotlib import pyplot as plt
import numpy as np


class PDFCreator:
    def __init__(self, filename: str) -> None:
        self.doc = Document(filename)

    def makeTitle(self, title: str = "Stockfish chess statistics", authors: str = "Tinus F Alsos and Johan Bjerkem"):
        self.doc.preamble.append(Command("title", title))
        self.doc.preamble.append(Command("author", authors))
        self.doc.preamble.append(Command("date", NoEscape(r"\today")))
        self.doc.append(NoEscape(r"\maketitle"))

    

    def createTable(self, size, data):
        with self.doc.create(Tabular(size)) as table:
            rows = int(len(data) / (len(size) - 1))
            columns = int(len(data) / rows)
            for i in range(rows):
                rowInfo = []
                for j in range(columns):
                    rowInfo.append(data[i * columns + j])
                table.add_row(rowInfo)
                if i == 0:
                    table.add_hline()

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
        subSectionText2 = "Here we present a number og tables from the chess database. This corresponds to task 8"

        self.addText(introductionText)
        self.addSection(sectionCaption=sectionCaption)
        self.addText(sectionText)
        self.addSubSection(subSectionCaption1)
        self.addText(subSectionText1)


        self.addSubSection(subSectionCaption2)
        self.addText(subSectionText2)

        with self.doc.create(Section("Plots and tables")):
            self.doc.append(
                "In this section you will see statistics about all the games presented in plots and tables. This means 2600 games where Stockfish was either black or white and where Stockfish won, draw or lost"
            )

            with self.doc.create(Subsection("Plots")):
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

            with self.doc.create(Subsection("Tables")):
                self.doc.append("Table showing the results of Stockfish games.")

                self.doc.append(LineBreak())

                self.createTable('l|rrr', ["Color/Result", "Wins", "Draws", "Losses", "Any", len(database["gamesStockfishWon"]), len(database["gamesStockfishDrawn"]), len(database["gamesStockfishLost"]), "White", len(database["gamesWhiteStockfishWon"]), len(database["gamesWhiteStockfishDrawn"]), len(database["gamesWhiteStockfishLost"]), "Black", len(database["gamesBlackStockfishWon"]), len(database["gamesBlackStockfishDrawn"]), len(database["gamesBlackStockfishLost"])])

                self.doc.append(LineBreak())
                self.doc.append(LineBreak())

                self.doc.append(
                    "Table showing the mean and SD for the length of games Stockfish played."
                )
                self.doc.append(LineBreak())
                self.doc.append(LineBreak())

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
                    ],
                )

        self.generate_pdf()
        # doc.generate_tex()

    def generate_pdf(self) -> None:
        self.doc.generate_pdf(clean_tex=False)


def main():
    pdf = PDFCreator('test')
    db = ChessDatabase()

    pdf.createPdfExample(db)
    pdf.generate_pdf()
    pdf.createTable(
                    "l|rr",
                    [
                        "Identifier/Statistic",
                        "Mean",
                        "SD",
                        "All games",
                        0,
                        1,
                        "White",
                        2,
                        3,
                        "Black",
                        4,5,
                        "Win",
                        6,7,
                        "Draw",
                        8,9,
                        "Lost",
                        10,11,
                    ],
                )
    pdf.generate_pdf()

    text = ''
    text2 = ''
    for i in range(30):
        text += 'aaaaaa '
        text2 += 'bbbbbb '
    pdf.addSection('Skrrt')
    pdf.addText(text)
    pdf.addSubSection('SubsSkrrrt')
    pdf.addText(text2)
    pdf.generate_pdf()


    


if __name__ == "__main__":
    main()
