import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


base_path = 'Mediciones FIR'

df = pd.read_csv(base_path + '/Filtro2_BP_IIR_RtaFrec.csv')

fig, ax1 = plt.subplots()
freq = df['Frequency (Hz)']

phase = df['Channel 2 Phase (deg)'].to_numpy()
phase[np.abs(phase - 180) <= 180] -= 360
ax1.semilogx(freq, df['Channel 2 Magnitude (dB)'], label = 'Output')
# ax2.semilogx(freq, phase, label = 'Output')
ax1.legend();# ax2.legend()
ax1.grid(); #ax2.grid()
ax1.set_title('Frequency Response - Band Pass IIR 2')
ax1.set_ylabel('Magnitude [dB]');# ax2.set_ylabel('Phase [deg]')
#ax2.set_xlabel('Frequency [Hz]')
ax1.set_xlabel('Frequency [Hz]')
plt.tight_layout()
plt.show()
