import math

# --- Constants ---
Yf0 = 0.249603
FA_st = 0.066033
H_total = 5.0  # m

# Derived constants for the functions
C_Y = 1.0 - Yf0  # Approx 0.750397
log_C_Y = math.log(C_Y)  # Approx -0.287158

# --- Phi function and its derivative ---
def phi_func(x):
    """Calculates phi at height x."""
    if x < 0 or x > H_total: # Physical bounds
        # For x slightly outside due to numerical method, allow calculation
        # but very large/small x could cause math errors.
        # However, Newton method should converge within bounds if initial guess is reasonable.
        pass
    
    # Handle edge case x=H to avoid potential 0/0 if not careful, though formula handles it.
    if abs(x - H_total) < 1e-9: # x is very close to H
         return 0.0
    
    exponent = -(1.0 - x / H_total)
    try:
        term_base_pow_exp = C_Y ** exponent
    except ValueError: # math domain error if C_Y is negative (not here) or base is zero with neg exponent
        # This shouldn't happen with C_Y being ~0.75
        print(f"Math error for C_Y ** exponent with C_Y={C_Y}, exponent={exponent}")
        return float('nan')
        
    phi = (term_base_pow_exp - 1.0) / FA_st
    return phi

def phi_prime_func(x):
    """Calculates d(phi)/dx at height x."""
    if abs(x - H_total) < 1e-9: # At x=H, Yf=0, phi=0. Derivative might be tricky.
                                # Let's evaluate it normally.
                                # (C_Y)^0 * log_C_Y / (FA_st * H) = log_C_Y / (FA_st*H)
        exponent = 0.0
    else:
        exponent = -(1.0 - x / H_total)

    try:
        term_base_pow_exp = C_Y ** exponent
    except ValueError:
        print(f"Math error for C_Y ** exponent in derivative with C_Y={C_Y}, exponent={exponent}")
        return float('nan')

    phi_prime = (1.0 / FA_st) * term_base_pow_exp * log_C_Y * (1.0 / H_total)
    return phi_prime

# --- Newton's Method Implementation ---
def newton_method(phi_target, initial_guess_x, iterations=15):
    x_current = initial_guess_x
    #print(f"\nSolving for phi_target = {phi_target} with initial guess x = {initial_guess_x}")
    for i in range(iterations):
        phi_val = phi_func(x_current)
        f_val = phi_val - phi_target
        
        phi_prime_val = phi_prime_func(x_current)
        if abs(phi_prime_val) < 1e-12: # Avoid division by zero
            #print(f"Iteration {i+1}: Derivative too small. Stopping.")
            break
            
        x_next = x_current - f_val / phi_prime_val
        #print(f"Iteration {i+1}: x = {x_next:.8f}, f(x) = {f_val:.8f}, phi(x) = {phi_val:.8f}")
        
        # Simple convergence check (optional, as 15 iterations are fixed)
        if abs(x_next - x_current) < 1e-7:
            #print("Converged.")
            #pass # continue for fixed iterations
            x_current = x_next
            break

        x_current = x_next
        # Safety break if x goes out of physical bounds [0, H] significantly
        if not (-0.1 < x_current < H_total + 0.1) :
             print(f"Iteration {i+1}: x = {x_current:.4f} is out of bounds [0, {H_total}]. Stopping.")
             break

    return x_current

# --- Calculations ---
# Initial guess for both cases
x0 = 0.0 # m

# Calculate x_low (height for phi = 0.5)
phi_target_low = 0.5
x_for_phi_0_5 = newton_method(phi_target_low, x0)

# Calculate x_high (height for phi = 3.5)
phi_target_high = 3.5
x_for_phi_3_5 = newton_method(phi_target_high, x0)

# Round solutions to two decimal places
x_low_rounded = round(x_for_phi_0_5, 2)
x_high_rounded = round(x_for_phi_3_5, 2)

# --- Output JSON ---
# Per problem: "x_low corresponds to phi=0.5", "x_high corresponds to phi=3.5"
# This means the JSON field named "x_low" stores the height for phi=0.5.
# And "x_high" stores the height for phi=3.5.
# Since phi decreases with x, x_for_phi_3.5 will be smaller than x_for_phi_0.5.
# So json_output["x_high"] will be a smaller number than json_output["x_low"].
# The flammable region is [json_output["x_high"], json_output["x_low"]].
json_output = {
    "x_low": x_low_rounded,
    "x_high": x_high_rounded 
}

# --- Print intermediate values for verification (optional) ---
#print(f"\n--- Constants ---")
#print(f"Yf0 = {Yf0:.6f}")
#print(f"(F/A)_st = {FA_st:.6f}")
#print(f"H = {H_total:.1f} m")
#print(f"C_Y (1-Yf0) = {C_Y:.6f}")
#print(f"ln(C_Y) = {log_C_Y:.6f}")
#
#print(f"\n--- Function values at x=0 ---")
#print(f"phi(0) = {phi_func(0.0):.4f}") # Expected: 5.0373
#print(f"phi_prime(0) = {phi_prime_func(0.0):.4f}") # Expected: -1.1590
#
#print(f"\n--- Results ---")
#print(f"Calculated x for phi = {phi_target_low}: {x_for_phi_0_5:.8f} m")
#print(f"Calculated x for phi = {phi_target_high}: {x_for_phi_3_5:.8f} m")
#
#print(f"\nRounded x_low (for phi={phi_target_low}): {x_low_rounded:.2f} m")
#print(f"Rounded x_high (for phi={phi_target_high}): {x_high_rounded:.2f} m")
#
import json
print("\nJSON Output:")
print(json.dumps(json_output, indent=4))