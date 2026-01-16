import numpy as np
from math import comb

def n_choose_k(n, k):
    #Calculates n choose k for negative n using the extended binomial coefficient formula.
    
    if k < 0:
        return 0  # By definition, n choose k is 0 if k is negative
    
    if n >= 0:
        return comb(n, k) # Use standard comb for non-negative n

    # Apply the identity for negative n
    # n_prime = k - n - 1
    # Example: n = -5, k = 3 => n_prime = 3 - (-5) - 1 = 7.  (-1)^3 * comb(7, 3)
    n_prime = k - n - 1 
    
    # Calculate (-1)^k
    sign = -1 if k % 2 else 1
    
    # Calculate comb(n_prime, k)
    return sign * comb(n_prime, k)

N=-2
a0 = 1/(N+1)

def a(k):
    sum = -a0*n_choose_k(N+1, k+1)
    for h in range(1, k-1+1):
        #print(sum)
        sum += -a(h)*n_choose_k(N+1-h, k+1-h)
        #print(a(h)*n_choose_k(N+1-h, k+1-h))
        #print(sum)

    return sum / (N+1-k)

params = [a0]
print(f"1: {a0}")

#Specify max number of terms
M=10

if N>=0:
    numTerms = N+1
else:
    numTerms = M
for k in range(1, numTerms):
    print(f"{1+k}: {a(k)}")
    params.append(a(k))

print(params)
