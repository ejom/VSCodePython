from sympy.parsing.sympy_parser import *
from sympy import *
import numpy as np
import matplotlib.pyplot as plt

def inputStrToSymExpr(inputStr: str):
    inputStr = inputStr.replace('sin', ' sin')
    inputStr = inputStr.replace('cos', ' cos')
    inputStr = inputStr.replace('tan', ' tan')

    x, y = symbols('x y', real=True)
    local_dict = {
        'i': I,
        'e': exp(1),
        'x': x,
        'y': y,
    }

    transformations = (standard_transformations + (convert_xor, implicit_multiplication_application,))
    return parse_expr(inputStr, local_dict=local_dict, transformations=transformations)

def findCritInRange(fun1, fun2, x, y, x_min_max, y_min_max, numpoints):
    x_guesses = np.linspace(x_min_max[0], x_min_max[-1], numpoints)
    y_guesses = np.linspace(y_min_max[0], y_min_max[-1], numpoints)
    crit_points = set()
    for y_guess in y_guesses:
        for x_guess in x_guesses:
            try:
                x_root, y_root = nsolve((fun1, fun2), (x, y), (float(x_guess), float(y_guess)))
                if x_root<x_min_max[0] or x_root>x_min_max[-1] or y_root<y_min_max[0] or y_root>y_min_max[-1]:
                    continue
                crit_points.add((round(x_root, 7), round(y_root, 7)))
            except:
                pass
    return crit_points

def main(inputStr, x_min_max, y_min_max, numPoints):
    f = inputStrToSymExpr(inputStr)
    x, y = symbols('x y', real=True)

    def plot_analyze_components(u, v, u_crit, v_crit):
        u_plot_fun = lambdify((x, y), u, 'numpy')
        v_plot_fun = lambdify((x, y), v, 'numpy')

        xin = np.linspace(x_min_max[0], x_min_max[-1], numPoints)
        yin = np.linspace(y_min_max[0], y_min_max[-1], numPoints)
        x_inputs, y_inputs = np.meshgrid(xin, yin)

        # generate outputs for u and v
        u_vals = u_plot_fun(x_inputs, y_inputs)
        v_vals = v_plot_fun(x_inputs, y_inputs)

        # Create a figure and a set of subplots
        fig = plt.figure() # Adjust figure size as needed

        # Add the 3D subplot for u
        ax_u = fig.add_subplot(121, projection='3d') # 1 row, 2 columns, first plot
        ax_u.plot_surface(x_inputs, y_inputs, u_vals, cmap='viridis', alpha=0.8)
        #add critical points
        u_pCrit = []
        x_pCrit = []
        y_pCrit = []
        for (xCrit, yCrit) in u_crit:
            u_pCrit.append(u_plot_fun(float(xCrit), float(yCrit)))
            x_pCrit.append(xCrit)
            y_pCrit.append(yCrit)
        ax_u.scatter(x_pCrit, y_pCrit, u_pCrit, s=60, color='red', label="critial points for u")
        ax_u.legend()

        ax_u.set_title('u(x+yi): real component of f')
        ax_u.set_xlabel('x-axis')
        ax_u.set_ylabel('y-axis')
        ax_u.set_zlabel('u-axis')

        # Add the 3D subplot for v
        ax_v = fig.add_subplot(122, projection='3d') # 1 row, 2 columns, second plot
        ax_v.plot_surface(x_inputs, y_inputs, v_vals, cmap='viridis', alpha=0.8)
        #add critical points
        v_pCrit = []
        x_pCrit = []
        y_pCrit = []
        for (xCrit, yCrit) in v_crit:
            v_pCrit.append(v_plot_fun(float(xCrit), float(yCrit)))
            x_pCrit.append(xCrit)
            y_pCrit.append(yCrit)
        ax_v.scatter(x_pCrit, y_pCrit, v_pCrit, s=60, color='blue', label="critial points for v")
        ax_v.legend()

        ax_v.set_title('v(x+yi): imag component of f')
        ax_v.set_xlabel('x-axis')
        ax_v.set_ylabel('y-axis')
        ax_v.set_zlabel('v-axis')

        # Adjust layout to prevent overlapping titles/labels
        plt.tight_layout()

        # Display the plots
        plt.show()

    #real and complex components of f
    u, v = f.as_real_imag()
    u_x = diff(u, x)
    u_y = diff(u, y)
    v_x = diff(v, x)
    v_y = diff(v, y)

    u_crit = findCritInRange(u_x, u_y, x, y, x_min_max, y_min_max, numPoints)
    v_crit = findCritInRange(v_x, v_y, x, y, x_min_max, y_min_max, numPoints)

    plot_analyze_components(u, v, u_crit, v_crit)

    #TESTING
    #convert to polar coordinates for convienence
    r, theta = symbols('r theta', real=True, nonnegative=True)
    v_x_pol=v_x.subs([(x, r*cos(theta)), (y, r*sin(theta))])
    v_y_pol=v_y.subs([(x, r*cos(theta)), (y, r*sin(theta))])

    #CUSTOM BOUNDS AND CRIT POINTS FOR TESTING PURPOSES
    v_pol_crit = findCritInRange(v_x_pol, v_y_pol, r, theta, [1, 2], [0, 2*pi], 10)
    #sort in ascending order of magnitude (r), than -x, than -y, and negetive both last
    v_pol_crit = list(v_pol_crit)
    v_pol_crit.sort(key=lambda p: (float(p[0]), -float(p[0])*np.cos(float(p[1])), float(p[0])*np.sin(float(p[1]))))
    #convert each point back to cartesian
    sol = []
    for (r_p, theta_p) in v_pol_crit:
        r_p = float(r_p)
        theta_p = float(theta_p)
        sol.append((round(r_p*np.cos(theta_p), 2), round(r_p*np.sin(theta_p), 2)))

    print(sol)

#TESTING
inputStr = "x*i+xy+ye^x+ysin(ix-y)"
if __name__ == "__main__":
    main(inputStr, [-3, 3], [-3, 3], 10)
