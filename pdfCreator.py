from chessDatabase import ChessDatabase
from pylatex import Document, Section, Subsection, Command, Tabular, TikZ, Axis, Plot, LineBreak, Figure, StandAloneGraphic, NewPage
from pylatex.utils import italic, NoEscape
from matplotlib import pyplot as plt
import numpy as np


class PDFCreator:
    def __init__(self):
        pass

    def makeTitle(self, doc):
        doc.preamble.append(Command('title', 'Stockfish chess statistics'))
        doc.preamble.append(Command('author', 'Tinus F Alsos and Johan Bjerkem'))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))

    def createTable(self, doc, size, data):
        with doc.create(Tabular(size)) as table:
            rows = int(len(data)/(len(size)-1))
            columns = int(len(data)/rows)
            for i in range(rows):
                rowInfo = []
                for j in range(columns):
                    rowInfo.append(data[i*columns+j])
                table.add_row(rowInfo)
                if i==0:
                    table.add_hline()

    def createPlot(self, datapoints, label, xlabel, ylabel, filename):
        for i, points in enumerate(datapoints):
            plt.plot(points, label=label[i])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.savefig(filename + ".png")
        plt.clf()

    def createPdf(self, db: ChessDatabase, fileName: str = 'report'):
        database = db.getStatsDictionary()

        doc = Document(fileName)
        
        self.makeTitle(doc)

        doc.append("In this document i will present tables, graphs and statistics about 2600 chess games played by the chess engine Stockfish. The game information is gathered from the document 'Stockfish_15_64-bit.commented.[2600].pgn'. Hopefully you find the data insightful.")

        with doc.create(Section('Plots and tables')):
                doc.append("In this section you will see statistics about all the games presented in plots and tables. This means 2600 games where Stockfish was either black or white and where Stockfish won, draw or lost")
                  
                with doc.create(Subsection('Plots')):
                    with doc.create(Figure(position='h!')) as allGamesPlot:
                        datapoints = [database["dataPointsAllGames"], database["dataPointsStockFishWhiteGames"], database["dataPointsStockFishBlackGames"]]
                        labels = ["All games", "Stockfish white", "Stockfish black"]
                        self.createPlot(datapoints, labels, "turns", "games", "allGamesPlot")
                        allGamesPlot.add_image("allGamesPlot.png", width='200px')
                        allGamesPlot.add_caption("All games plotted against their length.")

                    with doc.create(Figure(position='h!')) as histoPlot:         
                        plt.hist([game.getTotalMoves() for game in database["gamesAll"]], range=(0,250), label="any")
                        plt.xlabel("turns")
                        plt.ylabel("games")
                        plt.legend()
                        plt.savefig("histogram.png")
                        plt.clf()
                        histoPlot.add_image("histogram.png", width='200px')
                        histoPlot.add_caption('Histogram of all games and their lengths. Looks normally distributed with a longer tail on the right side.')

                    with doc.create(Figure(position='h!')) as winLossPlot:
                        datapoints = [database["dataPointsStockFishWon"], database["dataPointsStockFishDrawn"], database["dataPointsStockFishLost"]]
                        labels = ["Stockfish won", "Stockfish draw", "Stockfish lost"]
                        self.createPlot(datapoints, labels, "turns", "games", "winLossPlot")
                        winLossPlot.add_image("winLossPlot.png", width='200px')
                        winLossPlot.add_caption("All games plotted against their length.")

                    with doc.create(Figure(position='h!')) as boxPlot:
                        data = [[game.getTotalMoves() for game in database["gamesStockfishWon"]], [game.getTotalMoves() for game in database["gamesStockfishDrawn"]], [game.getTotalMoves() for game in database["gamesStockfishLost"]]]
                        plt.boxplot(data,patch_artist=True,labels=['Wins', 'Drawn', 'Losses'])
                        plt.savefig("boxplot.png")
                        plt.clf()
                        boxPlot.add_image("boxplot.png", width='150px')
                        boxPlot.add_caption("Boxplots representing the win, drawn and loss statistics of Stockfish.")

                
                with doc.create(Subsection('Tables')):
                    doc.append("Table showing the results of Stockfish games.")

                    doc.append(LineBreak())
                    
                    self.createTable(doc, 'l|rrr', ["Color/Result", "Wins", "Draws", "Losses", "Any", len(database["gamesStockfishWon"]), len(database["gamesStockfishDrawn"]), len(database["gamesStockfishLost"]), "White", len(database["gamesWhiteStockfishWon"]), len(database["gamesWhiteStockfishDrawn"]), len(database["gamesWhiteStockfishLost"]), "Black", len(database["gamesBlackStockfishWon"]), len(database["gamesBlackStockfishDrawn"]), len(database["gamesBlackStockfishLost"])])

                    doc.append(LineBreak())
                    doc.append(LineBreak())

                    doc.append("Table showing the mean and SD for the length of games Stockfish played.")
                    doc.append(LineBreak())
                    doc.append(LineBreak())

                    self.createTable(doc, 'l|rr', ["Identifier/Statistic", "Mean", "SD", "All games", db.getMean(database["gamesAll"]), db.getSd(database["gamesAll"]), "White", db.getMean(database["gamesStockfishWhite"]), db.getSd(database["gamesStockfishWhite"]), "Black", db.getMean(database["gamesStockfishBlack"]), db.getSd(database["gamesStockfishBlack"]), "Win", db.getMean(database["gamesStockfishWon"]), db.getSd(database["gamesStockfishWon"]), "Draw", db.getMean(database["gamesStockfishDrawn"]), db.getSd(database["gamesStockfishDrawn"]), "Lost", db.getMean(database["gamesStockfishLost"]), db.getSd(database["gamesStockfishLost"])])
        
        # with doc.create(Section('Stockfish white')):
        #     doc.append("In this section you will see statistics of the games where Stockfish was white.")
                
        #     with doc.create(Subsection('Plot')):
        #         with doc.create(Figure(position='h!')) as whiteGamesPlot:
        #             self.createPlot(database["dataPointsStockFishWhiteGames"], "Stockfish white", "turns", "games", "whiteGamesPlot")
        #             whiteGamesPlot.add_image("whiteGamesPlot.png", width='200px')
        #             whiteGamesPlot.add_caption("All games where Stockfish was white plotted against their length.")

        #     with doc.create(Subsection('Tables')):
        #         self.createTable(doc, 'l|rrr', ["Color/Result", "Wins", "Draws", "Losses", "White", len(database["gamesWhiteStockfishWon"]), len(database["gamesWhiteStockfishDrawn"]), len(database["gamesWhiteStockfishLost"])])

        #         doc.append(LineBreak())
        #         doc.append(LineBreak())

        #         self.createTable(doc, 'l|rr', ["Color/Statistic", "Mean", "SD", "White", db.getMean(database["gamesStockfishWhite"]), db.getSd(database["gamesStockfishWhite"])])

        # with doc.create(Section('Stockfish black')):
        #     doc.append("In this section you will see statistics of the games where Stockfish was black.")
                
        #     with doc.create(Subsection('Plot')):
        #         with doc.create(Figure(position='h!')) as blackGamesPlot:
        #             self.createPlot(database["dataPointsStockFishBlackGames"], "Stockfish black", "turns", "games", "blackGamesPlot")
        #             blackGamesPlot.add_image("blackGamesPlot.png", width='200px')
        #             blackGamesPlot.add_caption("All games where Stockfish was black plotted against their length.")
                

        #     with doc.create(Subsection('Tables')):
        #         self.createTable(doc, 'l|rrr', ["Color/Result", "Wins", "Draws", "Losses", "Black", len(database["gamesBlackStockfishWon"]), len(database["gamesBlackStockfishDrawn"]), len(database["gamesBlackStockfishLost"])])

        #         doc.append(LineBreak())
        #         doc.append(LineBreak())

        #         self.createTable(doc, 'l|rr', ["Color/Statistic", "Mean", "SD", "Black", db.getMean(database["gamesStockfishBlack"]), db.getSd(database["gamesStockfishBlack"])])
        #         doc.append(NewPage())

        # with doc.create(Section('Stockfish won')):
        #     doc.append("In this section you will see statistics of the games where Stockfish won.")
                
        #     with doc.create(Subsection('Plot')):
        #         with doc.create(Figure(position='h!')) as wonGamesPlot:
        #             self.createPlot(database["dataPointsStockFishWon"], "Stockfish won", "turns", "games", "wonGamesPlot")
        #             wonGamesPlot.add_image("wonGamesPlot.png", width='200px')
        #             wonGamesPlot.add_caption("All games where Stockfish won plotted against their length.")
                

        #     with doc.create(Subsection('Tables')):
        #         self.createTable(doc, 'l|r', ["Color/Result", "Wins", "White", (database["gamesWhiteStockfishWon"]), "Black", len(database["gamesBlackStockfishWon"])])

        #         doc.append(LineBreak())
        #         doc.append(LineBreak())

        #         self.createTable(doc, 'l|rr', ["Color/Statistic", "Mean", "SD", "Any", db.getMean(database["gamesStockfishBlack"]), db.getSd(database["gamesStockfishBlack"])])


        doc.generate_pdf(clean_tex=False)
        doc.generate_tex()

def main():
    pdf = PDFCreator()
    db = ChessDatabase()

    pdf.createPdf(db, "createPdf")

if __name__ == '__main__':
    main()
