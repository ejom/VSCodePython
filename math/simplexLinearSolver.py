import numpy as np
from scipy.optimize import linprog

def solve_linear_program():
    # Define the objective function coefficients (negative because linprog minimizes)
    # For f(x,y,z,w) = 3x-3y-z+4w, we use [-3, 3, 1, -4] to minimize -f
    c = [5, 10]
    
    # Define the equality constraints matrix
    # x + y + z + w = 5
    # x + 2y + 3z + 2w = 6
    A_ub = [[1, 1], [-1, -1]]
    
    # Define the equality constraints right-hand side
    b_ub = [25, -15]
    
    # Define bounds for variables (all non-negative)
    bounds = [(5, None), (7, None)]
    
    # Solve the linear program
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='simplex')
    
    return result

# Run the solver
result = solve_linear_program()
print("Optimization result:")
print(f"x = {result.x[0]:.2f}")
print(f"y = {result.x[1]:.2f}")
print(f"Maximum value of f = {result.fun:.2f}")