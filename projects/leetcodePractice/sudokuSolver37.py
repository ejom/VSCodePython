def solveSudoku(board: list[list[str]]) -> None:
    board_size = len(board)

    solved_cells = set()
    possible_vals = dict()
    dependent_cells = dict()
    for row_ind in range(board_size):
        for col_ind in range(board_size):
            possible_vals[(row_ind, col_ind)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            dependent_cells[(row_ind, col_ind)] = set()
            for i in range(board_size):
                dependent_cells[(row_ind, col_ind)].add((row_ind, i))
                dependent_cells[(row_ind, col_ind)].add((i, col_ind))
                if i<3: #fill in the squares
                    for j in range(3):
                        dependent_cells[(row_ind, col_ind)].add((row_ind-row_ind%3+i, col_ind-col_ind%3+j))
            dependent_cells[(row_ind, col_ind)].remove((row_ind, col_ind))

    #solve fun to update possible_vals dict of affected cells and solve the cell
    def solve_cell(row_ind, col_ind, val=None):
        if (row_ind, col_ind) in solved_cells:
            return
        solved_cells.add((row_ind, col_ind))
        if val:
            possible_vals[(row_ind, col_ind)] = {val}
        else:
            val=possible_vals[(row_ind, col_ind)]
        for depCell in dependent_cells[(row_ind, col_ind)]:
            if val in possible_vals[depCell]:
                possible_vals[depCell].remove(val)
            if len(possible_vals[depCell])==1:
                solve_cell(depCell[0], depCell[1])

    board_states = []

    #initialize the board with possible vals
    testDummy=0
    while testDummy<81:
        for row_ind, row in enumerate(board):
            for col_ind, cell in enumerate(row):
                if cell.isnumeric():
                    solve_cell(row_ind, col_ind, int(cell))
        testDummy+=1

    #TESTING
    return possible_vals

"""
fun update board
Iterate over empty cells in each row
Store possible vals for each cell
If there is a cell with no possible vals revert to last board state and restart
If there is only one possible val than solve the cell and update affected cells possible vals accordingly

Go into guessing mode passing in first unsolved cell with first guess
Remove the guess from the dict of guesses for that cell.
save the boards state in list
Solve inputted cell with inputted guess
Do update_board again

"""
board = [
    ["5","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"]]

easyBoard = [
    [".","5","8",".","7",".",".",".","2"],
    [".","4",".",".","6","2",".","9","8"],
    ["2","9","1",".","3",".","7",".","."],
    [".",".","6","9",".",".","4",".","7"],
    ["3","2",".","6",".",".",".","1","5"],
    [".","7",".","2","5","4","6",".","3"],
    [".",".",".","8","9","1","2",".","6"],
    [".",".",".",".","2",".",".","4","."],
    [".",".",".",".",".",".","8",".","1"]]

solved_board = solveSudoku(easyBoard)
print(solved_board)