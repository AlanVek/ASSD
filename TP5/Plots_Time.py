import matplotlib.pyplot as plt
import pandas as pd

base_path = 'Mediciones FIR'

df = pd.read_csv(base_path + '/Filtro2_HP_3000Hz.csv')

out = df['Channel 2 (V)'].to_numpy()

time_ms = (df['Time (s)'] - df['Time (s)'].min()) * 1e3
plt.plot(time_ms, df['Channel 1 (V)'], label = 'Input')
plt.plot(time_ms, out, label = 'Output')
plt.legend()
plt.grid()
plt.title('Signal Response High Pass 2 - 3 kHz')
plt.ylabel('Amplitude [V]')
plt.xlabel('Time [ms]')
plt.tight_layout()
plt.show()
