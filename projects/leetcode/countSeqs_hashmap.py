from collections import defaultdict
import math

class Solution:
    def numberOfSubsequences(self, nums: list[int]) -> int:
        n = len(nums)
        ans = 0
        # Map to store frequency of ratios (nums[p] / nums[q])
        # Key: (simplified_numerator, simplified_denominator)
        count = defaultdict(int)
        
        # r is our pivot. We need r + 2 < n for s to exist.
        # We start r at 4 because p, gap, q, gap, r requires at least 5 elements.
        for r in range(4, n - 2):
            # As r moves, the possible q is fixed at r - 2.
            # We now find all possible p for this new q.
            q = r - 2
            for p in range(q - 1): # p < q - 1 ensures gap of 1
                g = math.gcd(nums[p], nums[q])
                ratio = (nums[p] // g, nums[q] // g)
                count[ratio] += 1
            
            # Now, for the current r, look at all valid s.
            for s in range(r + 2, n):
                g = math.gcd(nums[s], nums[r])
                # We need nums[p]/nums[q] == nums[s]/nums[r]
                target_ratio = (nums[s] // g, nums[r] // g)
                ans += count[target_ratio]
                
        return ans
    
sol = Solution()
print(sol.numberOfSubsequences([3,4,3,4,3,4,3,4]))