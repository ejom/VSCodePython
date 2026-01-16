import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

L = 10
c_vals = [63.58, 84.04, 59.60, 108.6, 40.61]
eleNames = ["iron", "titanium", "copper", "aluminum", "gold"]
x_vals = np.linspace(0, L, 1000)
t_eval = 60
M = 20000

def g(x):
    return 100*np.sin(x)

for name, c in zip(eleNames, c_vals):
    n_vals = np.arange(1, M+1)
    # Precompute B(n)
    B_vals = np.array([
        (2/(n*np.pi*c)) * quad(lambda x: g(x)*np.sin(n*np.pi*x/L), 0, L)[0]
        for n in n_vals
    ])

    # Vectorized evaluation
    sin_nt = np.sin(n_vals * np.pi * c * t_eval / L)[:, np.newaxis]  # (M,1)
    sin_nx = np.sin(n_vals[:, np.newaxis] * np.pi * x_vals / L)      # (M,N)
    u_vals = (B_vals[:, np.newaxis] * sin_nt * sin_nx).sum(axis=0)   # (N,)

    x_u_max_idx = np.argmax(abs(u_vals[:300]))
    x_u_max = x_vals[x_u_max_idx]
    u_max = u_vals[x_u_max_idx]

    print(f"max magnitude for {name} at {x_u_max}, {u_max}")
    #plt.plot(x_vals, u_vals)
    #plt.title(f"Wave equation for {name}")
    #plt.show()
