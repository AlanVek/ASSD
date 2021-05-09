import numpy as np
import matplotlib.pyplot as plt

zeros = np.array([0 + 0j, -1 + 0j])
L = 10
fs = 100
rl = 1

denom = np.zeros(L + 2)
denom[[0, -2, -1]] = [2/rl, -1, -1]
poles = np.roots(denom)

t = np.linspace(-1, 1, 1000)

fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(t, np.sqrt(1 - t**2), color = 'blue', linewidth = .5)
ax1.plot(t, -np.sqrt(1 - t**2), color = 'blue', linewidth = .5)
ax1.scatter(poles.real, poles.imag, color = 'red', marker = 'x', label = 'Poles')
ax1.scatter(zeros.real, zeros.imag, color = 'green', marker = 'o', label = 'Zeros')

newpoles, newzeros = np.log(poles) / (2 * np.pi) * fs, np.log(zeros[zeros != 0]) / (2 * np.pi) * fs
ax2.scatter(newpoles.real, newpoles.imag, color = 'red', marker = 'x', label = 'Poles')
ax2.scatter(newzeros.real, newzeros.imag, color = 'green', marker = 'o', label = 'Zeros')


ax1.set_ylabel('Z', rotation = 0)
ax2.set_ylabel('S', rotation = 0)

ax1.set_ylim([-1.5, 1.5])
ax1.set_xlim([-1.5, 1.5])

ax1.legend(loc = 'upper right')
ax2.legend()

fig.suptitle(fr'Zeros and poles for $f_s$ = {fs}, L = {L} and $R_L$ = {rl}')
ax1.grid()
ax2.grid()
fig.tight_layout()
plt.show()