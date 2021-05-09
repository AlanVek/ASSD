import numpy as np
import matplotlib.pyplot as plt

L = 50
fs = 100
rl = .1

H = lambda z: z**L * (z + 1) / (2/rl * z**(L + 1) - z - 1)

w = np.linspace(-3 * np.pi, 3 * np.pi, 100000)

y = 20 * np.log10(np.abs(H(np.exp(1j * w))))

fout = np.round(fs/(L + .5), 3)
label = r'$f_{out}$' + f' = {fout}'

plt.plot(w / (2 * np.pi) * fs, y, label = label)
plt.xlabel('Frequency [Hz]')
plt.ylabel(r'$|H(e^{\frac{j\omega}{f_s}})|$')
plt.legend()
plt.title(fr'Transfer function for $f_s$ = {fs}, L = {L} and $R_L$ = {rl}')
plt.grid()
plt.tight_layout()
plt.show()