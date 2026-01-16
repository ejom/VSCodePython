import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Parameters
k_vals = [23e-6, 40e-6, 97e-6, 127e-6]
M = 1000       # number of modes
L = 1           # domain length
t_val = 1000      # time at which to evaluate

# Define functions
def f(x):
    return 1000*np.exp(-x)*np.sin(x)

def P(x, n):
    return np.sin(n * np.pi * x / L)

# Pre-compute An coefficients
def An(n):
    integrand = lambda x: f(x) * P(x, n)
    return (2/L) * quad(integrand, 0, L)[0]

A_n_vals = np.array([An(n) for n in range(1, M+1)])

# Build u(x, t) vectorized
def u_eq(x):
    return (f(L)-f(0))*x/L+f(0)
def u(x, t):
    u_sol = []
    x = np.asarray(x)
    for k in k_vals:
        modes = np.array([
            A_n_vals[n-1] * P(x, n) * np.exp(-k * t * (n * np.pi / L)**2)
            for n in range(1, M+1)
        ])
        u_sol.append(np.sum(modes, axis=0)+u_eq(x))
    return u_sol

x_vals = np.linspace(0, 1, 1000)
u_p_vals = u(x_vals, t_val)

for u_p_sol in u_p_vals:
    max_u = max(u_p_sol)
    print("MAX VALUE diff OF u(x, 1000)")
    print(max_u)



plt.plot(x_vals, u_p_vals[0])
plt.show()