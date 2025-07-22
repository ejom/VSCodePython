import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

# Grid parameters
nx, ny = 101, 101  # number of grid points
x = np.linspace(0, 1, nx)
y = np.linspace(0, 2, ny)
dx = x[1] - x[0]
dy = y[1] - y[0]

# Initialize solution matrix
u = np.zeros((ny, nx))

# Set boundary conditions (excluding corners)
# Bottom boundary: u(x,0) = sin(πx)
u[0, 1:-1] = np.sin(np.pi * x[1:-1])

# Top boundary: u(x,2) = 2(x+1)^-2
u[-1, 1:-1] = 2 / (x[1:-1] + 1)**2

# Left boundary: u(0,y) = -e^y
u[1:-1, 0] = -np.exp(y[1:-1])

# Right boundary: u(1,y) = 4y^3 - 20y
u[1:-1, -1] = 4 * y[1:-1]**3 - 20 * y[1:-1]

# Solve using iterative method (Gauss-Seidel)
max_iter = 10
tolerance = 1e-8

for iteration in range(max_iter):
    u_old = u.copy()
    
    # Update interior points using finite difference approximation
    for i in range(1, ny-1):
        for j in range(1, nx-1):
            u[i, j] = 0.25 * (
                u[i+1, j] + u[i-1, j] + 
                u[i, j+1] + u[i, j-1]
            )
    
    # Check convergence
    error = np.max(np.abs(u - u_old))
    if error < tolerance:
        print(f"Converged after {iteration} iterations with error {error}")
        break

# Interpolate to find u(0.7, 1.5)
x_target = 0.7
y_target = 1.5

# Find grid indices
i_x = int(x_target / dx)
i_y = int(y_target / dy)

# Bilinear interpolation
x1, x2 = x[i_x], x[i_x + 1]
y1, y2 = y[i_y], y[i_y + 1]

# Interpolation weights
wx = (x_target - x1) / (x2 - x1)
wy = (y_target - y1) / (y2 - y1)

# Bilinear interpolation
u_result = (
    u[i_y, i_x] * (1 - wx) * (1 - wy) +
    u[i_y, i_x + 1] * wx * (1 - wy) +
    u[i_y + 1, i_x] * (1 - wx) * wy +
    u[i_y + 1, i_x + 1] * wx * wy
)

print(f"u(0.7, 1.5) = {u_result}")
print(f"Rounded to 3 decimal places: {u_result:.3f}")

# Verification - check if solution satisfies Laplace equation at interior points
def check_laplace(u, dx, dy, i, j):
    laplacian = (u[i+1,j] - 2*u[i,j] + u[i-1,j])/dx**2 + (u[i,j+1] - 2*u[i,j] + u[i,j-1])/dy**2
    return abs(laplacian)

# Check a few interior points
test_points = [(50, 50), (25, 75), (75, 25)]
for i, j in test_points:
    error = check_laplace(u, dx, dy, i, j)
    print(f"Laplacian error at ({x[j]:.2f}, {y[i]:.2f}): {error:.2e}")