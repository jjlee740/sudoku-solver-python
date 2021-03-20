"""
    sudoku-solver.py by JJ Lee
    Sudoku solver is a sudoku solving algorithm that uses a classic backtracking algorithm and Knuth's X algorithm, a more efficient backtracking algorithm.
"""
import constant, copy, requests, bs4, numpy as np

class classicSolver:
    def __init__(self,board):
        self.board = board
        self.currentIndex = [0,0]
        self.count = 0
        self.backtrackCount = 0
    
    def deepCopyBoard(self, board):
        """ Helper function that creates a deepcopy of the sudoku board."""
        copiedBoard = copy.deepcopy(board)
        return copiedBoard

    def displayBoard(self, board):
        """ Displays the state of the current board. """
        for rows in range(constant.ROWS_LENGTH):
            print(board[rows])
        print('-----------------------------')

    def checkRowConstraint(self, board, row):
        """ Returns true if the row constraint is not violated. """
        currentRowNum = row
        currentRowValues = []
        for i in range(constant.ROWS_LENGTH):
            if board[currentRowNum][i] == 0:
                continue
            if board[currentRowNum][i] not in currentRowValues:
                currentRowValues.append(board[currentRowNum][i])
            else:
                return False
        return True
    
    def checkColConstraint(self, board, col):
        """ Return true if the column constraint is not violated. """
        currentColNum = col
        currentColValues = []
        for i in range(constant.COLUMNS_LENGTH):
            if board[i][currentColNum] == 0:
                continue
            if board[i][currentColNum] not in currentColValues:
                currentColValues.append(board[i][currentColNum])
            else:
                return False
        return True
    
    def check3x3Constraint(self,board, row, col):
        """ Return true if the 3x3 constraint is not violated. """
        # total of 9 3x3 boxes (quadrants) in a puzzle
        # transform value such that 0-2 -> 0, 1-3 -> 1, 4-6 -> 2
        currentXQuad = row // 3
        currentYQuad = col // 3 
        currentQuadValues = []

        for i in range(currentYQuad*3, (currentYQuad+1)*3):
            for y in range(currentXQuad*3, (currentXQuad+1)*3):
                if board[i][y] == 0:
                    continue
                if board[i][y] not in currentQuadValues:
                    currentQuadValues.append(board[i][y])
                else:
                    return False
        return True

    def checkAllConstraints(self, testValue, row, col):
        """ Ensures that all constraints are not broken. """ 
        tempBoard = copy.deepcopy(self.board)
        tempBoard[row][col] = testValue
        self.displayBoard(tempBoard)
        self.count = self.count + 1

        if self.checkRowConstraint(tempBoard, row) == True:
            if self.checkColConstraint(tempBoard, col) == True:
                if self.check3x3Constraint(tempBoard, row, col) == True:
                    return True
        return False
    
    def checkIfSolved(self):
        """ Returns true if the puzzle is solved and there are no longer any non zero elements on the board. """
        for i in range(constant.ROWS_LENGTH):
            for y in range(constant.COLUMNS_LENGTH):
                if self.board[i][y] == 0:
                    return False
        print("--- Successfully solved ----")
        print("This puzzle took", self.count, "iterations and", self.backtrackCount, "backtracks!")
        return True

    def nextIndex(self):
        """ Returns the next index on the board where it is 0. """
        for i in range(constant.ROWS_LENGTH):
            for y in range(constant.COLUMNS_LENGTH):
                if self.board[i][y] == 0:
                    return (i,y)
        return(-1,-1)    
    
    def solveBacktrack(self):
        """ Recursively solve the board by using backtracking. """
        if self.checkIfSolved():
            return True
        else: 
            row, col = self.nextIndex() 
        for i in range(1,constant.ROWS_LENGTH+1):
            if self.checkAllConstraints(i, row, col):
                self.board[row][col] = i

                if self.solveBacktrack():
                    return True
                self.backtrackCount = self.backtrackCount + 1
                self.board[row][col] = 0
            else:
                continue
        return False

class KnuthsX_Solver:
    def __init__(self, board):
        self.A = self.createExactCover(board)
        self.backtracks = 0
        self.B = {}
        self.updates = {}
        self.covered_cols = {}
        for (r, c) in self.A:
            self.covered_cols[c] = False
        
    def createExactCover(self, board):
        """ Creates an matrix such that it is equal to the exact cover board. """
        try:
            import exact_cover_np as ec
        except ImportError as error:
            print("ERROR FOUND: ", error)
            print("")
            print("Most likely you did not install the exact_cover_np package. Please install it and try again.")
            print("")
            quit()

        S = np.array(board)
        exact_cover = ec.get_exact_cover(S)
        return exact_cover

    def print_solution(self):
        print("SOLUTION")
        for k in self.B:
            for node in self.B[k]:
                print(node[1])
            print("") 

    def choose_column(self):
        """ Returns an uncovered column with minimal number of rows. """
        cols = [c for c in self.covered_cols if not self.covered_cols[c]]
        if not cols:
            print("All columns are completed.")

        tmp = dict([(c,0) for c in cols ])
        for (r,c) in self.A:
            if c in cols:
                tmp[c] = tmp[c] + 1
        min_c = cols[0]
        for c in cols:
            if tmp[c] < tmp[min_c]:
                min_c = c
        return min_c

    def search(self, k):
        """ Recursive solution that uses dancing links. """
        if not self.A: 
            for c in self.covered_cols: 
                if not self.covered_cols[c]:
                    return
            self.print_solution()
            return
        c = self.choose_column()
        
        rows = [node[0] for node in self.A if node[1] == c]
        if not rows:
            return
        for r in rows:
            box = []
            self.B[k] = [node for node in self.A if node[0]==r]

            for node in self.B[k]:
                box.append(node)
                self.A.remove(node)
                self.updates[k] = self.updates.get(k,0) + 1
            cols = [node[1] for node in B[k]]
            for j in cols:
                self.covered_cols[j] = True
                rows2 = [node[0] for node in self.A if node[1]==j]
                tmp = [node for node in self.A if node[0] in rows2]
                for node in tmp:
                    box.append(node)
                    self.A.remove(node)
                    self.updates[k] = self.updates.get(k,0) + 1
            self.search(k+1)
            for node in box:
                self.A.append(node)
            del box
            del self.B[k]
            for j in cols:
                self.covered_cols[j] = False
            self.print_solution()
            return

