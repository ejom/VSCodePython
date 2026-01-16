import timeit
import numpy as np
import sympy as sp
import math
import pandas as pd
import matplotlib.pyplot as plt

# --- Functions to be tested ---

def mclar_2_sin(x):
    """2nd Order Maclaurin series approximation for sin(x)"""
    return x - (x**3) / 6

def small_ang_sin(x):
    """Small-angle approximation for sin(x)"""
    return x

# --- Analysis Function ---

def analyze_sin_functions(x_values):
    """
    Analyzes the speed and accuracy of various sin implementations.
    """
    results = []
    
    # A dictionary mapping function names to lambda functions for timing
    functions_to_test = {
        "math.sin": lambda x: math.sin(x),
        "numpy.sin": lambda x: np.sin(x),
        "sympy.sin": lambda x: sp.sin(x).evalf(), # .evalf() to get a float
        "Maclaurin Approx": mclar_2_sin,
        "Small Angle Approx": small_ang_sin,
    }

    for x in x_values:
        # Use math.sin(x) as the true value for accuracy comparison
        true_value = math.sin(x)
        
        row = {'x': x, 'True Value': true_value}

        for name, func in functions_to_test.items():
            # --- Performance Test ---
            # timeit needs a zero-argument function, so we use a lambda
            time = timeit.timeit(lambda: func(x), number=10000)
            
            # --- Accuracy Test ---
            approx_value = func(x)
            error = abs(true_value - approx_value)
            
            # Column names are updated for easier selection during plotting
            row[f'{name} Time'] = time * 1e6 # convert to microseconds
            row[f'{name} Error'] = error
            
        results.append(row)
        
    return pd.DataFrame(results)

# --- Plotting Function ---

def plot_results(df):
    """
    Plots the error and performance results from the analysis DataFrame.
    """
    # Create a figure with two subplots, one for error and one for time
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
    fig.suptitle('Sine Function Analysis', fontsize=16)

    # --- Plot 1: Approximation Error ---
    ax1.plot(df['x'], df['Maclaurin Approx Error'], 'r-o', label='Maclaurin Approx Error')
    ax1.plot(df['x'], df['Small Angle Approx Error'], 'b-^', label='Small Angle Approx Error')
    ax1.set_title('Approximation Error vs. x')
    ax1.set_xlabel('x (radians)')
    ax1.set_ylabel('Absolute Error')
    ax1.legend()
    ax1.grid(True)

    # --- Plot 2: Execution Time ---
    for name in ["math.sin", "numpy.sin", "sympy.sin", "Maclaurin Approx", "Small Angle Approx"]:
        ax2.plot(df['x'], df[f'{name} Time'], '-o', label=f'{name} Time')
    
    ax2.set_title('Execution Time vs. x')
    ax2.set_xlabel('x (radians)')
    ax2.set_ylabel('Time (μs)')
    ax2.set_yscale('log') # Use a log scale as sympy is much slower
    ax2.legend()
    ax2.grid(True, which="both", ls="--")
    
    # Adjust layout and display the plots
    plt.tight_layout(rect=[0, 0, 1, 0.96]) # Adjust for suptitle
    plt.show()


# --- Execution ---

if __name__ == "__main__":
    # Define the range of x values to test (from 0 to π/2)
    # Increased the number of points for a smoother plot
    x_values_to_test = np.linspace(0, np.pi/2, 20)

    # Run the analysis
    analysis_df = analyze_sin_functions(x_values_to_test)
    analysis_df.to_csv('analysis.csv', index=False)
    
    # Set display options for cleaner output
    pd.set_option('display.float_format', '{:.6f}'.format)
    pd.set_option('display.width', 120)
    
    print("--- Performance and Accuracy Analysis of Sine Functions ---")
    print(analysis_df)
    
    # --- Generate and show the plots ---
    plot_results(analysis_df)