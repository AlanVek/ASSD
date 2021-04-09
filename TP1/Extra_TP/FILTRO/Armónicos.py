import numpy as np
import matplotlib.pyplot as plt

nmax = 1500


NPER = 5
fi = 17e3

t = np.linspace(0, NPER / (fi / 2), num = 10000)

a0 = (1 - np.exp(-5))/5
not_0 = lambda n: 10 * (1 + (-1)**n * np.exp(-5)) / (25 + (n * np.pi)**2)
armonicos =  np.vectorize(lambda n: a0 if not n else not_0(n))

y = np.full(t.size, armonicos(0))
y2 = y.copy()

for i in range(1, nmax + 1):
        if i <= 4: y2 += np.real(armonicos(i)) * np.cos(np.pi * t * fi * i)
        y += np.real(armonicos(i)) * np.cos(np.pi * t * fi * i)

fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(t * 1e3, y)
ax2.plot(t * 1e3, y2)
ax1.grid()
ax2.grid()
ax1.set_title('Señal original')
ax2.set_title('Señal recortada en frecuencia')
#ax1.set_xlabel('Tiempo [ms]')
ax2.set_xlabel('Tiempo [ms]')
#fig.subplots_adjust(wspace = .2)
fig.tight_layout()

plt.show()
