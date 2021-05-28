from Instruments.Instrument import Instrument, np
from Instruments.Karplus_Strong.Karplus_Strong import Karplus_Strong, Karplus_Strong_Z

# Clase abstracta KSInstrument para los instrumentos sintetizados por Karplus-Strong
class KSInstrument(Instrument):

    def _gen_note(self, freq, dur, **kwargs):
        if 'stretch_lim' in kwargs: self.stretch_lim = kwargs.pop('stretch_lim')
        else: self.stretch_lim = 200

        if isinstance(self.R, int):
            return Karplus_Strong_Z(freq, fs = self.fs, dur = dur, R = (self.R + 1)/2, S = max(1, freq/self.stretch_lim))
        else:
            return Karplus_Strong(freq, fs = self.fs, dur = dur, R = self.R, S = max(1, freq/self.stretch_lim))
    
# Clase guitarra, hereda de KSInstrument. Sobreescribe a _gen_note con b = 1
class Guitar(KSInstrument):
    
    def __init__(self, *args, **kwargs):
        self.R = 1

# Clase harpa, hereda de KSInstrument. Sobreescribe a _gen_note con b = -1
class Harp(KSInstrument):
    
    def __init__(self, *args, **kwargs):
        self.R = -1

class drumR:
    def __init__(self, p = .5):
        self.p = p

    def __mul__(self, other):

        if isinstance(other, (int, float, complex)): return other * (-1)**np.random.binomial(1, self.p)
        return other * (-1)**np.random.binomial(1, self.p, len(other))

    def __rmul__(self, other): return self * other

# Clase tambor, hereda de KSInstrument. Sobreescribe a _gen_note con b = drumB(), que al multiplicar toma valor 
# 1 o -1 con probabilidad 0.5.
class Drum(KSInstrument):
    def __init__(self, *args, **kwargs):
        self.R = drumR()
