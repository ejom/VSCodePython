from scipy.optimize import curve_fit, least_squares
import numpy as np


T1_data=np.array([100, 150, 200, 250, 300, 400, 600, 800, 1000, 1200])
p1_data=np.array([9009, 8992, 8973, 8951, 8930, 8884, 8787, 8642, 8568, 8458])
c1_data=np.array([0.254, 0.323, 0.357, 0.377, 0.386, 0.396, 0.431, 0.448, 0.446, 0.480])
k1_data=np.array([480, 429, 413, 406, 401, 393, 379, 366, 352, 339])

T1_Znorm = (T1_data - T1_data.mean())/T1_data.std()
c1_Znorm = (c1_data - c1_data.mean())/c1_data.std()

#c_{1}\sim a+bT_{1}+cT_{1}^{2}+dT_{1}^{3}+Ae^{BT_{1}}+Ce^{DT_{1}}
def model_c(T, a, b, c, d, A, B, C, D):
    return a+b*T+c*T**2+d*T**3+A*np.exp(B*T)+C*np.exp(D*T)

#k_{1}\sim a_{2}+b_{2}T_{1}+c_{2}T_{1}^{2}+d_{2}T_{1}^{3}+A_{2}e^{B_{2}T_{1}}+C_{2}e^{D_{2}T_{1}}
def model_k(T, a2, b2, c2, d2, A2, B2, C2, D2):
    return a2+b2*T+c2*T**2+d2*T**3+A2*np.exp(B2*T)+C2*np.exp(D2*T)

#p_{1}\sim a_{3}+b_{3}T_{1}+c_{3}e^{d_{3}T_{1}}
def model_p(T, a3, b3, c3, d3):
    return a3+b3*T+c3*np.exp(d3*T)

#bounds=([-6., 0.01, -0.0002, 3e-9, -7000, -0.005, 6000, -0.005], [-5., 0.02, -0.0001, 4e-9, -6000, -0.004, 7000, -0.004])
c_pop, _ = curve_fit(model_c, T1_Znorm, c1_Znorm, [-6., 0.01, -0.0002, 3e-9, -7000, -0.005, 6000, -0.005], method='lm')

print(c_pop)