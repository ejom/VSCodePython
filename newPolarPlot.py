import numpy as np
import matplotlib.pyplot as plt

# Define the function in polar coordinates
def f(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x**2+y**2 - 5

# Create a grid of r and theta values
r = np.linspace(0, 40, 400)
theta = np.linspace(0, 2*np.pi, 400)
R, Theta = np.meshgrid(r, theta)

# Evaluate the function on the grid
Z = f(R, Theta)

# Plot the contour in polar coordinates
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection='polar')
ax.contour(Theta, R, Z, levels=[0], colors='b')
ax.set_title('Polar Plot of f(r, theta) = 0')
plt.show()
