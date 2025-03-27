def generate_recursive_equations(eta, omega, alpha, num_terms):
    """
    Generates a system of recursive equations for different values of k.
    
    Args:
        eta (float): Damping coefficient
        omega (float): Natural frequency
        alpha (float): Nonlinear coefficient
        num_terms (int): Number of terms in the series expansion
        
    Returns:
        None
    """
    
    print("System of Recursive Equations:")
    for k in range(2, num_terms):
        term1 = (k+2)*(k+1)
        term2 = omega**2
        term3 = eta*(k+1)
        term4 = 0
        for n in range(k+1):
            for m in range(n+1):
                term4 += f"X[{m}]*X[{n-m}]*X[{k-n}]"
        term4 = f"{alpha}*({term4})"
        
        equation = f"{term1}*X[{k+2}] + {term2}*X[{k}] + {term3}*X[{k+1}] + {term4} = 0"
        print(f"For k={k}: {equation}")

# Example usage
eta = 0.2
omega = 1.0
alpha = 1.0
num_terms = 10

# Generate the recursive equations
generate_recursive_equations(eta, omega, alpha, num_terms)