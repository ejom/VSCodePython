import numpy as np
from scipy.optimize import minimize_scalar

# Define the temperature function at t=0
def f(x):
    """
    Initial temperature distribution function.
    f(x) = x^2 * sin(pi*x/3) * cos(pi*x)
    """
    return x**2 * np.sin(np.pi * x / 3) * np.cos(np.pi * x)

# To find the maximum, we can minimize the negative of the function
def neg_f(x):
    """
    Negative of the initial temperature distribution function.
    """
    return -f(x)

# Find the minimum of f(x) in the interval [0, 3]
cold_result = minimize_scalar(f, bounds=(0, 3), method='bounded')

# Find the minimum of -f(x) in the interval [0, 3] to find the maximum of f(x)
hot_result = minimize_scalar(neg_f, bounds=(0, 3), method='bounded')

# Extract the results
coldest_x = cold_result.x
coldest_temp = cold_result.fun
hottest_x = hot_result.x
hottest_temp = -hot_result.fun  # Negate the result to get the maximum value

# The time for both hottest and coldest points is t=0, based on the maximum principle for the heat equation.
time = 0.0

# Print the final formatted answer, rounded to one decimal place
print("{")
print(f"\"hottest\": ({hottest_x:.1f}, {time:.1f}, {hottest_temp:.1f}),")
print(f"\"coldest\": ({coldest_x:.1f}, {time:.1f}, {coldest_temp:.1f})")
print("}")