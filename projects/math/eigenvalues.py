import numpy as np

# Define the matrix
matrix = np.array([
    [2, 3, -7, 3],
    [1, 1, 3, -2],
    [4, -5, 3, 2],
    [-9, 8, 4, -3]
])

# Calculate eigenvalues
eigenvalues = np.linalg.eigvals(matrix)

print("The eigenvalues are:")
for eigenvalue in eigenvalues:
    # Round to 10 decimal places to handle floating point precision
    if abs(eigenvalue.imag) < 1e-10:
        print(f"{eigenvalue.real:.10f}")
    else:
        print(f"{eigenvalue:.10f}")

# Verify the trace
print(f"\nTrace of matrix: {np.trace(matrix)}")
print(f"Sum of eigenvalues: {np.sum(eigenvalues)}")

# Verify the determinant
print(f"\nDeterminant of matrix: {np.linalg.det(matrix)}")
print(f"Product of eigenvalues: {np.prod(eigenvalues)}")