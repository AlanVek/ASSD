import numpy as np
from scipy.signal import lfilter

def Karplus_Strong_Z(freq: float, dur: float, fs: float, S: float, R) -> np.array:
    N = int(np.round(fs / freq - 1 / (2 * S), 0))

    x = np.zeros(int(np.round(fs * dur, 0)))
    try: x[: N] = (2 * np.random.randint(0, 2, N) - 1).astype(float)
    except ValueError: return x

    factor = 2 * R - 1
    b_filt = [factor, factor]
    a_filt = np.zeros(N + 2)
    a_filt[[0, -2, -1]] = [2, -factor * (2 - 1/S), -factor/S]

    return lfilter(b_filt, a_filt, x)

def Karplus_Strong(freq : float, dur : float, fs : float, S : float, R) -> np.array:
    N = int(np.round(fs/freq - 1/(2 * S), 0))
    samples = np.zeros(int(np.round(fs * dur, 0)))

    try: samples[ : N] = (2 * np.random.randint(0, 2, N) - 1).astype(float)
    except ValueError: return samples

    for i in range(N, N * (1 + samples.size//N), N):
        size = min(N, samples.size - i)

        t1 = samples[i - N : i - N + size]
        if i == N: t2 = np.concatenate(([samples[i - N - 1]], samples[i - N : i - N - 1 + size]))
        else: t2 =  samples[i - N - 1 : i - N - 1 + size]

        samples[i : i + N] = R * (t1 * (2 - 1/S) + t2 / S) / 2

    return samples