import numpy as np
from scipy.optimize import fsolve

# Define complex function split into real and imaginary parts
def func(vec):
    x, y = vec
    z = x + 1j*y
    try:
        f = (np.exp(z) + 2 * z) * np.cos(np.exp(z) + z**2) \
            + np.log(2) * (1 / (z - 1) + 1) * 2**(z + np.log(z - 1)) \
            + 1j * z**(1j - 1) + 3 * z**2
        return [f.real, f.imag]
    except Exception:
        return [np.inf, np.inf]

# Function to compute the magnitude of f at a root
def evaluate_magnitude(vec):
    return np.linalg.norm(func(vec))

# Store accurate, unique roots
roots = []
tolerance = 1e-14

x_vals = np.arange(-5, 5.2, 0.2)
y_vals = np.arange(-5, 5.2, 0.2)

for x0 in x_vals:
    for y0 in y_vals:
        guess = [x0, y0]
        root, info, ier, _ = fsolve(func, guess, full_output=True)
        if ier == 1 and evaluate_magnitude(root) < tolerance:
            rounded_root = np.round(root, 10)
            if not any(np.allclose(root, r, atol=1e-4) for r in roots):
                roots.append(root)

# Print filtered, accurate roots

for i, r in enumerate(roots):
    print(f"Root {i+1}: {r[0]:.10f} + {r[1]:.10f}j")

for i, r in enumerate(roots):
    z = complex(r[0], r[1])
    fz = (np.exp(z) + 2 * z) * np.cos(np.exp(z) + z**2) \
        + np.log(2) * (1 / (z - 1) + 1) * 2**(z + np.log(z - 1)) \
        + 1j * z**(1j - 1) + 3 * z**2
    print(f"Root {i+1}: {r[0]:.5f} + {r[1]:.5f}j | f(z) ≈ {fz.real:.2e} + {fz.imag:.2e}i | |f(z)| ≈ {abs(fz):.2e}")

