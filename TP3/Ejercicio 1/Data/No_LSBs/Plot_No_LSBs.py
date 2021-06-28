import pandas as pd
import matplotlib.pyplot as plt

bits = 3

data_org = pd.read_csv('Original.csv')
org = data_org['Diente de sierra'].to_numpy()
time_org = data_org['TIME'].to_numpy() * 1000
df = pd.read_csv(f'VDAC_{bits}_bits.csv')

time_ms = df['TIME'].to_numpy() * 1000
vdac = df['VDAC'].to_numpy()

fig, ax = plt.subplots()
ax.plot(time_org, org, label = 'Original')
ax.plot(time_ms, vdac, label = f'Output - {bits} bits')
ax.legend()
ax.grid()
ax.set_xlabel('Time [ms]')
ax.set_ylabel('Output [V]')
ax.set_title(f'Output DAC -- {bits} MSB')
fig.tight_layout()

# plt.show()

fig.savefig(f'No_LSBs_{bits}.png')