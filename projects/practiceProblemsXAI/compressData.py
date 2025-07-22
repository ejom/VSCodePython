"""
Take a list of strings and returns a list of tuples and a dictionary. 
The tuples should be first the abbreviated string and then an int for how many times that string occurs. 
The dict should be the abbreviated string (key) and the original string (value). 

Examples

Input:
["Cow", "Camel", "Green", "orange", "Camel", "green", "orange"]

Output:
[("C", 1), ("Ca", 2), ("G", 1), ("o", 2), ("g", 1)]
{"C": "Cow", "Ca": "Camel", "G": "Green", "o": "orange", "g": "green"}
"""
from collections import Counter

def compress(data: list) -> tuple[list, dict]:
    compressedList = []
    compressedWords = []
    compressedKey = {}
    countedData = Counter(data)
    for word in countedData:
        i=1
        compressedWord = word[0]
        while compressedWord in compressedWords:
            try:
                compressedWord = word[:i]
            except IndexError:
                compressedWord = f"{word}{i}"
            i += 1
        compressedList.append((compressedWord, countedData[word]))
        compressedWords.append(compressedWord)
        compressedKey[compressedWord] = word
    return compressedList, compressedKey

print(compress(["Cow", "Camel", "Green", "orange", "Camel", "green", "orange"]))
