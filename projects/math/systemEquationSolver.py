from sympy import symbols, exp, tan, nsolve, cos, sin, sqrt
from scipy.integrate import quad
import numpy as np

t, x = symbols('t x')

c = sqrt(7)

def g(x):
    return (-x**4-x**2+x)/(tan(x**2))

def f(x):
    return x**3+x**2-x+exp(x)

def u(x, t):
    integral, _ = quad(g, x-t, x+t)
    return 0.5*(f(x+t)+f(x-t)+integral)

u_1x = (
    (
    100*sin(x + c*t)/(x + c*t)**2
    - 100*cos(x + c*t)/(x + c*t)
    + 100*sin(x - c*t)/(x - c*t)**2
    - 100*cos(x - c*t)/(x - c*t)
) / 2
)
#U_{t}\left(t,\ x\right)=6xt+2t+\frac{1}{2}\left(e^{t}-e^{-t}\right)e^{x}+\frac{1}{2}\left(g\left(x+t\right)+g\left(x-t\right)\right)

u_1t = (
    (
    100*c*sin(c*t + x)/(c*t + x)**2
    - 100*c*cos(c*t + x)/(c*t + x)
    + 100*c*sin(c*t - x)/(x - c*t)**2
    + 100*c*cos(c*t - x)/(x - c*t)
) / 2
)

u_2x = (
    100*sin(x + c*t)/(x + c*t)**2
    - 100*cos(x + c*t)/(x + c*t)
    - 100*sin(x - c*t)/(c*t - x)**2
    - 100*cos(x - c*t)/(c*t - x)
) / 2

u_2t = (
    100*c*sin(c*t + x)/(c*t + x)**2
    - 100*c*cos(c*t + x)/(c*t + x)
    - 100*c*sin(c*t - x)/(c*t - x)**2
    + 100*c*cos(c*t - x)/(c*t - x)
) / 2

sol = nsolve()
print(sol)

