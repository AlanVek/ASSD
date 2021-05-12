from Instruments.Instrument import Instrument
from Instruments.Additive_Synthesis.ADSR_Note_Generator import ADSR_Note_Generator

class ADSR_instrument(Instrument):

    def _gen_note(self, freq, dur, **kwargs):
        return ADSR_Note_Generator(self.Amp,self.A,self.D,self.S,self.R,self.freq,self.dur,self.fs);

class Píano(ADSR_instrument):

    def __init__(self, *args, **kwargs):
        self.A = 0.001;
        self.D = 0.2;
        self.S = 0.3;
        self.R = 0.2;
        self.Amp = [1, 0.561, 0.355, 0.0631, 0.02, 0.00631, 0.00369]
         #Obs: Si suelto la tecla antes de entrar a sustain, se saltea sustain.