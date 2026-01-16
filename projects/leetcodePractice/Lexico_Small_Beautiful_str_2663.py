class Solution:
    def smallestBeautifulString(self, s: str, k: int) -> str:
        #Need to find the smallest string that can contain only the first k characters of the alphabet
        # and is larger than the inputted string that doesn't contain a palindrome
        
        #Start at the end and work towards the front
        #if the end character can be incremented increment it and return
        #It can't be incremented if it would increment outside the range of k or increment to create
        #a palindrome
        
        for i, c in enumerate(s[::-1]):
            while True:
                #implement recursive call to check c
                print(c)
                if c=='z':
                    break
                nextOrd = ord(c)+1
                if nextOrd > ord('a')-1 + k:
                    break
                nextChar = chr(nextOrd)
                j=len(s)-i
                if self.isPalindrome(s[i:j]):
                    continue
                s[j-1] = nextChar
                return s


    def isPalindrome(self, s: str) -> bool:
        i = len(s)//2
        if s[:i]==s[:-i-1:-1]:
            return True
        return False

#TEST
"""
Input: s = "abcz", k = 26
Output: "abda"

Input: s = "dc", k = 4
Output: ""
"""

sol = Solution()
print(sol.smallestBeautifulString("abcba", 26))