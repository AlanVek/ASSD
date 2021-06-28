import numpy as np
import matplotlib.pyplot as plt
import os

quant = lambda bits: 2**bits - 1

def sigma_delta(x : np.array, bits : int, Vref : [int, float] = 5.0) -> tuple[np.array, np.array]:
    y, acc = np.zeros(x.size), 0
    chunksize = quant(bits)
    if y.size >= chunksize:
        for i in range(x.size):
            acc += x[i] - y[i - 1] * Vref/2
            y[i] = np.sign(acc)
        res = y[ : y.size - y.size%chunksize].reshape(-1, chunksize).mean(axis = 1) * Vref/2
    else: res = y[:1]
    return res, y


if __name__ == '__main__':

    freq = 3
    NPER = 3
    Vref = 5

    fny = 2 * freq
    bits = 4
    L = 2**10

    if not f'{bits}_bits' in os.listdir(os.getcwd()): os.mkdir(f'{bits}_bits')
    if not 'Noise' in os.listdir(os.getcwd() + f'/{bits}_bits'): os.mkdir(f'{bits}_bits/Noise')

    _x = -Vref/2 + Vref * np.random.rand(int(np.round(NPER / freq * 2**(bits + 15) * fny)))

    fs = fny * L
    t = np.linspace(0, NPER / freq, int(np.round(NPER / freq * fs)))
    x = 1 * np.cos(2 * np.pi * t * freq) - np.sqrt(np.abs(np.sin(2 * np.pi * t**2 * freq/4))) #- 2 * np.sin(2 * np.pi * t * 2 * freq)**2

    res, y = sigma_delta(x = x, bits = bits, Vref = Vref)
    idx_slice = slice(None, res.size * quant(bits), quant(bits))

    # Tiempo
    #############################################################################
    fig, (ax1, ax2) = plt.subplots(2)

    ax1.plot(t, y, label = r'$\Sigma \Delta$', linewidth = .5 if bits == 2 else .05, color = 'black')
    ax1.plot(t[idx_slice], res, label = f'Output', linewidth = 3)
    ax1.plot(t, x, label = 'Input')
    ax1.legend(loc = 'lower right')
    ax1.grid()

    ax2.plot(t, x - y, label = 'Error 1 bit')
    ax2.plot(t[idx_slice], x[idx_slice] - res, label = f'Error {bits} bits')
    ax2.grid()
    ax2.legend(loc = 'lower right')

    ax1.set_title('L = ' + r'$2^{' + str(int(np.round(np.log2(L)))) + r'}$' + f' -- {bits} bits')
    fig.tight_layout()
    # fig.savefig(f'{bits}_bits/sigma_delta__L=2^{l}___{bits}_bits.png')
    # plt.close(fig)

    # Frecuencia
    #############################################################################
    fig, ax = plt.subplots()
    errsd = (x - y * Vref/2)
    err1b = (x - np.piecewise(x, [x >= 0], [Vref/2, -Vref/2]))
    f = np.fft.fftshift(np.fft.fftfreq(t.size, t[1] - t[0]))
    transf1 = np.fft.fftshift(np.fft.fft(errsd)) * (t[1] - t[0])
    transf2 = np.fft.fftshift(np.fft.fft(err1b))  * (t[1] - t[0])
    # ax.plot(f, 10 * np.log10(np.abs(transf2)**2 / 100), label=f'Noise')
    # ax.plot(f, 10 * np.log10(np.abs(transf1)**2 / 100), label = r'$\Sigma \Delta$ Noise')
    ax.plot(f, 20 * np.log10(np.abs(transf1/transf2)), label = 'Noise transfer function')
    ax.grid()
    ax.legend()
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Quantization noise [dB]')
    ax.set_title('Noise Shaping -- L = ' + r'$2^{' + str(int(np.round(np.log2(L)))) + r'}$' + f' -- {bits} bits')
    ax.set_xscale('log')
    fig.tight_layout()


    plt.show()
    # fig.savefig(f'{bits}_bits/Noise/sigma_delta_Noise__L=2^{l}___{bits}_bits.png')
    # plt.close(fig)