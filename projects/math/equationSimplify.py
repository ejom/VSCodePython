# import sympy
from sympy import *
 
[x, y] = symbols('x y')
expr = exp(x+y*I)*(x+y*I)**3+10*exp(2*x+2*y*I)*(x+y*I)**2+50*exp(9*x+9*y*I)*(x+y*I)+1
   
# Use sympy.simplify() method
smpl = simplify(expr) 
   
print("{}".format(smpl)) 
print(f"{re(smpl)}")
print(f"{im(smpl)}")