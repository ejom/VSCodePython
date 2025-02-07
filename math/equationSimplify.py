# import sympy
from sympy import *
 
x = symbols('x')
expr = (x+3)*(x-2)**2*(x-7)+4*x+1
   
# Use sympy.simplify() method
smpl = simplify(expr) 
   
print("{}".format(smpl)) 