import numpy as np
from Karplus_Strong import Karplus_Strong
import matplotlib.pyplot as plt

L = 500
fs = 8000
rl = 1
dur = 5
distrib = 'unif'
Rin = 50

t = np.linspace(0, dur, fs * dur)

y = Karplus_Strong(dur = dur, N = L, fs = fs, rl = rl, noise_distrib = distrib)

freqs = np.fft.fftfreq(t.size, 1/fs)
transf = np.fft.fft(y)

fout = np.round(fs/(L + .5), 3)
label = r'$f_{out}$' + f' = {fout}'

fig, (ax1, ax2, ax3) = plt.subplots(3)

ax1.plot(t, y, label = label)
ax2.plot(freqs / 1e3, 10 * np.log10(np.abs(transf)**2 / 1e-3 / Rin), label = label)
ax3.specgram(y, Fs = fs)

ax1.set_xlabel('Time [s]')
ax2.set_xlabel('Frequency [kHz]')
ax3.set_xlabel('Time[s]')

ax1.set_ylabel('Output [V]')
ax2.set_ylabel('Output [dBm]')
ax3.set_ylabel('Frequency [kHz]')

ax1.legend()
ax2.legend()

fig.suptitle(fr'Output for $f_s$ = {fs}, L = {L} and $R_L$ = {rl}')
ax1.grid()
ax2.grid()

ax3.set_yticklabels(['0', '1', '2'])

fig.tight_layout()
plt.show()