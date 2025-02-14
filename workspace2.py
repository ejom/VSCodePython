import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# Define the function
def f(x):
    return x * np.sin(np.exp(0.1 * x))

# Define the x range from -50 to 50
x_vals = np.linspace(-50, 50, 500)  # More points for a smoother curve

# Compute function values
y_vals = f(x_vals)

# Find the index where x = 0
zero_index = np.argmin(np.abs(x_vals))

# Compute the numerical integral from x = 0
integral_vals = cumulative_trapezoid(y_vals, x_vals, initial=0)
integral_vals -= integral_vals[zero_index]  # Shift so that F(0) = 0

def F(x):
    return integral_vals

# Plot the function and its integral
#plt.figure(figsize=(10, 6))
#plt.plot(x_vals, y_vals, label=r'$f(x) = x \sin(e^{0.1x})$', color='blue')
##plt.plot(x_vals, integral_vals, label=r'$F(x) = \int_{0}^{x} f(t) dt$', color='red')
#plt.axhline(0, color='black', linewidth=0.5)
#plt.axvline(0, color='black', linewidth=0.5)
#plt.legend()
#plt.grid()
#plt.xlabel('x')
#plt.ylabel('y')
#plt.title('Function and Its Integral with $F(0) = 0$')
#plt.show()

eval_x_vals = np.arange(-50, 51, 10)  # Values: -50, -40, ..., 50

print(eval_x_vals)

print(f(eval_x_vals))
print(F(eval_x_vals))