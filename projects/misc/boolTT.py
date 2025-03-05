import itertools
import sympy as sp

def get_variables(expression):
    """Extracts unique variables from a logical expression."""
    return sorted(expression.free_symbols, key=lambda x: str(x))

def generate_truth_table(expression):
    """Generates and prints the truth table for a given logical expression."""
    variables = get_variables(expression)
    
    print(" | ".join([str(var) for var in variables] + [str(expression)]))
    print("-" * (4 * len(variables) + len(str(expression)) + 3))
    
    for values in itertools.product([0, 1], repeat=len(variables)):
        env = dict(zip(variables, values))
        result = int(bool(expression.subs(env)))
        print(" | ".join(map(str, values)) + " | " + str(result))

"""if __name__ == "__main__":
    expression = sp.sympify("((a&b)|((~b)^c))&(~(~(c^(~d))|~(d&e)))")
    generate_truth_table(expression)
    """

if __name__ == "__main__":
    a, b, c, d, e = sp.symbols("a b c d e")  # Define symbols explicitly
    expression = ((a & b) | (sp.Not(b) ^ c)) & (sp.Not(sp.Not(c ^ sp.Not(d)) | sp.Not(d & e)))
    generate_truth_table(expression)
