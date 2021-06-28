import numpy as np

def bits_modulation(signal : np.array, bits : int = 8, Vref : [int, float] = 5.0) -> np.array:
    res = np.zeros((signal.size, bits))
    value = Vref
    signal_temp = signal.copy() + 2.5
    for bit in range(bits):
        value /= 2
        idx = signal_temp >=  value
        signal_temp[idx] -= value
        res[:, bit] = idx.astype(int) * Vref
    return res

def bits_demodulation(binary : np.array, bits : int = 8) -> np.array:
    return binary.dot(2.0**np.arange(-1, -1 - bits, -1).reshape(-1, 1)) - 2.5


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from Useful.File import save_file
    import pandas as pd

    Vref = 5
    fs = 500
    tmin, tmax = 0, 1
    bits = 8
    save = True


    tsize = (tmax - tmin) * fs + 1
    # f = lambda x: np.exp(-2.5*(x%2)**.8 * ss.square(2 * np.pi * 25*(x%2), .5)) - 3 * np.sin(2 * np.pi * 25*(x%2) * 2)**2
    f = lambda x: 2.5 * np.sin(2 * np.pi * 100 * x)

    t = np.linspace(tmin, tmax, tsize)

    y = f(t)

    # Clamping y escalamiento
    if y.max() - y.min() > Vref: y *= Vref / (y.max() - y.min())
    if y.min() < -Vref / 2: y -= (y.min() + Vref/2)
    if y.max() > Vref / 2: y += (Vref/2 - y.max())

    y_mod = bits_modulation(y, Vref = Vref, bits = bits)
    y_demod = bits_demodulation(y_mod, bits = bits)

    if save:
        filename = save_file()
        basename, ext = filename.split('.')
        ext = '.' + ext
        for bit in range(bits):
            pd.DataFrame(np.vstack((t, y_mod[:, bit])).T).to_csv(basename + f'_bit{bit+1}_' + ext , index = False, header = False)
    #
        pd.DataFrame(np.vstack((t, y)).T).to_csv(basename + '_in' + ext, index = False, header=False)
    else:
        plt.plot(t, y, label = 'Original')
        plt.plot(t, y_demod, label = 'Reconstructed')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()