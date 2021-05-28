import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Vref = 5.0
bits = 8

data = pd.read_csv('Salida_ADC_entrada_rampa.csv')
data = data.replace('SHI', 1).replace('SLO', 0)

data['dec'] = np.dot(data[data.columns[1:]], 2**np.arange(7, -1, -1))

time_ms = data['TIME'] * 1000
output = data['dec'] * Vref / 2.0**bits

idx = 2
plt.hlines(output[idx:-1], time_ms[idx:-1], time_ms[idx + 1:])
plt.vlines(time_ms[idx + 1:], output[idx:-1], output[idx+1:])
plt.title('ADC output with ramp input')
plt.xlabel('Time [ms]')
plt.ylabel('Output [V]')
plt.grid()
plt.tight_layout()

plt.show()