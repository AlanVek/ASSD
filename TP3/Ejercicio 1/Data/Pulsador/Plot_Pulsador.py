import pandas as pd
import matplotlib.pyplot as plt

bits = 7

df_eoc = pd.read_csv(f'Salida_DAC_con_EOC_como_muestreo.csv')
df_4k = pd.read_csv(f'Salida_DAC_con_oscilador_excterno_4kHz.csv')
df_7_5k = pd.read_csv(f'Salida_DAC_con_oscilador_excterno_75kHz.csv')

vdac_eoc = df_eoc['VDAC'].to_numpy()
vdac_4k = df_4k['VDAC'].to_numpy()
vdac_7_5k = df_7_5k['VDAC'].to_numpy()

time_ms_eoc = df_eoc['TIME'].to_numpy() * 1000
time_ms_4k = df_4k['TIME'].to_numpy() * 1000 + time_ms_eoc[-1]
time_ms_7_5k = df_7_5k['TIME'].to_numpy() * 1000 + time_ms_4k[-1]

plt.plot(time_ms_eoc, vdac_eoc, label = 'EOC')
plt.plot(time_ms_4k, vdac_4k, label = f'4kHz')
plt.plot(time_ms_7_5k, vdac_7_5k, label = f'7.5kHz')
plt.legend(loc = 'upper right')
plt.grid()
plt.xlabel('Time [ms]')
plt.ylabel('Output [V]')
plt.title(f'Output with different clocks')
plt.tight_layout()

plt.show()

