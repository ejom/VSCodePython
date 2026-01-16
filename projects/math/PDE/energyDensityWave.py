import scipy as sp
import numpy as np
from scipy.integrate import dblquad, tplquad
from scipy.optimize import approx_fprime
from scipy.differentiate import derivative
from sympy import *
import matplotlib.pyplot as plt

def f(x):
    return exp(-0.01*(x[0]**2+x[1]**2+x[2]**2))/((1e-8)*(x[0]+x[1]+x[2])**2+1e-12)
def g(x):
    return 0

c=1.5

def jac(theta, t):
    return t**2*np.sin(theta)
def w1(theta, phi):
    return np.sin(theta)*np.cos(phi)
def w2(theta, phi):
    return np.sin(theta)*np.sin(phi)
def w3(theta):
    return np.cos(theta)
x1, x2, x3 = symbols('x1 x2 x3')
f_sym = exp(-(x1**2+x2**2+x3**2))/((x1+x2+x3)**2+1e-12)
fprime1 = diff(f_sym, x1)
fprime2 = diff(f_sym, x2)
fprime3 = diff(f_sym, x3)
f_x1 = lambdify((x1, x2, x3), fprime1, 'numpy')
f_x2 = lambdify((x1, x2, x3), fprime2, 'numpy')
f_x3 = lambdify((x1, x2, x3), fprime3, 'numpy')

def integrand1(theta, phi, t, x):
    return jac(theta, t)*f([x[0]+c*t*w1(theta, phi), x[1]+c*t*w2(theta, phi), x[2]+c*t*w3(theta)])
def integrand2(theta, phi, t, x):
    inputArr = (x[0]+c*t*w1(theta, phi), x[1]+c*t*w2(theta, phi), x[2]+c*t*w3(theta))
    term1 = w1(theta, phi)*f_x1(inputArr[0], inputArr[1], inputArr[2])
    term2 = w2(theta, phi)*f_x2(inputArr[0], inputArr[1], inputArr[2])
    term3 = w3(theta)*f_x3(inputArr[0], inputArr[1], inputArr[2])
    return jac(theta, t)*(term1+term2+term3)
def integrand3(theta, phi, t, x):
    return jac(theta, t)*g([x[0]+c*t*w1(theta, phi), x[1]+c*t*w2(theta, phi), x[2]+c*t*w3(theta)])

def integral1(t, x):
    val, _ = dblquad(integrand1, 0, 2*np.pi, 0, np.pi, (t, x))
    return val/(4*np.pi*t**2)
def integral2(t, x):
    val, _ = dblquad(integrand2, 0, 2*np.pi, 0, np.pi, (t, x))
    return val/(4*np.pi*t)
def integral3(t, x):
    val, _ = dblquad(integrand3, 0, 2*np.pi, 0, np.pi, (t, x))
    return val/(4*np.pi*t)

def u(t, x):
    if t==0:
        return f(x)
    return (integral1(t, x)+integral2(t, x)+integral3(t, x))*1e-6

u_spac = lambda x, t: u(t, x)
def q_KE(x1, x2, x3, t):
    x = [x1, x2, x3]
    return (approx_fprime([t], u, 1e-5, (x)))**2
def q_PE(x1, x2, x3, t):
    x = [x1, x2, x3]
    PE_comps = approx_fprime(x, u_spac, 1e-5, (t))
    return PE_comps[0]**2+PE_comps[1]**2+PE_comps[2]**2
def q(x1, x2, x3, t):
    return 0.5*(q_KE(x1, x2, x3, t) + q_PE(x1, x2, x3, t))[0]
"""
print(u(5e-9, [1.1, 1.1, 1.1]))
print(u(5e-9, [1.5, 1.5, 1.5]))
"""
plt.figure()
time = np.linspace(0, 3, 10)
spc = np.linspace(1, 5, 10)
t_i = 1
x_i = [1, 1, 1]
u_vals = []
for X in spc:
    u_vals.append(u(t_i, [X, X, 1]))
    print(f"{X}, {u_vals[-1]}")
plt.plot(spc, u_vals)
plt.show()
