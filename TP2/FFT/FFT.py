import numpy as np

def fftshift(y):
    return np.append(y[y.size//2:], y[:y.size//2])

def ifft(X_f):
    return 1 / X_f.size * fft(X_f.conj()).conj()

def fftfreq(N : int, dtime : float) -> np.array:
    res = np.arange(N) / (N * dtime)
    return fftshift(res - res[N//2])

def bitrev_indices(n):
    cant_bits = int(np.log2(n))
    res = np.zeros(n, dtype = int)
    res[:2] = [0, n//2]
    for i in range(1, cant_bits):
        res[2**i : 2**(i + 1)] = res[ : 2**i] + (2**(cant_bits - i - 1))
    return res

def fft(x_n):
    if x_n.size <= 1: return x_n
    if x_n.size & x_n.size - 1: raise Exception ('Size must have shape 2^k')

    gamma = int(np.log2(x_n.size))
    order = bitrev_indices(x_n.size).reshape(-1, 1)
    W = np.exp(-2j * np.pi * order[::2] / x_n.size)

    res = x_n.astype(complex)

    for i in range(gamma):
        groups = res.reshape(2**i, 2, -1)
        groups[:, 1] *= W[:2**i]
        groups[:, 0] += groups[:, 1]
        groups[:, 1] *= -2
        groups[:, 1] += groups[:, 0]

    return res[order].reshape(-1)

