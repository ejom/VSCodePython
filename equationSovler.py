import numpy as np
from scipy.optimize import fsolve
theta = float
def func(r):
    return (r*np.cos(theta))**3 + (r*np.sin(theta)-5)**3 + (r*np.cos(theta))**2 * ((r*np.sin(theta))+5)**2 + (r*np.cos(theta)) * (r*np.sin(theta)+5) - 2
# Update the initial guess based on the plot inspection 
initial_guesses = [0] 
# Find roots using multiple initial guesses 
for guess in initial_guesses: 
    root = fsolve(func, guess) 
    print(f"Initial guess: {guess}, Root: {root[0]:0.6f}")
