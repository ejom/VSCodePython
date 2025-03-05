#Read lines of comma seperated numbers and store in 2d list and flag non numeric lines with line number and store as None
inputFile = "randomStuff.txt"
file = open(inputFile)

#initialize empty 2d list
D1 = 0
D2 = 0
data = [[None for x in range(D1)] for y in range(D2)]
#Initialize flagged lines list
flaggedLines = []

#FUNCTIONS
#strip all elements of input
def stripAll(input: list):
    newList = []
    for i in input:
        i = i.replace(" ", "").strip()
        newList.append(i)
    return newList
#test if all items are numeric
def allIsnumeric(input: list):
    for i in input:
        if i.isnumeric():
            t = True
        else:
            t = False
            return t
    return t

#Reading in and munipulating each line from inputFile
for y, line in enumerate(file):
    #Initialize line list
    data.append([])
    #split comma dilimated numbers in line
    line = line.split(',')
    #strip all whitespace inner or outer from each element
    line = stripAll(line)
    #Make sure line elements are all numeric before converting to ints and appending to list
    if (allIsnumeric(line)):
        for x in line:
            data[y].append(int(x))
    #If not all numeric append none and flag that index
    else:
        data[y].append("")
        flaggedLines.append(y)

print(data)
print(flaggedLines)