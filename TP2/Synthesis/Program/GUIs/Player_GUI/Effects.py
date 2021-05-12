import numpy as np
from scipy.signal import lfilter, lfilter_zi

class efecto:
    def _init_(self):
        pass

    def comb_filter(self, fs: int, data, tau: float, T60: float, zi=None) -> tuple[np.array, np.array]:
        N = int(np.round(tau * fs, 0))
        a = np.zeros(N + 1)

        g = 10 ** (-3 * tau / T60)
        a[[0, N]] = [1, g]
        b = [1.0]

        ok_size = max(a.size, len(b)) - 1

        if not isinstance(zi, np.ndarray): zi = np.zeros(ok_size)
        elif zi.size > ok_size: zi = zi[-ok_size : ]
        elif zi.size < ok_size: zi = np.append(np.zeros(ok_size - zi.size), zi)


        res, zo = lfilter(b, a, data, zi=zi)
        res *= .4 / g

        return res, zo

    def transfer_f(self, N: int, f: float, d: float) -> tuple[np.array, np.array]:
        num = [1, -d]
        den = np.zeros(N + 2)
        den[[0, 1, -2]] = [1.0, -d, -f * (1 - d)]
        return num, den

    def echo(self, fs: int, data, tau: float, T60: float, zi=None) -> tuple[np.array, np.array]:
        return self.comb_filter(fs, data, tau, T60, zi)

    def freeverb(self, data, N: int, f: float, d: float, zi=None) -> tuple[np.array, np.array]:
        g = .5 / (1 - f)
        num, den = self.transfer_f(N, f, d)

        ok_size = max(den.size, len(num)) - 1

        if not isinstance(zi, np.ndarray): zi = np.zeros(ok_size)
        elif zi.size > ok_size: zi = zi[-ok_size : ]
        elif zi.size < ok_size: zi = np.append(np.zeros(ok_size - zi.size), zi)

        res, zo = lfilter(num, den, data, zi=zi)
        res /= g
        return res, zo

    def flanger(self, full_data, data, i: int, delay: int, range_sound: int, sweep_freq: float, fs) -> np.array:
        j = np.arange(len(data))
        index = (j - delay - np.round(range_sound * np.sin(2 * np.pi * (j + i) * sweep_freq / fs), 0)).astype(int)

        y_filt = data.copy()
        y_filt[index < 0] += full_data[index[index < 0] + i]

        index2 = (index < len(data)) & (index >= 0)
        y_filt[index2] += data[index[index2]]

        index3 = (index >= len(data)) & (index + i < len(full_data))
        y_filt[index3] += full_data[i + index[index3]]

        return y_filt/2

    def effect_select(self, efect: dict):
        # for key in efect.keys():
        #    if efect[key]: key()
        if 'echo' in efect: return self.echo(*efect['echo'])
        if 'flanger' in efect: return self.flanger(*efect['flanger']), 0
        if 'freeverb' in efect: return self.freeverb(*efect['freeverb'])
