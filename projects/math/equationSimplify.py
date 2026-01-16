# import sympy
from sympy import *
 
x = symbols('x')
expr = (1/30 * (x*(x-1)*(2*x-1)*(3*x**2-3*x-1)))
   
# Use sympy.simplify() method
#smpl = simplify(expr) 
   
#print("{}".format(smpl)) 
#print(f"{re(smpl)}")
#print(f"{im(smpl)}")

print(Poly(expr.expand()))