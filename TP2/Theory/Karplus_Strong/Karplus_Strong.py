import numpy as np

def Karplus_Strong(dur : float, N : int, fs : float, rl : float, noise_distrib = 'unif') -> np.array:
    samples = np.zeros(int(np.round(fs * dur, 0)))

    if noise_distrib == 'unif': samples[ : N] = np.random.randint(-10, 10, N).astype(float)
    else: samples[: N] = np.random.normal(0, 5, N)

    for i in range(N, N * (1 + samples.size//N), N):
        size = samples[i : i + N].size

        t1 = samples[i - N : i - N + size]
        if i == N: t2 = np.concatenate(([samples[i - N - 1]], samples[i - N : i - N - 1 + size]))
        else: t2 =  samples[i - N - 1 : i - N - 1 + size]

        samples[i : i + N] = rl * (t1 + t2)/2

    return samples
