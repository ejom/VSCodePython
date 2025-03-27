import numpy as np
from math import sin, pi

def duffing_recurrence(eta, omega, alpha, A, Omega, a, b, n_terms):
    # Initialize the first two terms
    X = [a, b]

    # Recurrence relation to compute the next term
    def next_term(k):
        if k >= n_terms - 2:
            return 0

        term = (k+2)*(k+1) * X[k+2]
        term += omega**2 * X[k]
        term += eta*(k+1) * X[k+1]
        term += alpha * sum([X[m] * X[n-m] * X[k-n] for m in range(k+1) for n in range(k+1-m)])
        term -= (A * Omega**k * sin(k*pi/2)) / factorial(k)
        term /= (k+2)*(k+1)

        return term

    # Compute the next n_terms - 2 terms
    for _ in range(n_terms - 2):
        X.append(next_term(len(X)))

    return X

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Example usage
eta = 0.1
omega = 1
alpha = 1
A = 1
Omega = 1
a = 1
b = 0
n_terms = 10

X = duffing_recurrence(eta, omega, alpha, A, Omega, a, b, n_terms)
print("X(k) values:")
print(X)