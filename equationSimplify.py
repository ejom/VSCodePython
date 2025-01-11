# import sympy
from sympy import *
 
r, theta = symbols('r theta')
expr =  (r*cos(theta))**3 + (r*sin(theta)-5)**3 + (r*cos(theta))**2 * ((r*sin(theta))+5)**2 + (r*cos(theta)) * (r*sin(theta)+5) - 2
   
# Use sympy.simplify() method
smpl = simplify(expr) 
   
print("{}".format(smpl)) 