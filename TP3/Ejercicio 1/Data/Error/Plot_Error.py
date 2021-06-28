import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('Error_cuantizacion_restador.csv')

start = 100
time_ms = df['TIME'].to_numpy()[start:] * 1000
original = df['Diente de sierra'].to_numpy()[start:]
vdac = df['VDAC'].to_numpy()[start:]

desf = 1
plt.plot(time_ms[:-desf], original[:-desf], label = 'Original', linewidth = 2.5)
plt.plot(time_ms[:-desf], vdac[desf:], label = 'Output DAC')
# plt.plot(time_ms[:-desf], (original[:-desf] - vdac[desf:]), label = 'Error')
plt.legend()
plt.xlabel('Time [ms]')
plt.ylabel('Error [mV]')
plt.grid()
plt.title('Error de cuantización')
# plt.ylim(-10e-3, 20e-3)
plt.tight_layout()
plt.show()
