import numpy as np
import matplotlib.pyplot as plt

t = np.arange(-1500, 1500, .5)

# x = np.piecewise(t, [t != 0], [lambda t : np.sin(t / 5) / t * 5, 1])
x = np.zeros(t.size)
x[t != 0] = np.sin(t[t != 0]) / t[t != 0]
x[t == 0] = 1


M = 2
M2 = 3

y1 = x[::M]
y2 = x[::M2]

transf_x = np.fft.fft(x)
transf_y1 = np.fft.fftshift(np.fft.fft(y1))
transf_y2 = np.fft.fftshift(np.fft.fft(y2))

f = np.fft.fftfreq(t.size, t[1] - t[0])
f1 = np.fft.fftshift(np.fft.fftfreq(t[::M].size, t[1] - t[0]))
f2 = np.fft.fftshift(np.fft.fftfreq(t[::M2].size, t[1] - t[0]))

# plt.plot(t, x)
# plt.plot(t[::M], y1)
plt.plot(np.append(f - 2 * f.max(), np.append(f, f - 2 * f.min())), np.tile(np.abs(transf_x), 3), label = 'Input')
plt.plot(np.append(f1 - 2 * f1.max(), np.append(f1, f1 - 2 * f1.min())), np.tile(np.abs(transf_y1), 3), label = 'M = 2')
plt.plot(np.append(f2 - 2 * f2.max(), np.append(f2, f2 - 2 * f2.min())), np.tile(np.abs(transf_y2), 3), label = 'M = 3')
plt.legend()
plt.show()

