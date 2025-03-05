#The input is ciphered text where the letters are shifted an unknown amount up and one known word. 
# The output is the deciphered original text. 

import unittest
def decipher(ciphertext: str, knownWord: str) -> str:
    #Input the cipher text and one deciphered word
    # All of the words are shifted alphebatically by the same amount (possibly all shifted up from original)
    #Need to output original deciphered text
    
    #Test all the words in ciphertext to find which is the known word
    #split sentence input into list of words
    cipherList = ciphertext.split()
    #Sort words with the same number of characters
    nList = []
    for word in cipherList:
        if len(word) == len(knownWord):
            nList.append(word)
    #claclulate the ascii value difference between each character in new list
    differences = []
    for i, ciphWord in enumerate(nList):
        differences.append([])
        for ciphChar, knownChar in zip(ciphWord, knownWord):
            differences[i].append(ord(ciphChar) - ord(knownChar))
    #Test the sets of differences to filter out the ones that are all same and save indexes
    sameDifferences = []
    sameDifferencesIndexes = []
    for i, dList in enumerate(differences):
        if dList.count(dList[0]) == len(dList):
            sameDifferences.append(dList)
            sameDifferencesIndexes.append(i)
    #Later might revise this to check for first actual word but for now just take first instance
    ciphKnownWordIndex = sameDifferencesIndexes[0]
    ciphKnownWord = cipherList[ciphKnownWordIndex]
    #save differences for the ciphKnownWord
    #diff = sameDifferences[ciphKnownWordIndex]
    diff = sameDifferences[0]
    #Save one with same difference for every character and save number of differance
    #Apply saved difference to each word of input and pass as output
    decipherList = []
    decipherWord = ""
    for word in cipherList:
        for char in word:
            nCharNum = ord(char) - diff[0]
            decipherChar = chr(nCharNum)
            decipherWord = decipherWord + decipherChar
        decipherList.append(decipherWord)
        decipherWord = ""
    deciphertext = " ".join(decipherList)
    return deciphertext
    #Calculate how much the word was shifted to be ciphered
    #Shift back down the cipher text to pass to output

#Inputs
print("input the ciphered text, with all letters shifted up the same amount ")
ciphertext = input().strip()
print("input one of the words in the deciphered text ")
knownWord = input().strip()

#Tests
"""
ciphertext = "uijt jt djqifsfe ufyu"
knownWord = "is"
"""
result = decipher(ciphertext, knownWord)
print(result)
