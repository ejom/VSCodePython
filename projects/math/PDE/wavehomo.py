import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

L = 10
c_vals = [63.58, 84.04, 59.60, 108.6, 40.61]
eleNames = ["iron", "titanium", "copper", "aluminum", "gold"]
x_vals = np.linspace(0, L, 1000)
t_eval = 60
M=2000

#f(x)=0, A(n)=0

def g(x):
    return 100*np.sin(x)

for name, c in zip(eleNames, c_vals):

    def B(n):
        integral, _ = quad(lambda x: g(x)*np.sin(n*np.pi*x/L), 0, L)
        return (2/(n*np.pi*c))*integral

    def U(n, t, x):
        return B(n)*np.sin(n*np.pi*c*t/L)*np.sin(n*np.pi*x/L)

    def u(t, x):
        sum = 0
        for n in range(1, M+1):
            sum += U(n, t, x)
        return sum

    u_vals = u(t_eval, x_vals)
    x_u_max_idx = np.argmax(abs(u_vals))
    x_u_max = x_vals[x_u_max_idx]
    u_max = u(t_eval, x_u_max)

    print(f"max magnitude for {name} at {x_u_max}, {u_max}")

