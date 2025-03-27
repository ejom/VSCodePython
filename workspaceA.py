import numpy as np
import math

def duffing_diff_transform(eta, omega, alpha, A, Omega, a, b, num_terms):
    """
    Computes the solution of the Duffing equation using the differential transform method.
    
    Args:
        eta (float): Damping coefficient
        omega (float): Natural frequency
        alpha (float): Nonlinear coefficient
        A (float): Amplitude of the forcing function
        Omega (float): Frequency of the forcing function
        a (float): Initial position
        b (float): Initial velocity
        num_terms (int): Number of terms in the series expansion
        
    Returns:
        numpy.ndarray: Solution of the Duffing equation
    """
    
    # Initialize solution array
    X = np.zeros(num_terms)
    X[0] = a
    X[1] = b
    
    # Compute the recursive terms
    for k in range(2, num_terms-2):
        term1 = (k+2)*(k+1)*X[k+2]
        term2 = omega**2*X[k]
        term3 = eta*(k+1)*X[k+1]
        term4 = 0
        for n in range(k+1):
            for m in range(n+1):
                term4 += X[m]*X[n-m]*X[k-n]
        term4 *= alpha
        term5 = -A*Omega**k*np.sin(k*np.pi/2)/math.factorial(k)
        
        X[k+2] = (term5 - term2 - term3 - term4)/(term1)
        
    return X

# Example usage
eta = 0.2
omega = 1.0
alpha = 1.0
A = 1.0
Omega = 1.0
a = 1.0
b = 0.0
num_terms = 20

# Compute the solution
solution = duffing_diff_transform(eta, omega, alpha, A, Omega, a, b, num_terms)

# Print the solution
print("Solution of the Duffing equation:")
print(solution)