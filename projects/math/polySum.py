from math import comb
import math
from scipy.special import bernoulli
import matplotlib.pyplot as plt
import numpy as np

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

k=-2
M = 10
B = bernoulli(M)

def poly_sum(x, k):
    sum=0
    for m in range(M+1):
        term = x**(k+1-m)*n_choose_k(k, m)*B[m]/(k+1-m)
        if math.isnan(term):
            continue
        sum+= term
    return sum

def partial_sum(x, k, a=0):
    sum = 0
    for n in range(a, x):
        sum+=n**k
    return sum

a=1
b=5
X = list(range(a, b+1))
Y_poly = [poly_sum(x, k) for x in X]
Y_partial = [partial_sum(x, k, a) for x in X]

F_a = poly_sum(a, k)
plt.scatter(X, Y_partial)
plt.plot(X, Y_poly-F_a)
plt.show()
print(Y_poly)
print(Y_partial)