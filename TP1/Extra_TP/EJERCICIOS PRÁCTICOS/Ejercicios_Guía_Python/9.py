from Causal import Causal
import matplotlib.pyplot as plt
from cmath import sqrt
import numpy as np

x = lambda n: 1 if not n else 0
N = 80

alpha = 1
beta = -1/2

xAxis = np.arange(N)
A = Causal([0]) * N


for i in range(N):
    A[i] = x(i - 2) * 0.5 + A[i - 1] * alpha + A[i - 2] * beta

r1 = (alpha + sqrt(alpha**2 + 4 * beta)) / 2
# r2 = (alpha - sqrt(alpha**2 + 4 * beta)) / 2
r2 = alpha - r1

c1, c2 = np.linalg.solve([[1, 1], [r1, r2]], [0, 1/2])
A_closed = np.real(np.concatenate(([0], c1 * r1**xAxis + c2 * r2**xAxis)))

plt.title(rf'$\alpha$ = {alpha}; $\beta$ = {beta}')
plt.plot(A, label = 'y(n)')
plt.plot(A_closed, label = 'y(n) closed')
plt.xlabel('n')
plt.legend()
plt.grid()
plt.tight_layout()

plt.show()