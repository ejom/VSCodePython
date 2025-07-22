import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

#We need at analyze the ODE y'(t)+(3t^2+t-1)y(t)=sin(t-4)
#Define the ODE as y'(t) = sin(t-4) - (3t^2+t-1)y(t)
def y_t(t, y):
    return np.sin(t-4) - (3*t**2+t-1)*y

#Solve the ODE for y(t) using y(0)=0
y_0=0
#We visually inspect that a good range for t is [-1, 2]
min_t = -1
max_t = 2
#Solve for t>=0
y_tpos = solve_ivp(y_t, [0, max_t], [y_0], dense_output=True)
#Solve for t<=0
y_tneg = solve_ivp(y_t, [0, min_t], [y_0], dense_output=True)
#Stich positive and negetive solutions together
def y(t, ypos=y_tpos, yneg=y_tneg):
    if t>0:
        return ypos.sol(t)[0]
    elif t<0:
        return yneg.sol(t)[0]
    else:
        return 0

#Solve y'(t) can call it y_prime
def y_prime(t):
    return y_t(t, y(t))

#Find y''(t)
#we already have y'(t) = sin(t-4) - (3t^2+t-1)y(t)
#y''(t) = d/dt(sin(t-4) - (3t^2+t-1)y(t))
#y''(t) = cos(t-4) - (6t+1)y(t) - (3t^2+t-1)y'(t)
def y_2prime(t):
    return np.cos(t-4) - (6*t+1)*y(t) - (3*t**2+t-1)*y_prime(t)

#Find the critical points, values of t when y_prime = 0
#We can see from the graph that these will be around t=0.6 and 1.8
critGuesses = [0.6, 1.8]
critPoints = []
for guess in critGuesses:
    t_val = root(y_prime, guess).x[0]
    critPoints.append((round(float(t_val), 2), round(float(y(t_val)), 2)))
#Find the inflection points, t when y_2prime = 0
#We can see from the graph that these will be around t=0.04, -0.4, and 1
inflGuesses = [0.04, -0.4, 1]
inflPoints = []
for guess in inflGuesses:
    t_val = root(y_2prime, guess).x[0]
    inflPoints.append((round(float(t_val), 2), round(float(y(t_val)), 2)))

#Print the json solution in the desired format:
print("{")
print(f"\"critical\": {critPoints}")
print(f"\"inflection\": {inflPoints}")
print("}")