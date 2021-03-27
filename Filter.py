import sympy as sp

K = sp.symbols('K', real = True)
Z1, Z2, Z3, Z4, Z5 = sp.symbols('Z1 Z2 Z3 Z4 Z5')

R1, C2, R3, R4, C5 = sp.symbols('R1 C2 R3 R4 C5', real = True)

s = sp.symbols('s')


H_1 = (C2*C5*R1*R3*R4*s**2*(1 - K) + C2*R1*R4*s + C5*s*(-K*R1*R3 - K*R4*(R1 + R3) + R1*R3 + R4*(R1 + R3)) - K*R1 + R1 + R4)/(K*R4)

H = 1 / H_1

wo2 =  (-K*R1 + R1 + R4) / (C2*C5*R1*R3*R4*(1 - K))

one_woq = (C2*R1*R4 + C5*(-K*R1*R3 - K*R4*(R1 + R3) + R1*R3 + R4*(R1 + R3))) / (-K*R1 + R1 + R4)


Q = 1 / (sp.sqrt(wo2) * one_woq)

r1 = 470
c2 = 18e-9
r3 = 470
c5 = 4.7e-9

q = 9.72
wo = 240485.97

eq = Q.subs(R1, r1).subs(C2, c2).subs(C5, c5).subs(R3, r3) - q

eq2 = sp.sqrt(wo2).subs(R1, r1).subs(C2, c2).subs(C5, c5).subs(R3, r3) - wo


print(sp.solve([eq, eq2]))