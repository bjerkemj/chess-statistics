# This file is just copy paste of code that was in a poor place that should be put elsewhere or removed


# FROM chessDatabase.py

    def createPdf(self, fileName: str = 'report') -> None:
        gamesAll = self.getAllGames()
        gamesStockfishWhite = self.filterStockfishWhite(gamesAll)
        gamesStockfishBlack = self.filterStockfishBlack(gamesAll)

        gamesStockfishWon = self.filterStockfishWon(gamesAll)
        gamesStockfishDrawn = self.filterDrawn(gamesAll)
        gamesStockfishLost = self.filterStockfishLost(gamesAll)

        gamesWhiteStockfishWon = self.filterStockfishWhite(gamesStockfishWon)
        gamesWhiteStockfishDrawn = self.filterStockfishWhite(
            gamesStockfishDrawn)
        gamesWhiteStockfishLost = self.filterStockfishWhite(gamesStockfishLost)

        gamesBlackStockfishWon = self.filterStockfishBlack(gamesStockfishWon)
        gamesBlackStockfishDrawn = self.filterStockfishBlack(
            gamesStockfishDrawn)
        gamesBlackStockfishLost = self.filterStockfishBlack(gamesStockfishLost)

        onGoing = self.getNumListOngoingGames(gamesAll)
        onGoingWhite = self.getNumListOngoingGames(gamesStockfishWhite)
        onGoingBlack = self.getNumListOngoingGames(gamesStockfishBlack)
        onGoingWon= self.getNumListOngoingGames(gamesStockfishWon)
        onGoingDrawn= self.getNumListOngoingGames(gamesStockfishDrawn)
        onGoingLost = self.getNumListOngoingGames(gamesStockfishLost)

        dataPointsAllGames = self.getDataPoints(onGoing)
        dataPointsStockFishWhiteGames = self.getDataPoints(onGoingWhite)
        dataPointsStockFishBlackGames = self.getDataPoints(onGoingBlack)
        dataPointsStockFishWon= self.getDataPoints(onGoingWon)
        dataPointsStockFishDrawn= self.getDataPoints(onGoingDrawn)
        dataPointsStockFishLost = self.getDataPoints(onGoingLost)

        doc = Document(fileName)
        doc.preamble.append(Command('title', 'Stockfish chess statistics'))
        doc.preamble.append(Command('author', 'Tinus F Alsos and Johan Bjerkem'))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))
        doc.append("In this document i will present tables, graphs and statistics about 2600 chess games played by the chess engine Stockfish. The game information is gathered from the document 'Stockfish_15_64-bit.commented.[2600].pgn'. Hopefully you find the data insightful.")

        with doc.create(Section('I am a section')):
            doc.append('Take a look at this beautiful plot:')

            with doc.create(Figure(position='htbp')) as plot:
                plot.add_plot(width=NoEscape(width), *args, **kwargs)
                plot.add_caption('I am a caption.')

            doc.append('Created using matplotlib.')

            doc.append('Conclusion.')

        with doc.create(Section('Tables')):
                doc.append("In the table below you can see the results of the 2600 games that Stockfish played.")
                doc.append(LineBreak())
                doc.append(LineBreak())
                with doc.create(Tabular('l|rrr')) as table:
                    table.add_row(("Color/Result", "Wins", "Draws", "Losses"))
                    table.add_hline()
                    table.add_row(("Any", len(gamesStockfishWon), len(gamesStockfishDrawn), len(gamesStockfishLost)))
                    table.add_row(("White", len(gamesWhiteStockfishWon), len(gamesWhiteStockfishDrawn), len(gamesWhiteStockfishLost)))
                    table.add_row(("Black", len(gamesBlackStockfishWon), len(gamesBlackStockfishDrawn), len(gamesBlackStockfishLost)))

                doc.append(LineBreak())
                doc.append(LineBreak())
                doc.append("The table below shows the mean and standard deviation accompanying Figure 1.")
                doc.append(LineBreak())
                doc.append(LineBreak())
                with doc.create(Tabular('l|rr')) as table:
                    table.add_row(("Color/Result", "Mean", "SD"))
                    table.add_hline()
                    table.add_row(("Any", self.getMean(gamesAll), self.getSd(gamesAll)))
                    table.add_row(("White", self.getMean(gamesStockfishWhite), self.getSd(gamesStockfishWhite)))
                    table.add_row(("Black", self.getMean(gamesStockfishBlack), self.getSd(gamesStockfishBlack)))


        with doc.create(Subsection('Plots')):
                with doc.create(Figure(position='h!')) as allGamesPlot:         
                    plt.plot(dataPointsAllGames, label="any")
                    plt.plot(dataPointsStockFishWhiteGames, label="white")
                    plt.plot(dataPointsStockFishBlackGames, label="black")
                    plt.xlabel("playes")
                    plt.ylabel("games")
                    plt.legend()
                    plt.savefig("allGamesPlot.png")
                    plt.clf()
                    allGamesPlot.add_image("allGamesPlot.png", width='300px')
                    allGamesPlot.add_caption('All games plotted against their length.')

                    plt.hist([game.getTotalMoves() for game in gamesAll], range=(0,250), label="any")
                    plt.xlabel("playes")
                    plt.ylabel("games")
                    plt.savefig("histogram.png")
                    plt.legend()
                    plt.clf()
                    allGamesPlot.add_image("histogram.png", width='300px')
                    allGamesPlot.add_caption('Histogram of all games and their lengths. Looks normally distributed with a longer tail on the right side.')
                    doc.append(LineBreak())


                    plt.plot(dataPointsStockFishWon, label="won")
                    plt.plot(dataPointsStockFishDrawn, label="drawn")
                    plt.plot(dataPointsStockFishLost, label="lost")
                    plt.xlabel("playes")
                    plt.ylabel("games")
                    plt.legend()
                    plt.savefig("winLossPlot.png")
                    plt.clf()
                    allGamesPlot.add_image("winLossPlot.png", width='300px')
                    allGamesPlot.add_caption('Won, drawn and lost games plotted against their length.')
                    doc.append(LineBreak())


        doc.generate_pdf(clean_tex=False)
        doc.generate_tex()

    def addOpeningTableToPDF(self, filename: str, opening: str, depth: int = 0) -> None:
        statsDictionary = self.getStatsDictionary()
        with open(filename + '.tex', 'r') as file:
            lines = file.readlines()
            endLine = lines.pop()

        with open(filename + '.tex', 'w') as file:
            file.writelines(lines)
            file.write('Here comes another table!!\n\n')
            file.write('\\begin{table}[h!]\n')
            file.write('\\centering\n')
            file.write('\\begin{tabular}{l|rrrr}\n')
            file.write('Color/Result & Wins & Draws & Losses & Total\\\\\n')
            file.write('\hline\n')
            file.write(
                f'Any & {statsDictionary["numGamesStockfishWon"]} & {statsDictionary["numGamesStockfishDrawn"]} & {statsDictionary["numGamesStockfishLost"]} & {statsDictionary["numGamesAll"]}\\\\\n')
            file.write(
                f'White & {statsDictionary["numGamesWhiteStockfishWon"]} & {statsDictionary["numGamesWhiteStockfishDrawn"]} & {statsDictionary["numGamesWhiteStockfishLost"]} & {statsDictionary["numGamesWhiteStockfishAll"]}\\\\\n')
            file.write(
                f'Black & {statsDictionary["numGamesBlackStockfishWon"]} & {statsDictionary["numGamesBlackStockfishDrawn"]} & {statsDictionary["numGamesBlackStockfishLost"]} & {statsDictionary["numGamesBlackStockfishAll"]}\\\\\n')
            file.write('\end{tabular}\n')
            file.write(
                '\caption{Statistics for Stockfish when opening is: ' + opening + '}\n')
            file.write('\end{table}\n')
            file.write(endLine)

    def addOpeningsPlayedOverNTimesToPDF(self, filename: str, n=int) -> None:
        openingsDict = self.getOpeningsPlayedOverNTimes(n=n)
        for opening in openingsDict.keys():
            new_db = ChessDatabase(
                self.getFilteredListOfGamesByOpening(opening))
            new_db.addOpeningTableToPDF(
                filename=filename, opening=opening, depth=0)
            



# FROM CHESSOPENINGTREE.PY



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



def generateDotFileFromTree(tree: Tree, filename: str, depth: int = 2, rootName: str = None) -> None:
    allText = getDotText(tree, depth, rootName)
    with open(filename + '.dot', 'w') as file:
        file.write(
            "digraph g {\nfontname=\"Helvetica,Arial,sans-serif\"\nnode [fontname=\"Helvetica,Arial,sans-serif\" filledcolor = \"white\" label = \"\" style = \"filled\" shape = \"circle\" ]\nedge [fontname=\"Helvetica,Arial,sans-serif\"]\ngraph [fontsize=30 labelloc=\"t\" label=\"\" splines=true overlap=false rankdir = \"LR\"];\nratio = auto;\n")
        file.write(allText)
        file.write("\n}")
