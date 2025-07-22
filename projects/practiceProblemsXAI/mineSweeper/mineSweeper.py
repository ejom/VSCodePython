import random

def coordinateToValue(coord: str):
    column = coord[0]
    row = coord[1]
    return (int(row)-1)*9 + (ord(column)-97)

def revealBoxes(box, revealed, key):
    #add box to revealed if its not a mine. 
    #call function on adjacent boxes if they arent a mine or *(aren't a second box adjacent to a mine)*
    #* If the function's target box is adjacent to a mine, don't call it on adjacent boxes that are also adjacent to a mine
    
    #number of adjacent mines
    numAdj = 0
    if key[box]:
        return False #kill signal, hit a mine
    else:
        adjacentBoxes = [box-1, box-10, box-9, box-8, box+1, box+8, box+9, box+10]
        #Ignore borders that would go out of bounds
        #Start with left border
        if box%9 == 0:
            adjacentBoxes.remove(box-1)
            adjacentBoxes.remove(box-10)
            adjacentBoxes.remove(box+8)
        #Right
        if box%9 == 8:
            adjacentBoxes.remove(box-8)
            adjacentBoxes.remove(box+1)
            adjacentBoxes.remove(box+10)
        #Bottom 
        if box < 9:
            try:
                adjacentBoxes.remove(box-8)
            except ValueError:
                pass
            adjacentBoxes.remove(box-9)
            try:
                adjacentBoxes.remove(box-10)
            except ValueError:
                pass
        #Top
        if box >= 72:
            try:
                adjacentBoxes.remove(box+8)
            except ValueError:
                pass
            adjacentBoxes.remove(box+9)
            try:
                adjacentBoxes.remove(box+10)
            except ValueError:
                pass
        for adjBox in adjacentBoxes:
            #Check if an adjacent box is a mine
            if key[adjBox]:
                numAdj += 1
        if numAdj:
            revealed[box] = numAdj
            return True
        else:
            revealed[box] = 0
            for adjBox in adjacentBoxes:
                if revealed[adjBox] >= 0:
                    continue
                revealBoxes(adjBox, revealed, key)
    return True

def printBoard(revealed):
    for i in range(9):
        print(f"{9-i}", end=" ")
        for j in range(9):
            ind = (8-i)*9 + j
            if revealed[ind] >= 0:
                print(f"|{revealed[ind]}", end="")
            elif revealed[ind] < -1:
                print("|*", end="")
            else:
                print("|#", end="")
        print("|")
    print("   a b c d e f g h i")

def main():
    #Change this to choose how many mines to play with
    numMines = 10
    #Populate the mines on the board other than the selected position (10 total)
    boardKey = [False] * 81
    revealed = [-1] * 81
    notMines = []
    mines = []
    #Create the board
    printBoard(revealed)
    #Choose an input on the board
    #Input a letter and a number
    print("Choose your first position on the board")
    print("Enter first a letter between a and i and then a number between 1 and 9, such as a1 or i9")
    startSquare = input("Enter your position here: ")
    
    for i in range(81):
        notMines.append(i)
    #Remove startSquare from notMines for now
    strtInd = coordinateToValue(startSquare)
    notMines.pop(strtInd)
    #80 squares are left in unknown, so use randint(0, 79), and call 10 times with one less square
    #so randint(0, 78), randint(0, 77), ..., randint(0, 69). 
    #Each time remove that index and put in mines and set that index value to True
    for i in range(numMines):
        mineInd = random.randint(0, len(notMines)-1)
        mineNum = notMines.pop(mineInd)
        mines.append(mineNum)
        boardKey[mineNum] = True
    notMines.insert(strtInd, strtInd)

    #Sort everything
    notMines.sort()
    mines.sort()

    #Call revealBoxes(strtInd)
    revealBoxes(strtInd, revealed, boardKey)
    printBoard(revealed)

    stillAlive = True
    while stillAlive:
        move = input("Enter your position here: ")
        moveInd = coordinateToValue(move)
        stillAlive = revealBoxes(moveInd, revealed, boardKey)
        printBoard(revealed)
        print()
        if not stillAlive:
            print("You hit a mine")
            revealed[moveInd] = -2
            break
        if sum([rev<0 for rev in revealed]) == numMines:
            print("You win")
            break
    printBoard(revealed)

main()

