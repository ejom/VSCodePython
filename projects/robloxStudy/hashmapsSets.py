from collections import defaultdict
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # A defaultdict(list) creates a new list for a key if it doesn't exist.
        anagram_map = defaultdict(list)

        for word in strs:
            # The sorted string is the unique key for any group of anagrams.
            # For example, both "eat" and "tea" produce the key "aet".
            key = "".join(sorted(word))
            
            # Append the original word to the list associated with its sorted key.
            anagram_map[key].append(word)
            
        # The values of the map are the lists of grouped anagrams.
        return list(anagram_map.values())