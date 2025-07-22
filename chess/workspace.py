import numpy as np
from scipy.integrate import tplquad, dblquad

def spherical_to_cartesian(rho, theta, phi):
    return np.array([
        rho * np.sin(phi) * np.cos(theta),
        rho * np.sin(phi) * np.sin(theta),
        rho * np.cos(phi)
    ])

def solve_u(f_cart, g_cart, phi, theta, rho):
    # Convert evaluation point to Cartesian and compute image point
    x = spherical_to_cartesian(rho, theta, phi)
    x_star = x / (rho**2)
    
    # Green's function in the ball of radius 1
    def G(y):
        return (
            -1 / (4 * np.pi * np.linalg.norm(x - y))
            + 1 / (4 * np.pi * np.linalg.norm(x) * np.linalg.norm(x_star - y))
        )
    
    def vol_integrand(theta_y, phi_y, rho_y):
        y = spherical_to_cartesian(rho_y, theta_y, phi_y)
        return G(y) * f_cart(*y) * rho_y**2 * np.sin(phi_y)
    
    int_vol, err_vol = tplquad(
        vol_integrand,
        0, 1,                              # rho from 0 to 1
        lambda _rho: 0, lambda _rho: np.pi,          # phi from 0 to π
        lambda _rho, _phi: 0, lambda _rho, _phi: 2*np.pi,  # theta from 0 to 2π
        epsabs=1e-5, epsrel=1e-5
    )
    
    def surf_integrand(theta_y, phi_y):
        y = spherical_to_cartesian(1, theta_y, phi_y)
        normal_deriv = (rho**2 - 1) / (4 * np.pi * np.linalg.norm(x - y)**3)
        return g_cart(*y) * normal_deriv * np.sin(phi_y)
    
    int_surf, err_surf = dblquad(
        surf_integrand,
        0, np.pi,                         # phi from 0 to π
        lambda _: 0, lambda _: 2*np.pi,  # theta from 0 to 2π
        epsabs=1e-5, epsrel=1e-5
    )
    
    return int_vol + int_surf

# Example input functions
def f_cart(x, y, z):
    return x**2 + np.cos(x)*y - z**3 * np.sin(x)

def g_cart(x, y, z):
    return x - y + z

u_val = solve_u(f_cart, g_cart, phi=1.0, theta=1.0, rho=0.5)
print(round(u_val, 3))
