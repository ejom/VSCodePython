from collections import deque

class Solution:
    def numsSameConsecDiff(self, n: int, k: int) -> list[int]:
        # Start with all possible first digits (1-9)
        queue = deque([1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        # We already have numbers of length 1, 
        # so we need to perform n-1 more steps to reach length n.
        for _ in range(n - 1):
            level_size = len(queue)
            for _ in range(level_size):
                num = queue.popleft()
                last_digit = num % 10
                
                # Potential next digits
                next_digits = set()
                if 0 <= last_digit + k <= 9:
                    next_digits.add(last_digit + k)
                if 0 <= last_digit - k <= 9:
                    next_digits.add(last_digit - k)
                
                for next_digit in next_digits:
                    new_num = num * 10 + next_digit
                    queue.append(new_num)
                    
        return list(queue)
    
sol = Solution()
print(sol.numsSameConsecDiff(3, 7))