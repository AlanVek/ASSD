import numpy as np
import matplotlib.pyplot as plt
import ltspice
data = ltspice.Ltspice('C:/Users/alanv/OneDrive/Documentos/Downloads/Osclidor_2 (1).raw')
data.parse()

fig, ax = plt.subplots()
for i in range(data.getCaseNumber() - 1):
    if not i%2 or i == 1:
        t = data.get_time()
        y = data.get_data('V(Square)')

        y = y[t < 60e-6]
        t = t[t < 60e-6]
        if i <= 1: ax.plot(t * 1e6, y - 17 * i, label = rf'$R_4$ = {100}$\Omega$')
        else: ax.plot(t * 1e6, y - 17 * (i//2 + 1), label = rf'$R_4$ = {i}k$\Omega$')

ax.set_title(r'Duty Cycle del 50%')
ax.grid()
ax.set_yticklabels([])
ax.set_xlabel(r'Time [$\mu$s]')
ax.legend()
fig.tight_layout()
plt.show()