"""
Input: board = [["5","3",".",".","7",".",".",".","."],
["6",".",".","1","9","5",".",".","."],
[".","9","8",".",".",".",".","6","."],
["8",".",".",".","6",".",".",".","3"],
["4",".",".","8",".","3",".",".","1"],
["7",".",".",".","2",".",".",".","6"],
[".","6",".",".",".",".","2","8","."],
[".",".",".","4","1","9",".",".","5"],
[".",".",".",".","8",".",".","7","9"]]
Output: [["5","3","4","6","7","8","9","1","2"],
["6","7","2","1","9","5","3","4","8"],
["1","9","8","3","4","2","5","6","7"],
["8","5","9","7","6","1","4","2","3"],
["4","2","6","8","5","3","7","9","1"],
["7","1","3","9","2","4","8","5","6"],
["9","6","1","5","3","7","2","8","4"],
["2","8","7","4","1","9","6","3","5"],
["3","4","5","2","8","6","1","7","9"]]
"""

"""
Mark possible numbers for each empty square.
Make necessary moves, remark possibilities, and repeat.
After all necessary moves have been made, make a guess. 
Keep track of all necessary moves made from that guess. 
Make more guesses if necessary and repeat. 
If a contradiction happens (cell with no possible numbers), revert last guess, change it, and continue. 
"""
import time

def solveSudoku(board: list[list[str]]) -> None:
    """
    Variables:
    Possible nums: 
    def solveCell
    boardHistory

    Each empty cell will actually be a dict 
    They each have property possible nums (list). 
    They also have index on board (tuple of two numbers)
    local cells: list of tuples for indexes in same row, col, or square. 
    """
    def solveCell(targCell):
        #Mark number on the board
        solvedNum = cells[targCell]["possibleNums"][0]
        board[targCell[0]][targCell[1]] = f"{solvedNum}"
        #Update local cells' possible numbers
        for ind in cells[targCell]["localIndexes"]:
            if solvedNum in cells[ind]["possibleNums"]:
                cells[ind]["possibleNums"].remove(solvedNum)
                #If an affected possibleNums is only 1 recursively solve that same way
                if len(cells[ind]["possibleNums"])==1:
                    solveCell(ind)

    cells = {}
    for i, row in enumerate(board):
        for j, cel in enumerate(row):
            localRow = [(i, k) for k in range(9)]
            localCol = [(k, j) for k in range(9)]
            localSqr = []
            rowOffset = (i//3)*3
            colOffset = (j//3)*3
            for k in range(3):
                for l in range(3):
                    localSqr.append((k+rowOffset, l+colOffset))
            #Turn everything into sets
            localRow = set(localRow)
            localCol = set(localCol)
            localSqr = set(localSqr)
            #non empty cells
            if cel.isdigit():
                cells[(i, j)] = {"possibleNums": [int(cel)], "localIndexes": localRow | localCol | localSqr}
            else:
                cells[(i, j)] = {"possibleNums": [1, 2, 3, 4, 5, 6, 7, 8, 9], "localIndexes": localRow | localCol | localSqr}
    #SOLVING GIVENS
    for cell in cells:
        for ind in cells[cell]["localIndexes"]:
            #Value of local cells
            num = board[ind[0]][ind[1]]
            #If its empty skip, else remove from possibleNums
            if num.isdigit():
                num = int(num)
            else:
                continue
            if num in cells[cell]["possibleNums"]:
                cells[cell]["possibleNums"].remove(num)
                if not cells[cell]["possibleNums"]:
                    print(cell)
        #If there is one possible num solve the cell
        if len(cells[cell]["possibleNums"])==1:
            solveCell(cell)

    #GUESSING
    startTime = time.time()
    timeLimit = 5
    boardHist = [board.copy()]
    guessCells = []
    i1=0
    j1=0
    guessInd = 0
    while True:
        cell = (i1, j1)
        if len(cells[cell]["possibleNums"])>1:
            #If not out of index guess solve the cell
            if guessInd < len(cells[cell]["possibleNums"]):
                cells[cell]["possibleNums"] = [cells[cell]["possibleNums"][guessInd]]
                solveCell(cell)
                boardHist.append(board.copy())
                guessCells.append((i1, j1))
            else:
                guessInd = 0
        elif not cells[cell]["possibleNums"]:
            #Revert board
            boardHist.pop()
            board = boardHist[-1]
            #Go back to last cell you guessed. 
            (i1, j1) = guessCells.pop()
            #Increment the guess unless out of guesses then skip to next cell
            guessInd += 1
            continue

        #See if we solved the board
        if all(item.isdigit() for row in board for item in row):
            break
        #Check for timeout
        if time.time() - startTime > timeLimit:
            print("Timed out, board might not be solvable")
            break
        #Update Index
        if i1 < 8:
            i1+=1
        elif j1 < 8:
            i1 = 0
            j1 += 1
        else:
            i1 = 0
            j1 = 0

    #After you have iterated through every cell for possibility solvings, we guess smallest number of first cell
    #Solve the cell (call the fun), but store previous board states whenever you guess.
        #After all the recursive calls execute, thats the current state
        #Before any fun calls and the guessed sol is the previous state
    #Do this for each cell until you hit a cell with no possible solutions
    #Revert to last state, increment guess, and continue. 
    #Once you hit the end you are done. 
        
board = [["5","3",".",".","7",".",".",".","."],
["6",".",".","1","9","5",".",".","."],
[".","9","8",".",".",".",".","6","."],
["8",".",".",".","6",".",".",".","3"],
["4",".",".","8",".","3",".",".","1"],
["7",".",".",".","2",".",".",".","6"],
[".","6",".",".",".",".","2","8","."],
[".",".",".","4","1","9",".",".","5"],
[".",".",".",".","8",".",".","7","9"]]

output = [["5","3","4","6","7","8","9","1","2"],
["6","7","2","1","9","5","3","4","8"],
["1","9","8","3","4","2","5","6","7"],
["8","5","9","7","6","1","4","2","3"],
["4","2","6","8","5","3","7","9","1"],
["7","1","3","9","2","4","8","5","6"],
["9","6","1","5","3","7","2","8","4"],
["2","8","7","4","1","9","6","3","5"],
["3","4","5","2","8","6","1","7","9"]]

hardBoard = [
[".",".","9","7","4","8",".",".","."],
["7",".",".",".",".",".",".",".","."],
[".","2",".","1",".","9",".",".","."],
[".",".","7",".",".",".","2","4","."],
[".","6","4",".","1",".","5","9","."],
[".","9","8",".",".",".","3",".","."],
[".",".",".","8",".","3",".","2","."],
[".",".",".",".",".",".",".",".","6"],
[".",".",".","2","7","5","9",".","."]
]

hardOut = [
["5","1","9","7","4","8","6","3","2"],
["7","8","3","6","5","2","4","1","9"],
["4","2","6","1","3","9","8","7","5"],
["3","5","7","9","8","6","2","4","1"],
["2","6","4","3","1","7","5","9","8"],
["1","9","8","5","2","4","3","6","7"],
["9","7","5","8","6","3","1","2","4"],
["8","3","2","4","9","1","7","5","6"],
["6","4","1","2","7","5","9","8","3"]
]

solveSudoku(hardBoard)
for row in hardBoard:
    print(row)
print(hardBoard==hardOut)