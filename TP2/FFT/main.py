import matplotlib.pyplot as plt
from FFT import fft, ifft, fftfreq
import numpy as np


if __name__ == '__main__':

    t = np.linspace(-5, 5, 2**10)

    y = np.sin(75 * t) / (75 * t)
    freqs = fftfreq(t.size, t[1] - t[0])
    transf = fft(y)
    antitransf = np.real(ifft(transf))

    fig, (ax1, ax2) = plt.subplots(2)

    ax1.plot(t, y, label = 'Original', linewidth = 3)
    ax1.plot(t, antitransf, label = 'Reconstructed')
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Time [s]')

    ax2.plot(freqs, np.abs(transf), label = 'FFT')
    ax2.grid()
    ax2.set_xlabel('Frequency [Hz]')
    ax2.legend()

    fig.tight_layout()

    plt.show()


