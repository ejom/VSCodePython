import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cmath

# Given roots
x_real = [-2.1038]
x_imag = [1.0519 - 0.5652j, 1.0519 + 0.5652j]
y_real = [-np.sqrt(3), np.sqrt(3)]
y_imag = []

# Function to compute w(z) for real x and imaginary y
def w_real_x_imag_y(x, y_imag, alpha=1):
    z = x + y_imag * 1j
    r = abs(z)
    theta = cmath.phase(z)
    if theta < 0:
        theta += 2 * np.pi
    theta += alpha
    if theta > 2 * np.pi:
        theta -= 2 * np.pi
    return np.log(r) + 1j * theta

# Function to compute w(z) for imaginary x and real y
def w_imag_x_real_y(y, x_imag, alpha=1):
    z = y + x_imag * 1j
    r = abs(z)
    theta = cmath.phase(z)
    if theta < 0:
        theta += 2 * np.pi
    theta += alpha
    if theta > 2 * np.pi:
        theta -= 2 * np.pi
    return np.log(r) + 1j * theta

# Create meshgrid for plotting
X_real, Y_imag = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
X_imag, Y_real = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))

# Evaluate w(z) for real x and imaginary y
W_real_x_imag_y_real = np.real(w_real_x_imag_y(X_real, Y_imag))
W_real_x_imag_y_imag = np.imag(w_real_x_imag_y(X_real, Y_imag))

# Evaluate w(z) for imaginary x and real y
W_imag_x_real_y_real = np.real(w_imag_x_real_y(Y_real, X_imag))
W_imag_x_real_y_imag = np.imag(w_imag_x_real_y(Y_real, X_imag))

# Plotting
fig = plt.figure(figsize=(16, 12))

# First plot: Real component of w as a function of real x and imaginary y
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax1.plot_surface(X_real, Y_imag, W_real_x_imag_y_real, cmap='viridis')
ax1.set_title('Real component of w(z) for real x and imaginary y')
ax1.set_xlabel('Real x')
ax1.set_ylabel('Imaginary y')
ax1.set_zlabel('Real w')

# Second plot: Imaginary component of w as a function of real x and imaginary y
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
ax2.plot_surface(X_real, Y_imag, W_real_x_imag_y_imag, cmap='viridis')
ax2.set_title('Imaginary component of w(z) for real x and imaginary y')
ax2.set_xlabel('Real x')
ax2.set_ylabel('Imaginary y')
ax2.set_zlabel('Imaginary w')

# Third plot: Real component of w as a function of imaginary x and real y
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
ax3.plot_surface(X_imag, Y_real, W_imag_x_real_y_real, cmap='viridis')
ax3.set_title('Real component of w(z) for imaginary x and real y')
ax3.set_xlabel('Imaginary x')
ax3.set_ylabel('Real y')
ax3.set_zlabel('Real w')

# Fourth plot: Imaginary component of w as a function of imaginary x and real y
ax4 = fig.add_subplot(2, 2, 4, projection='3d')
ax4.plot_surface(X_imag, Y_real, W_imag_x_real_y_imag, cmap='viridis')
ax4.set_title('Imaginary component of w(z) for imaginary x and real y')
ax4.set_xlabel('Imaginary x')
ax4.set_ylabel('Real y')
ax4.set_zlabel('Imaginary w')

plt.tight_layout()
plt.show()