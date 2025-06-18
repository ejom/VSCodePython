from sympy import symbols, exp, sin, cos, nsolve
import numpy as np

# 1) Define symbols
x, y = symbols('x y')

# 2) Define the real and imaginary parts
f1 = (
    exp(x)*x*(x**2 - 3*y**2)*cos(y)
    + 10*exp(2*x)*(x**2 - y**2)*cos(2*y)
    - 3*exp(x)*x**2*y*sin(y)
    + exp(x)*y**3*sin(y)
    - 20*exp(2*x)*x*y*sin(2*y)
    - 50*exp(9*x)*y*sin(9*y)
    + 50*exp(9*x)*x*cos(9*y)
    + 1
)

f2 = (
    exp(x)*(x**3*sin(y) - y*(y**2 - 3*x**2)*cos(y))
    + 10*exp(2*x)*x**2*sin(2*y)
    - 3*exp(x)*x*y**2*sin(y)
    - 10*exp(2*x)*y**2*sin(2*y)
    + 50*exp(9*x)*x*sin(9*y)
    + 20*exp(2*x)*x*y*cos(2*y)
    + 50*exp(9*x)*y*cos(9*y)
)

# 3) Build a 10×10 grid of initial guesses
xg = np.linspace(0.02, -7.4, 10)
yg = np.linspace(0, 9,      10)
guesses = [[xx, yy] for xx in xg for yy in yg]

# 4) Set up skip‐logic & storage
tol_skip   = 0.01     # skip if within 0.01 in both x and y
skip_count = 0
found      = set()

def is_near_existing(pt):
    return any(
        abs(pt[0] - x0) < tol_skip and abs(pt[1] - y0) < tol_skip
        for x0, y0 in found
    )

# 5) Main solve loop
for idx, guess in enumerate(guesses, 1):
    if is_near_existing(guess):
        skip_count += 1
        if skip_count % 20 == 0:
            print(f"...skipped {skip_count} silent guesses so far")
        continue

    try:
        sol = nsolve([f1, f2], [x, y], guess, tol=1e-6, maxsteps=30)
        sol_tup = tuple(round(float(s), 5) for s in sol)
        if sol_tup not in found:
            found.add(sol_tup)
            print(f"New root #{len(found)}: {sol_tup} (from guess={guess})")
    except Exception:
        skip_count += 1
        if skip_count % 20 == 0:
            print(f"...skipped {skip_count} silent guesses so far")
        continue


