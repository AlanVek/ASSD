# y(n) = x(nM)
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

M1, M2 = 2, 3
N = 2**10
# N = 100
t = np.linspace(0, 256, N)
# t = np.arange(30)
# x = np.exp(-np.abs(t))
# x = np.piecewise(t, [np.abs(t) < t.max()/2], [1, 0])
x = square(2 * np.pi * t * 4)
delta_train_M2 = np.zeros(t.size)
delta_train_M2[::M2] = 1

delta_train_M1 = np.zeros(t.size)
delta_train_M1[::M1] = 1


# y1 = x * delta_train_M1
# y2 = x * delta_train_M2

# y1 = x[::M1]
# y2 = x[::M2]

y1 = x * delta_train_M1
y2 = x * delta_train_M2

#
freqs = np.fft.fftshift(np.fft.fftfreq(t.size, t[1] - t[0]))
transf_1 = np.fft.fftshift(np.fft.fft(y1))
transf_2 = np.fft.fftshift(np.fft.fft(y2))
transf_x = np.fft.fftshift(np.fft.fft(x))


freqs = np.append(np.append(freqs - 2 * freqs.max(), freqs), freqs + 2 * freqs.max())
transf_1 = np.append(transf_1, np.append(transf_1, transf_1))
transf_2 = np.append(transf_2, np.append(transf_2, transf_2))
transf_x = np.append(transf_x, np.append(transf_x, transf_x))
# transf_2 = np.fft.fftshift(np.fft.fft(y2))
# transf_x = np.fft.fftshift(np.fft.fft(x))


fig, (ax1, ax2, ax3) = plt.subplots(3)
ax1.plot(freqs, np.abs(transf_x) * 2 * (t[1] - t[0]), label = 'X(f)')
ax2.plot(freqs, np.abs(transf_1) * 2 * (t[1] - t[0]), label = 'Y(f), M = 2', color = 'red')
ax3.plot(freqs, np.abs(transf_2) * 2 * (t[1] - t[0]), label = 'Y(f), M = 3', color = 'green')

ax1.legend()
ax2.legend()
ax3.legend()

ax1.set_ylim([-5, np.abs(transf_x).max() * 1.05 * 2 * (t[1] - t[0])])
ax2.set_ylim([-5, np.abs(transf_x).max() * 1.05 * 2 * (t[1] - t[0])])
ax3.set_ylim([-5, np.abs(transf_x).max() * 1.05 * 2 * (t[1] - t[0])])

ax3.set_xlabel('Frequency [Hz]')
ax1.grid()
ax2.grid()
ax3.grid()
plt.tight_layout()
plt.show()
#

# fig, (ax1, ax2, ax3) = plt.subplots(3)

# ax1.plot(t, x, label = 'x(n)', linestyle = '', marker = 'o')
# ax2.plot(t[::M1]/M1, y1, label = 'y(n), M = 2', linestyle = '', marker = 'o', color = 'red')
# ax3.plot(t[::M2]/M2, y2, label = 'y(n), M = 3', linestyle = '', marker = 'o', color = 'green')
#
# ax1.legend()
# ax2.set_xlim([-1, t.max() + 2])
# ax1.set_xlim([-1, t.max() + 2])
# ax3.set_xlim([-1, t.max() + 2])
# ax2.legend()
# ax3.legend()
#
# ax3.set_xlabel('Time [s]')
# ax1.grid()
# ax2.grid()
# ax3.grid()
# plt.tight_layout()
# plt.show()
#
#


