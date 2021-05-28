import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

quant = lambda bits: 2**bits - 1

def sigma_delta(x : np.array, bits : int, Vref : [int, float] = 5.0) -> tuple[np.array, np.array]:

    y, acc = np.zeros(x.size), 0
    chunksize = quant(bits)

    if y.size >= chunksize:
        for i in range(x.size):
            acc += x[i] - y[i - 1]
            y[i] = Vref/2 * np.sign(acc) if acc else Vref/2

        res = y[ : y.size - y.size%chunksize].reshape(-1, chunksize).mean(axis = 1)

    else: res = y[:1]

    return res, y


if __name__ == '__main__':

    freq = 10
    NPER = 3
    Vref = 10


    fny = 2 * freq
    for bits in range(2, 9):

        print(f'Bits: {bits}')

        if not f'{bits}_bits' in os.listdir(os.getcwd()): os.mkdir(f'{bits}_bits')

        for l in range(bits + 2, bits + 11, 2):

            L = 2**l
            fs = fny * L
            t = np.linspace(0, NPER / freq, int(np.round(NPER / freq * fs)))
            x = 5 * np.cos(2 * np.pi * t * freq) #- 2 * np.sin(2 * np.pi * t * 2 * freq)**2

            res, y = sigma_delta(x = x, bits = bits, Vref = Vref)
            idx_slice = slice(None, res.size * quant(bits), quant(bits))

            fig, (ax1, ax2) = plt.subplots(2)

            ax1.plot(t, y, label = r'$\Sigma \Delta$', linewidth = .1 if bits == 2 else .05, color = 'black')
            ax1.plot(t[idx_slice], res, label = f'Output', linewidth = 3)
            ax1.plot(t, x, label = 'Input')
            ax1.legend(loc = 'lower right')
            ax1.grid()

            ax2.plot(t, x - y, label = 'Error 1 bit')
            ax2.plot(t[idx_slice], x[idx_slice] - res, label = f'Error {bits} bits')
            ax2.grid()
            ax2.legend(loc = 'lower right')

            ax1.set_title('L = ' + r'$2^{' + str(l) + r'}$' + f' -- {bits} bits')

            fig.tight_layout()
            fig.savefig(f'{bits}_bits/sigma_delta__L=2^{l}___{bits}_bits.png')
            plt.close(fig)
            # plt.show()
