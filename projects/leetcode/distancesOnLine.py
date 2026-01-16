def sumDistance(nums, s: str, d: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # 1. Ignore collisions: move robots based on their initial direction
        for i in range(n):
            if s[i] == 'R':
                nums[i] += d
            else:
                nums[i] -= d
        
        # 2. Sort the final positions to calculate distances efficiently
        nums.sort()
        
        # 3. Calculate sum of all pairwise distances
        # Formula: Sum = Σ (nums[i] * i - nums[i] * (n - 1 - i))
        total_dist = 0
        for i in range(n):
            # i is how many elements are to the left of nums[i]
            # (n - 1 - i) is how many elements are to the right of nums[i]
            total_dist += i * nums[i] - (n - 1 - i) * nums[i]
            
        return total_dist % MOD

print(sumDistance([-3, -6, 0, -1], "LRLR", 2))
print(sumDistance([-3, -6, 0], "LRL", 2))