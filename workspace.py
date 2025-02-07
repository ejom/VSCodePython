import numpy as np
from sympy import Symbol, Matrix, expand, I

def find_characteristic_equation_and_eigenvalues(matrix):
    # Convert the matrix to a NumPy array for eigenvalue calculation
    A_np = np.array(matrix, dtype=float)
    
    # Calculate eigenvalues using NumPy
    eigenvalues = np.linalg.eigvals(A_np)
    
    # Generate the characteristic equation using SymPy
    λ = Symbol('λ')
    n = len(matrix)
    
    # Convert to SymPy matrix and create characteristic matrix
    A = Matrix(matrix)
    I = Matrix.eye(n)
    char_matrix = A - λ * I
    
    # Calculate the determinant symbolically
    char_equation = expand(char_matrix.det())
    
    return char_equation, eigenvalues

# The given matrix
matrix = [
    [7, -3, 3, -6],
    [5, 5, -2, -9],
    [-7, 4, 6, -3],
    [-8, 4, 5, 8]
]

# Find characteristic equation and eigenvalues
char_equation, eigenvalues = find_characteristic_equation_and_eigenvalues(matrix)

# Print results
print("Characteristic Equation:")
print(f"P(λ) = {char_equation}")
print("\nEigenvalues:")
for i, ev in enumerate(eigenvalues, 1):
    print(f"λ{i} = {ev}")

# Verify eigenvalues by substituting into characteristic equation
print("\nVerification by substituting eigenvalues into characteristic equation:")
λ = Symbol('λ')
for i, ev in enumerate(eigenvalues, 1):
    # Convert numpy complex to sympy complex
    sympy_ev = complex(ev.real) + I * complex(ev.imag)
    result = complex(char_equation.subs(λ, sympy_ev).evalf())
    print(f"P({ev}) = {abs(result):.2e}")  # Using absolute value for clearer verification