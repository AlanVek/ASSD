import numpy as np

def pwm_modulation(signal : np.array, bits : int = 8, Vref : [int, float] = 5.0) -> np.array:
    precision = 2**bits - 1
    res = np.zeros(precision * signal.size)

    clamped = signal + Vref/2
    for i in range(signal.size):
        duty = clamped[i] / Vref
        res[i * precision : int(np.round((i + duty) * precision))] = Vref
    return res

def pwm_demodulation(pwm : np.array, bits : int = 8, Vref : [int, float] = 5.0) -> np.array:
    return pwm.reshape(-1, 2**bits - 1).mean(axis = 1) * Vref


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from Useful.File import save_file
    import pandas as pd
    import scipy.signal as ss

    Vref = 3.3
    fs = 500
    tmin, tmax = 0, 5
    bits = 8


    tsize = (tmax - tmin) * fs + 1
    f = lambda x: np.exp(-2.5*(x%2)**.8 * ss.square(2 * np.pi * 2.5*(x%2), .5)) - 3 * np.sin(2 * np.pi * 2.5*(x%2) * 2)**2


    t = np.linspace(tmin, tmax, tsize)

    y = f(t)

    # Clamping
    if y.max() - y.min() > Vref: y *= Vref / (y.max() - y.min())
    if y.min() < -Vref / 2: y -= (y.min() + Vref/2)
    if y.max() > Vref / 2: y += (Vref/2 - y.max())

    y_mod = pwm_modulation(y, Vref = Vref)

    filename = save_file()
    tmod = np.linspace(t.min(), t.max(), y_mod.size)
    pd.DataFrame(np.vstack((tmod, y_mod)).T).to_csv(filename, index = False)
    pd.DataFrame(np.vstack((t, y)).T).to_csv(filename[:-4] + '_in' + filename[-4:], index = False)
    #plt.plot(t, y)
    #plt.show()