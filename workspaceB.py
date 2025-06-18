import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define the ODE system as before
def system(t, Y):
    y0, y1, y2, y3, y4 = Y
    rhs = - (t**4 + t + 1 + t*np.exp(t)*y3 + t*np.cos(4*t)*y2 + y0)
    y5 = rhs / np.sin(t)
    return [y1, y2, y3, y4, y5]

# Initial conditions at t0 = 0.1
Y0 = [0, 0, 0, 0, 0]

# Integrate forward and backward
t_fwd = np.linspace(0.1, 1.0, 150)
sol_fwd = solve_ivp(system, (0.1, 1.0), Y0, t_eval=t_fwd)

t_bwd = np.linspace(0.1, -1.0, 150)
sol_bwd = solve_ivp(system, (0.1, -1.0), Y0, t_eval=t_bwd)

# Stitch results
t_all   = np.hstack([sol_bwd.t[::-1], sol_fwd.t[1:]])
y_all   = np.hstack([sol_bwd.y[:, ::-1], sol_fwd.y[:, 1:]])

# Evaluation at specific test points
test_points = [-1.0, -0.5, 0.0, 0.5]
data = {'t': [], 'y': [], "y'": [], "y''": [], "y'''": [], "y⁽⁴⁾": []}

for tp in test_points:
    idx = np.argmin(np.abs(t_all - tp))
    data['t'].append(t_all[idx])
    for i, key in enumerate(['y', "y'", "y''", "y'''", "y⁽⁴⁾"]):
        data[key].append(y_all[i, idx])
        print(f"y({t_all[idx]:.3f}) ≈ {y_all[i, idx]:.6f} ({key})")

# Compute the 5th derivative at each point
y5_all = np.array([ system(t_all[i], y_all[:, i])[4]
                    for i in range(len(t_all)) ])

# Now plot all six curves:
plt.figure(figsize=(8,6))
labels = ["y(t)", "y'(t)", "y''(t)", "y'''(t)", "y⁽⁴⁾(t)", "y⁽⁵⁾(t)"]
for i in range(y_all.shape[0]):
    plt.plot(t_all, y_all[i], label=labels[i])
plt.plot(t_all, y5_all, label="y⁽⁵⁾(t)")  # dashed for distinction

plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.xlabel("t")
plt.ylabel("Value")
plt.title("ODE Solution and Derivatives on [-1, 1]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Choose the time at which to evaluate the 5th derivative
t_val = 0.5

# Find the closest index in the solution
idx = np.argmin(np.abs(sol_fwd.t - t_val))
t_closest = sol_fwd.t[idx]

# Get y, y'', y''', etc. at that point
y = sol_fwd.y[0][idx]
y_dd = sol_fwd.y[2][idx]   # y''(t)
y_ddd = sol_fwd.y[3][idx]  # y'''(t)

# Compute y⁽⁵⁾(t) using the known formula
numerator = -(t_closest**4 + t_closest + 1 + t_closest * np.exp(t_closest) * y_ddd +
              t_closest * np.cos(4*t_closest) * y_dd + y)
denominator = np.sin(t_closest)

y5 = numerator / denominator

print(f"y⁽⁵⁾({t_closest:.3f}) ≈ {y5:.6f}")
