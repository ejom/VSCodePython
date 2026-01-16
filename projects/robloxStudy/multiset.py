from collections import Counter

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        s_len, p_len = len(s), len(p)
        if p_len > s_len:
            return []

        p_count = Counter(p)
        s_count = Counter(s[:p_len]) # Initialize first window
        
        result = []
        
        # Check the first window
        if s_count == p_count:
            result.append(0)
            
        # Start sliding from index 1
        for i in range(1, s_len - p_len + 1):
            left_char = s[i - 1]          # Character leaving
            right_char = s[i + p_len - 1] # Character entering
            
            # Update s_count: Add new char, remove old char
            s_count[right_char] += 1
            s_count[left_char] -= 1
            
            # Clean up the map to keep comparison fast
            if s_count[left_char] == 0:
                del s_count[left_char]
                
            # Compare maps
            if s_count == p_count:
                result.append(i)
                
        return result