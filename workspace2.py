import numpy as np

def simplex_algorithm():
    # Initial tableau setup based on the problem
    # The tableau structure follows what's described in the article where
    # we set up an augmented matrix
    tableau = np.array([
        [1, 1, 1, 1, 1, 0, 5],    # First constraint
        [1, 2, 3, 2, 0, 1, 6],    # Second constraint
        [-3, 3, 1, -4, 0, 0, 0]   # Objective function (negated)
    ], dtype=float)
    
    # Main simplex loop
    while not is_optimal(tableau):
        # Select pivot column (entering variable)
        pivot_col = get_pivot_column(tableau)
        if pivot_col == -1:
            return "Unbounded solution"
        
        # Select pivot row (leaving variable)
        pivot_row = get_pivot_row(tableau, pivot_col)
        if pivot_row == -1:
            return "No solution exists"
        
        # Perform pivot operation
        tableau = pivot(tableau, pivot_row, pivot_col)
        
    return get_solution(tableau)

def is_optimal(tableau):
    # Check if all coefficients in objective row are non-negative
    return all(x >= 0 for x in tableau[-1, :-1])

def get_pivot_column(tableau):
    # Find most negative coefficient in objective row
    objective_row = tableau[-1, :-1]
    min_val = min(objective_row)
    if min_val >= 0:
        return -1
    return np.argmin(objective_row)

def get_pivot_row(tableau, pivot_col):
    # Use minimum ratio test
    ratios = []
    rhs = tableau[:-1, -1]
    column = tableau[:-1, pivot_col]
    
    for i in range(len(rhs)):
        if column[i] <= 0:
            ratios.append(float('inf'))
        else:
            ratios.append(rhs[i] / column[i])
    
    if min(ratios) == float('inf'):
        return -1
    return ratios.index(min(ratios))

def pivot(tableau, pivot_row, pivot_col):
    new_tableau = np.zeros_like(tableau)
    pivot_element = tableau[pivot_row, pivot_col]
    
    # Pivot row operation
    new_tableau[pivot_row] = tableau[pivot_row] / pivot_element
    
    # Other rows operations
    for i in range(len(tableau)):
        if i != pivot_row:
            new_tableau[i] = tableau[i] - tableau[i, pivot_col] * new_tableau[pivot_row]
    
    return new_tableau

def get_solution(tableau):
    solution = np.zeros(4)  # For x, y, z, w
    rhs = tableau[:, -1]
    
    for i in range(4):
        col = tableau[:, i]
        if sum(abs(col)) == 1:
            row = np.where(col == 1)[0][0]
            solution[i] = rhs[row]
    
    objective_value = -tableau[-1, -1]  # Note: we negated the objective function
    return solution, objective_value

# Run the algorithm
solution, objective_value = simplex_algorithm()
print(f"Solution (x, y, z, w): {solution}")
print(f"Maximum value: {objective_value}")