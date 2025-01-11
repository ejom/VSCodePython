import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import fsolve

theta = float
def func(r):
    return (r*np.cos(theta))**3 + (r*np.sin(theta)-5)**3 + (r*np.cos(theta))**2 * ((r*np.sin(theta))+5)**2 + (r*np.cos(theta)) * (r*np.sin(theta)+5) - 2
# Update the initial guess based on the plot inspection 
guesses = [2, 6, 30]

# setting the axes 
# projection as polar 
plt.axes(projection = 'polar') 

# creating an array 
# containing the radian values 
rads = np.arange(0, (2 * np.pi), 0.001) 

# plotting the cardioid 
for theta in rads: 
    for guess in guesses:
        fr = fsolve(func, guess) 
        plt.polar(theta,fr,'g.') 

# display the polar plot 
plt.show()
