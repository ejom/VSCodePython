import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Parameters
k = 2.3e-5        # thermal diffusivity
M = 1000          # number of modes
L = 3.0           # domain length
t_val = 3600.0       # time at which to evaluate

# Define functions
def f(x):
    return x**2 * np.sin(np.pi * x / 3) * np.cos(np.pi * x)

def P(x, n):
    return np.cos(n * np.pi * x / L)

# Compute A0
A0 = (1 / L) * quad(f, 0, L)[0]

# Pre-compute An coefficients
def An(n):
    integrand = lambda x: f(x) * P(x, n)
    return (2/L) * quad(integrand, 0, L)[0]

A_n_vals = np.array([An(n) for n in range(1, M+1)])

# Build u(x, t) vectorized
def u(x, t):
    x = np.asarray(x)
    modes = np.array([
        A_n_vals[n-1] * P(x, n) * np.exp(-k * t * (n * np.pi / L)**2)
        for n in range(1, M+1)
    ])
    return A0 + np.sum(modes, axis=0)

# Evaluate and plot u(x, 1) over x ∈ [0, 3]
x_vals = np.linspace(0, 3, 3000)
u_vals = u(x_vals, t_val)

max_u = max(u_vals)
print("MAX VALUE OF u(x, 1)")
print(max_u)

# Plot
plt.figure()
plt.plot(x_vals, u_vals)
plt.xlabel('x')
plt.ylabel('u(x, 1)')
plt.title('Temperature Profile at t = 1 s with Maximum Highlighted')
plt.grid(True)
plt.show()
