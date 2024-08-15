#Download and import these to read html data from a URL
import requests

from bs4 import BeautifulSoup
import pandas as pd
import time

#Find the index of the next digit in a string
def findDigit(text):
    for i, char in enumerate(text):
        if char.isdigit():
            return i

#The information from the table is formatted at (x-coordinate number)(character to be plotted)(y-coordinate number) repeating as a single string. 
# This function turns this into a list of [[characters to be plotted], [x-coordinate numbers], [y-coordinate numbers]]
def getCharXY(data: str):
    lData = data.split(' ')
    #characters to be plotted
    #isolate characters between digits replace with something to split from
    charData = list(data)
    cData = charData.copy()
    for char in cData:
        if char.isdigit():
            charData.remove(char)
        if char == " ":
            charData.remove(" ")

    #x-coordinates
    #get the number before non digit characters
    xCoordinates = []
    for i, char in enumerate(lData):
        if (char.isdigit())==False:
            xCoordinates.append(lData[i-1])

    #y-coordinates
    #get the number before non digit characters
    yCoordinates = []
    for i, char in enumerate(lData):
        if (char.isdigit())==False:
            yCoordinates.append(lData[i+1])

    charXY = [[charData], [xCoordinates], [yCoordinates]]
    return charXY

#This turns the contents of the url into a string and isolates the data (starting from the first number after the last table header "y-coordinate")
def parseDoc(URL):
    doc = requests.get(URL)
    soup = BeautifulSoup(doc.content, 'html.parser')
    text = soup.get_text(separator = " ")
    data = text[text.find("y-coordinate"): ]
    i = findDigit(data)
    data = data[i:]
    return data

#This takes the table data as a 3d list and prints the characters list (first one) at its corrisponding xy coordinates (2nd and 3rd respectively)
# x values are represented as whitespace and y values as new lines
def plotData(data: list):
    #Plot character with x number of spaces and y number of new lines 
    # up (inverted) (so max of y is 0 new lines and y = 0 is max number of new lines)
    characters = data[0][0]
    x = []
    y = []
    for num in data[1][0]:
        x.append(int(num))
    for num in data[2][0]:
        y.append(int(num))

    #Plot characters line by line starting with max y and lowest x
    currLine = max(y)
    #Starting at the top (line 0)
    while currLine >= 0:
        #We now need the x value with a y value of numlines and corrisponding chars
        currXs = []
        currChars = []
        for i, num in enumerate(y):
            if num == currLine:
                currXs.append(x[i])
                currChars.append(characters[i])
        #We now want to sort the currXs from least to greatest and sort the currChars the same. 
        # Starting from 1 we check if x has that value. If it does pring corrisponidng char otherwise space
        fullRangeXs = range(max(currXs))
        fullRangeXs = list(fullRangeXs)
        fullRangeXs.append(max(currXs))
        for spot in fullRangeXs:
            hasChar = False
            for i, num in enumerate(currXs):
                if num == spot:
                    print(currChars[i], end = "")
                    hasChar = True
            if hasChar == False:
                print(' ', end = "")
        currLine = currLine - 1
        print("")

#Using the sample url from the question as our input
testURL = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"

data = getCharXY(parseDoc(testURL))
plotData(data)