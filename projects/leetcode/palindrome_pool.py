class Solution:
    def maxPalindromesAfterOperations(self, words):
        total_chars = {}
        for word in words:
            for char in word:
                total_chars[char] = total_chars.get(char, 0) + 1
                
        # Count how many pairs we have in total
        total_pairs = sum(count // 2 for count in total_chars.values())
        
        # Sort word lengths to satisfy shortest words first (Greedy)
        lengths = sorted([len(w) for w in words])
        
        palindromes_count = 0
        for length in lengths:
            # Number of pairs needed for this word
            pairs_needed = length // 2
            
            if total_pairs >= pairs_needed:
                total_pairs -= pairs_needed
                palindromes_count += 1
            else:
                # Not enough pairs to satisfy even the shortest remaining word
                break
                
        return palindromes_count

        