#PROMPT
"""
Make me a python script that can test if a chessboard setup is in checkmate. 
It should return True, 'W' if white is in checkmate (black is the winner), True, 'B' if black is in checkmate, 
False, '' if neither is in checkmate, and False, 'E' if the board setup is invalid 
(such as both black and white in checkmate or one of the colors doesnt have a king, non square board, etc).  
The only input parameter in the script should be a list with the chess board setup, which can either be a 
2D list of characters or a list of strings. Each character corrisponds to a chess piece by the first letter 
of the piece name, with h for knight/horse. character 'n' in the string inputs signal an empty space, while 
the null character '' is an empty space for 2d list inputs. Lowercase letters represent white's pieces and 
uppercase letters represent black pieces. n and N are essentially the same. List index [0][0] would be the 
position A1 on a chessboard (whites left corner), and so on. The first index is the row and the second is the 
column. For example, index [0][4] is the starting position of whites king, and index [7][4] is the starting 
index of black's king. Test your script with the following list of test inputs, returning a list of lists for 
the output of each list. For example, if the test input was [[Board 2d list where black is in checkmate], 
[Board list of strings where white is in checkmate], [invalid input/board], [Board list of strings without 
anyone in checkmate]], then your final answer would be... 

[[True, 'B'], [True, 'W'], [False, 'E'], [False, '']]
"""

#Translate inputs into FEN
#Try valid input and run preset tests to ensure not invalid
#Try is_checkmate from both turns.
#If only one return true with that one
#If neighter return False
#If both true return invalid

"""
board = chess.Board("5rk1/5p1p/8/8/8/8/1B6/6RK")

print(board)
board.turn = False
print(board.is_checkmate())
"""
import chess

def checkmateStatus(FEN):
    #Try FEN input and run preset tests to ensure not invalid
    #(such as both black and white in checkmate or one of the colors doesnt have a king, nonsquare etc).
    #For non square board we can do a try catch with setting the preset board with our raw2Fen. 
    try:
        board = chess.Board(FEN)
    except ValueError:
        return [False, 'E']
    
    #Check that both colors have a king
    if 'k' not in FEN and 'K' not in FEN:
        return [False, 'E']
    
    #Check if white is in checkmate
    board.turn = True
    whiteCheckMate=True if board.is_checkmate() else False
    
    #Check if black is in checkmate
    board.turn = False
    blackCheckMate=True if board.is_checkmate() else False

    #Check that both arent in checkmate
    if whiteCheckMate and blackCheckMate:
        return [False, 'E']
    
    if whiteCheckMate:
        return [True, 'W']
    
    if blackCheckMate:
        return [True, 'B']

    return [False, '']

#Translate inputs into FEN
def raw2Fen(input):
    FEN = ""
    for row in input:
        FENRow = ""
        empties = 0
        #loop over each item
        #Need to handle string inputs with a row of just ""
        if row:
            for square in row:
                #check if item is chess pieces
                if square in "prhbqkPRHBQK" and square:
                    #invert chess piece capitilization
                    square = square.upper() if square.islower() else square.lower()
                    #change h to n or H to N
                    if square=='h':
                        square = 'n'
                    elif square=='H':
                        square = 'N'
                    #Add empties and piece to the row to be added to the beginning of FEN
                    if empties:
                        FENRow += str(empties)
                    FENRow += square
                    #Reset this everytime we hit a letter
                    empties = 0
                else:
                    #accumulate empty spaces
                    empties += 1
        else:
            #if row is null its all empty spaces (8)
            empties = 8
        #add empty spaces leftover 
        if empties:
            FENRow += str(empties)
        #if its not first row add Slash to the end
        if FEN:
            FENRow += '/'
        #Append complete FENRow to the beginning of FEN
        FEN = FENRow + FEN
    return FEN

#Testing
testBoards = [
[['', '', '', '', '', '', '', ''],
['', '', '', '', '', '', '', ''],
['', '', '', '', '', '', '', ''],
['', '', '', '', '', '', '', ''],
['', '', '', '', '', '', '', ''],
['', '', '', '', '', '', '', ''],
['', '', '', '', '', '', '', ''],
['', '', '', '', '', '', '', '']],

[['', '', '', '', '', '', 'r', 'k'],
['', 'b', '', '', '', '', '', ''],
['', '', '', '', '', '', '', ''],
['', '', '', '', '', '', '', ''],
['', '', '', '', '', '', '', ''],
['', '', '', '', '', '', '', ''],
['', '', '', '', '', 'P', '', 'P'],
['', '', '', '', '', 'R', 'K', '']],

["nhnnbrqk", "nnnpnnnp", "", "pnpnnnnn", "", "PPPPPPPP", "", "KRQNNBHR"],

[['r', 'h', 'b', '', 'k', '', 'h', 'r'],
['p', 'p', 'p', 'p', '', 'p', 'p', 'p'],
['', '', '', '', '', '', '', ''],
['', '', 'b', '', 'p', '', '', ''],
['', '', '', '', 'P', '', '', 'q'],
['', '', 'H', '', '', '', '', ''],
['P', 'P', 'P', 'P', '', 'P', 'P', 'P'],
['R', '', 'B', 'Q', 'K', 'B', 'H', 'R']],

[['', '', 'k', 'r', '', '', '', ''],
['p', 'p', 'p', '', '', 'p', 'p', 'p'],
['', '', '', '', '', '', '', ''],
['', '', '', '', 'p', '', '', ''],
['', '', '', '', 'P', '', 'b', ''],
['', '', '', '', 'Q', '', '', ''],
['P', '', '', '', '', 'P', 'P', 'P'],
['', 'H', '', '', 'K', 'B', '', 'R']],

["", "", "", "", "", "NNNNNBKH", "", "nnnnnnnk"],

[['', '', '', '', '', '', '', 'Q'],
['', 'p', 'p', 'k', '', 'p', 'p', ''],
['', '', 'h', '', '', '', '', 'p'],
['', 'p', '', 'p', '', 'b', '', ''],
['', '', '', '', '', '', '', ''],
['b', '', 'P', '', 'P', '', '', ''],
['P', '', '', 'H', '', 'P', 'P', 'P'],
['', '', 'K', 'R', '', '', 'H', 'R']]]

results = []
#run each board through the function
for board in testBoards:
    FEN = raw2Fen(board)
    results.append(checkmateStatus(FEN))

#Error, checkmate b, n, n, n, checkmate w, checkmate b
#Manually determine what each board should evaluate to
testVals = [[False, 'E'], [True, 'B'], [False, ''], [False, ''], [False, ''], [True, 'W'], [True, 'B']]
#Check that the function works
print("Evaluating function output with predetermined expected values")
print([results[i] == resultTest for i, resultTest in enumerate(testVals)])

#Print the correct output of the function as requested by the user
print(f"\nReporting output of the function for each board stored in a list per prompt requirements:")
print(results)