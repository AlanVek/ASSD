import numpy as np
import pandas as pd

# Clase abstracta Instrument para centralizar el comportamiento
class Instrument:
    
    # Frecuencia fundamental de cada nota
    notes = {'A' : 27.5, 'A#' : 29.0, 'B' : 30.87, 'Bb' : 29.135, 'C' : 16.35, 'C#' : 17.32, 'D' : 18.35, 'D#' : 19.0, 'E' : 20.6, 'Eb' : 19.445, 'F' : 21.83, 'F#' : 23.12 ,'G' : 24.5, 'G#' : 25.96}

    # Conversiones de hexa a nota + octava.
    df = pd.read_csv('Instruments/Notes.csv').set_index('Num')
    
    # Carga de archivo MIDI
    def load(self, midi): 
        self.midi, point = midi, 0
        self.tempos = np.array([[0], [120]])
        
        # Genera vector de tempos para cada momento de la canción
        for ev in self.midi.tracks[0]:
            point += ev.time
            if ev.is_meta and ev.type == 'set_tempo':
                if point == 0: self.tempos = np.array([[point], [ev.tempo]])
                else: self.tempos = np.append(self.tempos, [[point], [ev.tempo]], axis = 1)

        # Genera vector de tiempo/tick para cada momento de la canción
        self.time_steps = self.tempos[1] / (1e6 * self.midi.ticks_per_beat)
    
    # Devuelve el tiempo/tick para cierto punto de la canción
    def current_timestep(self, point):
        return self.time_steps[self.tempos[0] <= point][-1]

    # Sintetiza el track elegido del MIDI previamente cargado.
    # add: Si es True, entonces no borra los datos anterior, sino que los superpone.
    # nochannels: Qué canales no cargar.
    # lowtone: Cuántos armónicos bajarle a las notas.
    # Los parámetros propios de cada instrumento se deben agregar en sus respectivos constructores
    def synthesize(self, track : int, fs : float, add = False, nochannels = (), lowtone = 0, **kwargs):
        self.track = self.midi.tracks[track]
        self.fs = fs

        if not hasattr(self, 'sound'): self.sound = np.zeros(int(np.ceil(self.fs * self.midi.length)))
        elif not add:
            self.sound = self.sound[ : int(np.ceil(self.fs * self.midi.length))]
            self.sound[:] = 0
            
        point = real_time = 0
        self.used_off = []
        
        # Itera por cada evento en el track
        for i, ev in enumerate(self.track):
            
            # Carga los valores de tiempo (real y ticks)
            real_time += ev.time * self.current_timestep(point)
            point += ev.time
            
            # Si el evento es apto para ser cargado como nota...
            if not ev.is_meta and ev.type == 'note_on' and not ev.channel in nochannels and not i in self.used_off:
                
                # Obtiene información de la nota (frecuencia + octava)
                info = self.df.loc[ev.note]
                fnote, octave = self.notes[info['Note']], info['Octave']
            
                # Busca cuándo termina la nota y obtiene su duración
                d, v = self._find_off(ev.note, i, ev.channel)
                duration = d * self.current_timestep(point) * 1.5
                
                # Agrega la nota al vector de sonido
                if duration: self._add_note(fnote, octave, duration, max(v, ev.velocity), real_time, lowtone, **kwargs)
    
    # Agrega una nota al vector de sonido
    # fnote: Frecuencia
    # octave: Octava
    # duration: Duración
    # velocity: Intensidad
    # lowtone: Cuántos armónicos bajarle a las notas.
    def _add_note(self, fnote, octave, duration, velocity, real_time, lowtone, **kwargs):
        
        # Genera la nota y normaliza su amplitud
        nt = self._gen_note(freq = fnote * 2**max(0, octave-lowtone), dur = duration, **kwargs)
        nt *= velocity / np.abs(nt).max() * octave
        
        # Busca el índice en el que empieza la nota
        idx = int(np.round((self.fs * real_time), 0))

        # Agrega puntos en caso de sobrar por redondeos
        if idx + nt.size > self.sound.size:
            self.sound = np.append(self.sound, np.zeros(idx + nt.size - self.sound.size))
                    
        # Agrega la nota
        self.sound[idx : idx + nt.size] += nt
    
    # Busca cuándo termina una nota
    # note: La nota que debe terminar
    # idx: Índice a partir del cual puede estar el evento de off
    # channel: Canal al cual corresponde la nota
    def _find_off(self, note, idx, channel):
        tot = 0

        # Itera por cada evento, sumando los tiempos
        for i, ev in enumerate(self.track[idx + 1:]):
            tot += ev.time
            
            # Si encontró el correcto, devuelve la duración y la intensidad
            if not ev.is_meta and ev.type in ['note_on', 'note_off'] and ev.note == note and ev.channel == channel:
                self.used_off.append(i + idx + 1)
                return tot, ev.velocity

        return 0, 0

    # Las implementaciones de _gen_note tienen que tener esta forma siempre, y en **kwargs
    # se reciben los parámetros propios de cada instrumento.
    def _gen_note(self, freq, dur, **kwargs):
        raise Exception('No note generator: _gen_note() must be overwritten for each class')