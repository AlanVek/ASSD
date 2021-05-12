from Instruments.Instrument import Instrument
from Instruments.Additive_Synthesis.ADSR_Note_Generator import ADSR_Note_Generator
import numpy as np

class ADSR_instrument(Instrument):

    def _gen_note(self, freq, dur, **kwargs):
        norm = 440/freq #Corrección arbitraria pero que a grandes rasgos corrije bien cómo varían los ADSR de mayores y menores frecuencias a 440Hz.
        return ADSR_Note_Generator(self.Amp*norm,self.A*norm,self.D*norm,self.S*norm,self.R*norm, freq, dur,self.fs);

class Piano2(ADSR_instrument):

    def __init__(self, *args, **kwargs):
        self.A = 0.001;
        self.D = 0.2;
        self.S = 0.3;
        self.R = 0.2;
        self.Amp = np.array([1, 0.561, 0.355, 0.0631, 0.02, 0.00631, 0.00369]) #Estoy pensando si no pasar una matriz de dB para los harmónicos de cada nota, estos son de La.
         #Obs: Si suelto la tecla antes de entrar a sustain, se saltea sustain.