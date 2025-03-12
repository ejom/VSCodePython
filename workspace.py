import numpy as np
from scipy.optimize import fsolve

def f(x):
    return -30 + 21*x + 36*x**2 - 45*x**3 + 6*x**5

def f_prime(x):
    return 21 + 72*x - 135*x**2 + 30*x**4

# Find critical points by solving f'(x) = 0
x_range = np.linspace(-5, 5, 1000)
critical_points = fsolve(f_prime, [-0.5, 1, 5])  # initial guesses

# Filter critical points within the bounds
cos_x = np.cos(x_range)
y_line = -50
critical_points = critical_points[(f(critical_points) >= y_line) & (f(critical_points) <= np.max(cos_x))]

# Print the local extrema
for point in critical_points:
    print(f"Local extremum at x = {point:.2f}, f(x) = {f(point):.2f}")