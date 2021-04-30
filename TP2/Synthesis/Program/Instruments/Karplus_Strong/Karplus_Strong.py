import numpy as np

def Karplus_Strong(freq : float, dur : float, fs : float, S : float, b) -> np.array:
    N = int(np.round(fs/freq - 1/(2 * S), 0))
    samples = np.zeros(int(np.round(fs * dur, 0)))

    samples[ : N] = (2 * np.random.randint(0, 2, N) - 1).astype(float)
    k = np.zeros(N)
    r = np.random.binomial(1, 1 / S, samples.size).astype(bool)

    for i in range(N, N * (1 + samples.size//N), N):
        idx = r[i : i + N]
        k = k[ : idx.size]

        t1 = samples[i - N : i - N + k.size]
        if i == N: t2 = np.concatenate(([samples[i - N - 1]], samples[i - N : i - N - 1 + k.size]))
        else: t2 =  samples[i - N - 1 : i - N - 1 + k.size]

        k[~idx] = t1[~idx]
        k[idx] = (t1 + t2)[idx]/2

        samples[i : i + N] = b * k

    return samples
