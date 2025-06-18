import math

def solve_skin_friction_drag():
    """
    Calculates the total skin friction drag on a flat plate with a
    laminar-to-turbulent boundary layer transition.

    This script follows the methodology outlined in the prompt:
    1.  Calculates Reynolds numbers to determine flow regimes.
    2.  Uses the standard correction formula for mixed boundary layer flow,
        which accounts for both the laminar and turbulent sections.
    3.  Calculates the final drag force based on the average drag coefficient.
    """
    # --- Given Information from the Prompt ---
    L = 2.5          # Plate Length (m)
    w = 0.75         # Plate Width (m)
    U_infinity = 40.0  # Freestream Velocity (m/s)
    rho = 1.225      # Fluid Density (kg/m^3)
    mu = 1.81e-5     # Fluid Dynamic Viscosity (Pa·s)
    Re_crit = 5e5    # Critical Reynolds Number for transition

    print("--- Input Parameters ---")
    print(f"Plate Length (L): {L} m")
    print(f"Plate Width (w): {w} m")
    print(f"Freestream Velocity (U_infinity): {U_infinity} m/s")
    print(f"Fluid Density (rho): {rho} kg/m^3")
    print(f"Fluid Dynamic Viscosity (mu): {mu} Pa·s")
    print(f"Critical Reynolds Number (Re_crit): {Re_crit:.0e}\n")

    # --- Step-by-Step Solution ---
    print("--- Calculation Steps ---")

    # Step 1: Calculate the planform area of one side of the plate.
    A = L * w
    print(f"1. Plate Area (A): {A:.4f} m^2")

    # Step 2: Calculate the Reynolds number at the end of the plate (x = L)
    # This determines the overall state of the boundary layer.
    Re_L = (rho * U_infinity * L) / mu
    print(f"2. Reynolds Number at plate end (Re_L): {Re_L:,.2f} ({Re_L:.3e})")

    # Check if the flow is fully laminar or mixed.
    if Re_L <= Re_crit:
        print("\nFlow is fully laminar across the entire plate.")
        # Use the average skin friction formula for fully laminar flow
        C_D_total = 1.328 / (Re_L**0.5)
    else:
        print("\nFlow is mixed (laminar-turbulent). Applying correction method.")

        # Step 3: Determine the location (x_crit) where transition occurs.
        # This is an important intermediate value.
        x_crit = (Re_crit * mu) / (rho * U_infinity)
        print(f"3. Transition location (x_crit): {x_crit:.4f} m from the leading edge.")

        # Step 4: Calculate the total average drag coefficient (C_D_total).
        # This is the core reasoning challenge. We use the formula that subtracts
        # the "hypothetical" turbulent portion from the start of the plate
        # and adds back the actual laminar portion.
        # The standard formula is: C_D = (0.074 / Re_L**0.2) - (Correction_Constant / Re_L)
        
        # Calculate the correction constant 'A' based on Re_crit
        # A = Re_crit * (C_f_turb(Re_crit) - C_f_lam(Re_crit))
        correction_constant = Re_crit * ((0.074 / (Re_crit**0.2)) - (1.328 / (Re_crit**0.5)))
        print(f"4. Correction constant (A): {correction_constant:.2f}")

        # Apply the full formula for the average drag coefficient for mixed flow
        C_D_total = (0.074 / (Re_L**0.2)) - (correction_constant / Re_L)
        print(f"5. Total Average Drag Coefficient (C_D_total): {C_D_total:.6f}")

    # Step 5: Calculate the final total skin friction drag force (D_f).
    # D_f = C_f * A * (1/2) * rho * U_infinity^2
    D_f = C_D_total * A * 0.5 * rho * (U_infinity**2)
    print(f"6. Total Skin Friction Drag (D_f): {D_f:.4f} N")


    # --- Final Answer in Requested JSON Format ---
    print("\n" + "="*40)
    print("Final Answer in JSON Format:")
    
    final_answer_json = {
        "total_skin_friction_drag_N": round(D_f, 3)
    }

    # Pretty print the JSON object
    print("{")
    for key, value in final_answer_json.items():
        print(f'  "{key}": {value}')
    print("}")
    print("="*40)
    
    return final_answer_json

if __name__ == "__main__":
    solve_skin_friction_drag()