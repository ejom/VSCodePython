"""
input:
[
['#', '#', '#'], 
['*', '#', '-'], 
['-', '-', '#']
]

The output would be...
[
['-', '-', '-'],
['*', '-', '#'],
['-', '-', '#']
]
"""

"""
Each box '#' should inspect the space 'below' it. 
If the space is empty, the box should 'move down'.
If the space has an obstical '*', the box should be destoroyed and the obstical marked to activate. 
After all boxes have moved for that turn, every box adjacent to activated obsticals are destroyed. 
Repeat until there are no boxes with a obstical '*' or empty space '-' under them. 

VARIABLES:
currentSpace
nextSpace
activated
def makeAdjacentIndexes
"""

def makeAdjacentIndexes(ind: tuple, l: int, w: int) -> list[tuple]:
    adjacents = []
    i = ind[0]
    j = ind[1]
    adjRows = [i-1, i, i+1]
    adjCols = [j-1, j, j+1]
    for row in adjRows:
        for col in adjCols:
            if row>=0 and row<w and col>=0 and col<l and (row, col) != (i, j):
                adjacents.append((row, col))
    return adjacents

def shiftDown(board: list[list], rowLimit: int, col: int):
    print("before shift")
    print(board)
    newBoard = []
    for row in board:
        newBoard.append(row.copy())
    print(rowLimit)
    for i, _ in enumerate(board[:rowLimit+1]):
        print(i)
        if i==0:
            newBoard[i][col] = "-"
        else:
            newBoard[i][col] = board[i-1][col]
            print(board)
            print(board[i-1][col])
    print("After shift")
    print(newBoard)
    return newBoard

def fallingBoxes(board: list[list]):
    activated = []
    while True:
        didMove = False
        #Iterate through every space in all but last row.
        for i, row in enumerate(board[:-1]):
            for j, cell in enumerate(row):
                nextCell = board[i+1][j]
                if cell == "#":
                    if nextCell == "-":
                        board = shiftDown(board, i+1, j)
                        didMove = True
                        print("BOARD")
                        print(board)
                    elif nextCell == "*":
                        board = shiftDown(board, i+1, j)
                        #Restore nextCell staying as obstical and save it to activate
                        board[i+1][j] = "*"
                        activated.append((i+1, j))
                        didMove = True
                #Else it is a box '#' nothing
                #print(board)
        for obs in activated:
            toExplode = makeAdjacentIndexes(obs, len(board), len(board[0]))
            for ind in toExplode:
                if board[ind[0]][ind[1]] == "#":
                    board[ind[0]][ind[1]] = "-" 
        #If no boxes moved break
        if not didMove:
            break
    return board

inp=[
['#', '#', '#'], 
['*', '#', '-'], 
['-', '-', '#']
]

outp=[
['-', '-', '-'],
['*', '-', '#'],
['-', '-', '#']
]
output = fallingBoxes(inp)
print(output)
print(output==outp)