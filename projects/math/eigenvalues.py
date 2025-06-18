import numpy as np
import threading
import queue
import time
from sympy import Matrix, I, re, im

# Define the matrix ONCE with sympy notation
matrix_values = [
    [7581907*I, -693782, 603921, 693096*I],     
    [1653, 762, -7632, -76325],     
    [47632, -5763983000000000000000000000000000000000600000000000000000000000000000001*I, 75391, 2247],     
    [-9763, 87, 47320000000000000000000000000000000000000000000000001, 77392]
]

# Create symbolic matrix for exact calculations
symbolic_matrix = Matrix(matrix_values)

# Create numpy matrix for numerical calculations
# Extract values properly from sympy expressions
numpy_matrix = np.zeros((4, 4), dtype=complex)
for i in range(4):
    for j in range(4):
        if hasattr(matrix_values[i][j], 'is_complex'):
            # Extract real and imaginary parts for sympy numbers
            numpy_matrix[i, j] = float(re(matrix_values[i][j])) + 1j*float(im(matrix_values[i][j]))
        else:
            # For regular numbers
            numpy_matrix[i, j] = complex(matrix_values[i][j])

# First, always calculate the numerical solution
print("NUMERICAL SOLUTION:")
print("-" * 50)
eigenvalues, eigenvectors = np.linalg.eig(numpy_matrix)

for i, eigenvalue in enumerate(eigenvalues):
    if abs(eigenvalue.imag) < 1e-10:
        print(f"\nEigenvalue: λ{i+1} = {eigenvalue.real:.10f}")
    else:
        print(f"\nEigenvalue: λ{i+1} = {eigenvalue:.10f}")
    
    print("Eigenvector:")
    for j in range(eigenvectors.shape[0]):
        if abs(eigenvectors[j, i].imag) < 1e-10:
            print(f"  {eigenvectors[j, i].real:.10f}")
        else:
            print(f"  {eigenvectors[j, i]:.10f}")

print("\n\nEXACT SOLUTION ATTEMPT:")
print("-" * 50)

# Now attempt exact calculation with queue-based timeout
result_queue = queue.Queue()

def calculate_symbolic_solution(q):
    try:
        # Calculate eigenvects
        symbolic_result = symbolic_matrix.eigenvects()
        
        # Format the output
        output = "\nExact symbolic form:\n"
        for eigenval, multiplicity, eigenvecs in symbolic_result:
            output += f"\nEigenvalue: {eigenval} (multiplicity: {multiplicity})\n"
            for vec in eigenvecs:
                output += f"Eigenvector: {vec.T}\n"
        
        q.put(("result", output))
    except Exception as e:
        q.put(("error", str(e)))

# Run the entire symbolic calculation with timeout
thread = threading.Thread(target=calculate_symbolic_solution, args=(result_queue,), daemon=True)
thread.start()

# Wait for result or timeout
timeout_seconds = 60
try:
    result_type, result_data = result_queue.get(timeout=timeout_seconds)
    
    if result_type == "result":
        print(result_data)
    elif result_type == "error":
        print(f"Error in exact calculation: {result_data}")
except queue.Empty:
    print(f"Exact calculation timed out after {timeout_seconds} seconds")