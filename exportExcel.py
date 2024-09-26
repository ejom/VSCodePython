import numpy as np
import pandas as pd
import openpyxl

#strip everything outside of <b> tags and store in list
def findBodies(bulk:str):
    bulk = bulk.replace("<", ">")
    elements = bulk.split(">") 
    numElements = []
    for element in elements:
        if element.isnumeric() or element.replace('.', '').isnumeric():
            numElements.append(element)
    return numElements

    #return elements

def makeArr(nList):
    goodList = False
    while not goodList:
        #cut out unwanted numbers testing. Loop until it looks right.
        print(nList)
        bTrim = input("\n Would you like to trim the list? Enter (y) if yes or anything if no")
        if bTrim == 'y':
            frontTrim = input("Please input the number of values to trim from the front, or 0 if none")
            backTrim = input("Input number of items from back to trim")
            list = nList[frontTrim:len(nList-backTrim)]
            nList = list
        else:
            goodList = True
    
    nArr = np.array(nList)
    return nArr

#Test that the generated table looks right before creating excel file. Trimming numbers if necessary
def makeTable(nArr):
    goodTable = False
    while not goodTable:
        #change paramaters based on table of data
        validInput = False
        while not validInput:
            cols = input("Enter number of columns\n")
            rows = input("Enter number of rows\n")
            if cols.isnumeric() & rows.isnumeric():
                validInput = True
            else:
                print("Please enter only numbers for rows and columns")
        cols = int(cols)
        rows = int(rows)

        nArr = nArr.reshape(rows, cols)
        nTable = pd.DataFrame(nArr)
        print(nTable)

        bTable = input("does the table look right? If not, enter (n). Otherwise enter anything")
        if bTable != 'n':
            goodTable = True
    return nTable

HTMLCode = input("Please copy the HTML code containing the table you wish to export\n")

nList = findBodies(HTMLCode)
nArr = makeArr(nList)
nTable = makeTable(nArr)

#what excel file to save to
fileName = input("please type the file name without extension or spaces (.xlsx will automatically be made the extension of the file)\n")
ext = ".xlsx"
excelFile = pd.ExcelWriter(fileName + ext)

nTable.to_excel(excelFile)
excelFile.close()
