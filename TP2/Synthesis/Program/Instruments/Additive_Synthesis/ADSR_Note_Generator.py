import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from IPython.display import Audio
from random import seed
from random import randint

def ADSR_Note_Generator(Amp: np.array, A: float,D: float,S: float,R: float,freq: float,dur: float,fs: float) -> np.array:

    max_sustain = 2 #Duración máxima del sustain, seleccionado artesanalmente.
    #Es un magic number, la verdad, pero esta sección salió a base de prueba y error empíricamente.

    releaseTime = 0
    envelope = 0


    attackRate = 1/A #La amplitud máxima sobre el tiempo que el toma llegar.
    decayRate = (1-S)/D #Misma idea
    releaseRate = S/R #Asumo que el tiempo de release normal va a ser cuando el sustain está en su valor máximo S y quiero que baje en R segundos.

    if(dur < A + D ): #Si no llego al sustain, entro a este caso.
        if(dur > A): #Si completo el ataque, recorto el decay
            D = dur - A;
            S = 0;
            minDecay = 1 - decayRate * D; #Me fijo hasta donde baja después del ataque hasta el momento que se corta.
            releaseTime = minDecay/releaseRate #El tiempo de release va a ser el tiempo que tarda en bajar con la pendiente calculada desde minDecay hasta cero.
            attack = np.linspace(0, 1, int(A * fs)); #Creo el envelope.
            decay = np.linspace(1, minDecay, int(D * fs))
            release = np.linspace(minDecay, 0, int(releaseTime *fs))
            envelope = np.concatenate((attack, decay,release))#Concateno las rectas de la envolvente.
        else: #Si no, elimino el decay y recorto el ataque directamente.
            D = 0
            S= 0
            A = dur
            maxAttack = attackRate * dur
            releaseTime = (maxAttack)/releaseRate
            attack = np.linspace(0, maxAttack, int(A * fs))
            release = np.linspace(maxAttack, 0, int(releaseTime *fs))
            envelope = np.concatenate((attack, release))#Concateno las rectas de la envolvente.
    else:
        sustain_time = dur - A - D; #El sustain time asumiendo que fuese ideal y no decae. Luego elegiré el mínimo entre los dos.
        alpha = S/max_sustain #Fall rate del sustain. Puede ser que llegue a 0 antes del release, cuyo caso se contempla.
        t = np.linspace(0,max_sustain,int(fs*(max_sustain))) # Tiempo total
        Sf = S - t*alpha; #Asumo que desciende linealmente el sustain. Con el dur*alpha el
        index = Sf < S/100
        minIndex = np.argmax(index)
        Sf[index] = 0
        attack = np.linspace(0, 1, int(A * fs))
        decay = np.linspace(1, S, int(D * fs))
        if not minIndex:
            sustain = Sf[ : int(sustain_time*fs)]
            releaseTime = Sf[int(sustain_time*fs)]/releaseRate;
            release = np.linspace(Sf[int(sustain_time*fs)], 0, int(releaseTime * fs));
            envelope = np.concatenate((attack, decay,sustain,release))#Concateno las rectas de la envolvente.
        else:
            sustain = Sf[ : minIndex]
            releaseTime = Sf[-1]/releaseRate
            release = np.linspace(Sf[-1], 0, int(releaseTime * fs))
            envelope = np.concatenate((attack, decay,sustain,release))#Concateno las rectas de la envolvente.

    t = np.linspace(0,dur+releaseTime,int(fs*(dur+releaseTime))) # Tiempo total
    s = np.zeros(int(fs*(dur+releaseTime))) #Creo arreglo para la señal que será mi nota de piano.

    for i in range(len(Amp)):
        s += Amp[i]*np.sin(2*np.pi*((freq)*i*t));

    maxs = np.max(s)
    final_array = [(s/((maxs))*envelope) for s,envelope in zip(s,envelope)]

    return final_array;