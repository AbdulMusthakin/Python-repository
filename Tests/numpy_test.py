import sympy as sym

x = sym.symbols('x')
p = (x**2 + 8*x + 16)
q = sym.solve(p)
print(q)
