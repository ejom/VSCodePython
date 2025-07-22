#Falling Boxes
"""
This python script will simulate boxes falling with explosive obsticles. If a box '#' falls on an obstical '*' than
the box and all boxes adjacent to the obstical will be destroyed (replaced with empty space '-'). To fall on the obstical
means that the spaces overlap. The obstical will remain intact. 

The script will take any rectangular 2d list as input and will run until the boxes have "settled" to the "bottom"
(last index). For example, with an input of...

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

Another example input/output...
In:
[
['#', '#', '*'],
['-', '-', '-'],
['*', '#', '-'],
['#', '#', '#'],
['-', '#', '#']
]
Out:
[
['-', '-', '*'],
['-', '-', '-'],
['*', '-', '-'],
['-', '-', '#'],
['#', '#', '#']
]

reversed in/out of above:
in:
[
['-', '#', '#'], 
['#', '#', '#'], 
['*', '#', '-'], 
['-', '-', '-'], 
['#', '#', '*']
]
out:
[
['#', '#', '#'], 
['-', '-', '#'], 
['*', '-', '-'], 
['-', '-', '-'], 
['-', '-', '*']
]
"""


def main(grid: list):
    #Repeat this "falling" loop (moving down a space) until board is settled:
    grid.reverse()
    explodingObs = []
    while True:
        #Default of something happening is false
        event = False
        #Starting with the last row moving up.
        for i, row in enumerate(grid):

            #If the box is at the last row nothing happens.
            if i==0:
                continue
            for j, cell in enumerate(row):
                #we are only worried about analyzing boxes
                if cell != '#':
                    continue
                nextSpace = grid[i-1][j]
                #If its empty fall down a space
                if nextSpace == '-':
                    grid[i-1][j] = '#'
                    grid[i][j] = '-'
                    event = True
                #If its an obstical destroy the box and save index of obs
                elif nextSpace == '*':
                    grid[i][j] = '-'
                    explodingObs.append([i-1, j])
                    event = True
                #If it isnt empty or obs it must be a box
                #Do nothing
                    
        #Going through all obsticals flagged to explode:
        #All boxes adjacent to the flagged obstical are replaced with '-'.
        for obs in explodingObs:
            explodedIndexes = [
            [obs[0]-1, obs[1]-1],
            [obs[0]-1, obs[1]],
            [obs[0]-1, obs[1]+1],
            [obs[0], obs[1]-1],
            [obs[0], obs[1]+1],
            [obs[0]+1, obs[1]-1],
            [obs[0]+1, obs[1]],
            [obs[0]+1, obs[1]+1]
            ]
            for ind in explodedIndexes:
                if ind[0] <0 or ind[1] < 0:
                    explodedIndexes.remove(ind)
                    continue
                try:
                    space = grid[ind[0]][ind[1]]
                    if space == '#':
                        grid[ind[0]][ind[1]] = '-'
                        event = True
                except IndexError:
                    continue 
        #If you never moved a box or exploded an obstical than break the loop. 
        if not event:
            break
    grid.reverse()
    return grid

print(main([
['#', '#', '*'],
['-', '-', '-'],
['*', '#', '-'],
['#', '#', '#'],
['-', '#', '#']
]))

"""
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

Another example input/output...
In:
[
['#', '#', '*'],
['-', '-', '-'],
['*', '#', '-'],
['#', '#', '#'],
['-', '#', '#']
]
Out:
[
['-', '-', '*'],
['-', '-', '-'],
['*', '-', '-'],
['-', '-', '#'],
['#', '#', '#']
]
"""
