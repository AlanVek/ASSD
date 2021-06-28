import matplotlib.pyplot as plt
from Generate_Table import gen_data

real, dfs_dac, dfs_adc = gen_data()
fig, (ax1, ax2) = plt.subplots(2)

for i, df in enumerate(dfs_dac):
    label = None if i < len(dfs_dac) - 1 else 'DAC output'
    label2 = None if i < len(dfs_dac) - 1 else 'Error'
    ax1.plot(real[i], df['VDAC'][200], linewidth = 0, marker = 'o', color = 'red', label = label)
    ax2.plot(real[i], 1000 * (real[i] - df['VDAC'][200]), linewidth = 0, marker = 'o', color = 'green', label = label2)


ax1.grid(); ax2.grid()
ax1.legend(); ax2.legend()
ax1.set_ylabel('Output [V]')
ax2.set_ylabel('Error [mV]')
ax2.set_xlabel('Input [V]')
ax1.set_title('Quantization error - Full scale 12 steps')
fig.tight_layout()
plt.show()


