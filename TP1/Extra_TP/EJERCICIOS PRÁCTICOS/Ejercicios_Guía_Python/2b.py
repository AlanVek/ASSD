import matplotlib.pyplot as plt
from Causal import Causal
import numpy as np

N = 50
x = lambda n: 1 if not n else 0

xAxis = np.arange(N)

A = Causal([0]) * N

for i in range(N):
    A[i] = x(i) + A[i - 1] - 0.5 * A[i - 2]


y = [A[i] + A[i - 1] for i in xAxis]

A_closed = 2.0**((1 - xAxis)/2) * np.cos((xAxis - 1) * np.pi / 4)

y_closed = 2 ** ((1 - xAxis) / 2) * (np.cos((xAxis - 1) * np.pi / 4) + np.sqrt(2) * np.sin(xAxis * np.pi / 4))

plt.plot(A, label = 'A(n)')
plt.plot(y, label = 'y(n)')
plt.plot(A_closed, label = 'A(n) closed')
plt.plot(y_closed, label = 'y(n) closed')
plt.xlabel('n')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
