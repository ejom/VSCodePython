class Solution:
    def myPow(self, x: float, n: int) -> float:
        
        # Base case for the recursion
        if n == 0:
            return 1.0
        
        # Handle negative exponents
        if n < 0:
            x = 1 / x
            n = -n
            
        # Perform the exponentiation by squaring
        
        # If n is even, x^n = (x*x)^(n/2)
        if n % 2 == 0:
            return self.myPow(x * x, n // 2)
        # If n is odd, x^n = x * x^(n-1)
        else:
            return x * self.myPow(x * x, (n - 1) // 2)