def sudokuScraper(emptyGrid):
    """ Obtains a sudoku puzzle from the site websudoku.com. """
    res = requests.get('https://nine.websudoku.com')
    try: 
        res.raise_for_status()
    except Exception as exc:
        print('Issue: Unable to obtain response from websudoku.com')
    # TODO: Request a LXML file to decrease runtime 
    parsedHTMLSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    puzzleNumSoup = parsedHTMLSoup.select('input[value]')
    # TODO: Add the option to choose puzzle difficulty

    # REGEX: find all matching patterns with id="fXX" and value="fXX" 
    # testString = '<td class="g0" id="c60"><input autocomplete="off" class="s0" id="f60" name="s2inkd71" readonly="" size="2" value="4"/>'    
    # testString = str(puzzleNumSoup)
    # sudokuValueRegex = re.compile(r'id=("c\d\d").*value="(\d)"')
    # foundStr = sudokuValueRegex.findall(testString)
    # print(foundStr)
    listParsed = list(puzzleNumSoup)
    for i in list(puzzleNumSoup):
        correctEntryCheck = 'autocomplete'
        if correctEntryCheck in i.attrs.keys():
            for key in emptyGrid.keys():
                if i.attrs['id'] == key:
                    emptyGrid[key] = i.attrs['value']

def createEmptySudokuDict(N):
    """ Creates a empty NxN board. """
    # Boards are formated such that id: "f" + {col number} + {row number} 
    sudokuBoard = {}
    for i in range(N):
        for j in range(N):
            id = 'f' + str(i) + str(j)
            sudokuBoard[id] = 0 
    return sudokuBoard

def convertBoardtoArray(board):
    """ Converts a sudoku dictonary into an array board. """
    convertedBoard = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
                      [6, 8, 0, 0, 7, 0, 0, 9, 0],
                      [1, 9, 0, 0, 0, 4, 5, 0, 0],
                      [8, 2, 0, 1, 0, 0, 0, 4, 0],
                      [0, 0, 4, 6, 0, 2, 9, 0, 0],
                      [0, 5, 0, 0, 0, 3, 0, 2, 8],
                      [0, 0, 9, 3, 0, 0, 0, 7, 4],
                      [0, 4, 0, 0, 5, 0, 0, 3, 6],
                      [7, 0, 3, 0, 1, 8, 0, 0, 0]]
    for keys in board.keys():
        splitKeyArray= list(keys)
        convertedBoard[int(splitKeyArray[1])][int(splitKeyArray[2])] = int(board[keys])
    return convertedBoard

def printBoard(board):
    """ Takes a board array and prints it such that is viewable in the context of sudoku. """
    for rows in range(constant.ROWS_LENGTH):
        print(board[rows])

def main():
    print("Welcome to sudoku solver!")
    print("")
    print("First: Will you like sudoku solver to find a random puzzle or would you like to enter a puzzle?")
    print("Please enter 1 for random puzzle or 2 to enter your own puzzle.")
    while(True):
        userInput = input()
        if userInput == '1':
            boardDict = createEmptySudokuDict(9)
            sudokuScraper(boardDict)
            board = convertBoardtoArray(boardDict)
            print("")
            printBoard(board)
            print("This is the board we have found from websudoku.com")
            break
        if userInput == '2':
            print("Please paste your puzzle into the program.")
            board = input()
            try:
                printBoard(board)
                print("")
                print("This is the board you have entered: ")
            except:
                userInput = 3
                print("")
                print('You have entered an invalid board. Please try again.')
                print("Please enter 1 for random puzzle or 2 to enter your own puzzle.")
                continue
            break
        if userInput != '1' or userInput != '2':
            print("Please enter either 1 or two.")
    print("")
    print("Now will you want to use the classic backtrack algorithm or use Knuth's backtrack algorithm?")
    print("Please enter 1 for the classic backtrack algorithm or 2 to use Knuth's or 3 to use both.")
    while(True):
        userInput = input()
        if userInput == '1':
            solver = classicSolver(board)
            solver.solveBacktrack()
            print("Thanks for trying out sudoku solver! You have used the backtrack method.")
            break
        if userInput == '2':
            solver = KnuthsX_Solver(board)
            print("Thanks for trying out sudoku solver using Knuth's method.")
            break
        if userInput == '3':
            secondBoard = copy.deepcopy(board)
            classicSolve = classicSolver(board)
            classicSolve.solveBacktrack()
            solver = KnuthsX_Solver(board)
            print("The classic backtrack algorithm used: ", str(classicSolve.iterations), "iterations and ", str(classicSolve.backtrackCount), " backtracks." )
            print("The number of iterations and backtracks knuth's algorithm is:")
        else:
            print("Please enter either 1 or two.")

if __name__=='__main__':
    main()

            
