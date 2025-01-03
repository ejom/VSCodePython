def solution(board):
    #condition to loop until all remaining boxes are either at the bottom or under a box that is either at the bottom or under another box that is eventually at the bottom
    boxesSettled = False
    while not boxesSettled:
        boxesNotSettled = False
        #Evaluate if the boxes are settled (no boxes can move down anymore (For each box still alive startingf from first box onward, there is no empty spaces at the same index in a future (below) list))
        for i, row in enumerate(board):
            for j, space in enumerate(row):
                if space == '#':
                    #need to check each space at current index for future rows
                    for rowBelow in board[i:]:
                        if rowBelow[j] == '-':
                            boxesNotSettled = True
        #if the code above is never true (so it never breaks the for loop)
        if not boxesNotSettled:
            boxesSettled = True
        if boxesSettled:
            break
        
        #each box moves down a list, staying at the same index within the new list as it was in the previous list
        explodedSpcs = []
        for i, row in enumerate(board):
            for j, space in enumerate(row):
                if space == '#' and i != len(board)-1:
                    if board[i+1][j] == '#' or board[i+1][j] == '-':
                        board[i][j] = '-'
                        board[i+1][j] = '#'
                    elif board[i+1][j] == '*':
                        board[i][j] = '-'
                        for a in range(3):
                            for b in range(3):
                                explodedSpcs.append([i+a, j+b-1])
        # if the new position that the box took was previously occupied by an obstical, the box is replaced by the obstical and that specific obstical is saved for exploding effect. so they can simultanously explode
        #all obsticals that got hit by a box scan for any bordering boxes (either the same position as an adjacent list or 1 to the left or right of current list). Those boxes are replaced by empty space (destroyed)
        for i, row in enumerate(board):
            for j, space in enumerate(row):
                pos = [i, j]
                if space == '#' and pos in explodedSpcs:
                    board[i][j] = '-'
                    
    return board
                    
        
        #Evaluate if the boxes are settled (no boxes can move down anymore (For each box still alive startingf from first box onward, there is no empty spaces at the same index in a future (below) list))

print(solution([['#', '#', '#'], 
                ['-', '-', '*'], 
                ['#', '#', '-'] ]))