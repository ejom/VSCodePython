import numpy as np
from scipy.optimize import fsolve

def f(x):
    return -30 + 21*x + 36*x**2 - 45*x**3 + 6*x**5

def f_prime(x):
    return 21 + 72*x - 135*x**2 + 30*x**4

def cos_func(x):
    return np.cos(x)

def y_bound(x):
    return -50

# Define the function to find where f(x) = cos(x) or f(x) = -50
def find_intersections(func, x_range):
    x_vals = np.linspace(x_range[0], x_range[1], 1000)
    y_func = func(x_vals)
    y_cos = cos_func(x_vals)
    y_boun = y_bound(x_vals)
    
    intersections_cos = x_vals[np.isclose(y_func, y_cos, atol=1e-2)]
    intersections_bound = x_vals[np.isclose(y_func, y_bound, atol=1e-2)]
    
    return np.concatenate((intersections_cos, intersections_bound))

# Find the bounds
x_range = (-5, 5)  # Adjust this range based on your visual inspection of the graph
bounds = find_intersections(f, x_range)

# Find critical points within the bounds
critical_points = []
for bound in bounds:
    solution = fsolve(f_prime, bound)
    if np.isclose(f_prime(solution), 0, atol=1e-2):
        critical_points.append(solution[0])

# Evaluate f at critical points
local_extrema = [(x, f(x)) for x in critical_points]

# Print results
print("Local Extrema within the bounds:")
for point in local_extrema:
    print(f"x = {point[0]:.2f}, f(x) = {point[1]:.2f}")