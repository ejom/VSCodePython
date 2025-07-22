"""
Takes a string as input and returns the longest substring that is a palindrome:

Examples
Kawow
wow

abmomab
mom

Kadadish
dad
"""

"""
Need to check for matching character
Start with beginning characters and check for matching starting with ending characters
If there if a match, check middle ones for palindrome. Else continue
"""

def subPalindrome(word: str):
    palindromes = []
    for i, _ in enumerate(word):
        for j, _ in enumerate(word[:-i]):
            if j==0:
                substring = word[i:]
            else:
                substring = word[i:-j]
            if substring == substring[::-1]:
                palindromes.append(substring)
    return max(palindromes, key=len)
#TESTING
testInputs = ["Kawow", "aamomab", "Kadadish"]
testOutputs = ["wow", "mom", "dad"]

for input in testInputs:
    print(subPalindrome(input))