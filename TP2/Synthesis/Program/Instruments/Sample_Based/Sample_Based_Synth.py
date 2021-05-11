from Instruments.Instrument import Instrument
import soundfile as sf
import os
import librosa
#path = os.getcwd()
path = 'Instruments/Sample_Based'
import numpy as np


# Clase abstracta SampleBasedInstrument para los instrumentos sintetizados por muestras.
class SampleBasedInstrument(Instrument):

    # Constructor. Tira error si se intenta instanciar.
    def __init__(self, *args, **kwargs):
        raise Exception('Cannot instantiate abstract class SampleBasedInstrument')

    # Genera un diccionario para asociar cada una de las muestras con su correspondiente frecuencia. (Ej samples_dic[0]="F6").
    def generate_samples_dic(self):
        self.samples_dic = {}
        for sample in os.listdir(self.samples_location):
            instr_note = sample.split(".")
            self.samples_dic[sample] = self.frec_dic[
                instr_note[-2]]  # Notamos que el value sale del diccionario de frecuencias creado al principio.
        # print(self.samples_dic)

    # Crea un diccionario con las distintas notas y sus correspondientes frecuencias
    def create_frec_index(self):
        self.frec_dic = {}
        notes = ["A0", "Bb0", "B0", "C1", "Db1", "D1", "Eb1", "E1", "F1", "Gb1", "G1", "Ab1", "A1", "Bb1", "B1",
                 "C2", "Db2", "D2", "Eb2", "E2", "F2", "Gb2", "G2", "Ab2", "A2", "Bb2", "B2",
                 "C3", "Db3", "D3", "Eb3", "E3", "F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3",
                 "C4", "Db4", "D4", "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4", "B4",
                 "C5", "Db5", "D5", "Eb5", "E5", "F5", "Gb5", "G5", "Ab5", "A5", "Bb5", "B5",
                 "C6", "Db6", "D6", "Eb6", "E6", "F6", "Gb6", "G6", "Ab6", "A6", "Bb6", "B6",
                 "C7", "Db7", "D7", "Eb7", "E7", "F7", "Gb7", "G7", "Ab7", "A7", "Bb7", "B7", "C8"]
        i = 0
        for note_ in notes:
            frec = round(440 / 32 * (2 ** (((21 + i) - 9) / 12)), 3)
            self.frec_dic[note_] = frec
            i += 1
        # print(self.frec_dic)

    # Busca la muestra que más se parece en frecuencia a la frecuencia de la nota.
    def find_closest_note(self, freq):
        # Devuelve la muestra correspondiente en forma de string (es el nombre del archivo sin la terminación)
        # Búsqueda del key tal que su value minimice una condición tomada de
        # https://stackoverflow.com/questions/3282823/get-the-key-corresponding-to-the-minimum-value-within-a-dictionary
        closest_note_ = min(self.samples_dic, key=lambda x: abs(self.samples_dic[x] - freq))
        return closest_note_

    # Recupera el código MIDI correspondiente a una frecuencia
    def get_midi_note(self, frec):
        # return 12*np.log2(frec/440)+69
        return 12 * np.log2(frec * 32 / 440) + 9

    # Se busca estirar o comprimir la señal en tiempo sin afectar el tono o pitch
    # Estira o comprime la señal sample_data en un factor time_scaling_factor
    # Para pasar al dominio de la frecuencia se realiza la STFT, usando una ventana de Hann
    # La STFT se implementa con la librería librosa
    def time_scale(self, sample_data, time_scaling_factor):
        # stft(y, n_fft=2048, hop_length=None, win_length=None, window='hann', center=True, dtype=np.complex64, pad_mode='reflect')
        # Returns D such that
        # np.abs(D[f, t]) is the magnitude of frequency bin f at frame t, and
        # np.angle(D[f, t]) is the phase of frequency bin f at frame t.
        # D es una matriz de tamaño (1+n_fft/2)*t

        # Computo STFT
        FFT_window_size = 2048
        frame_size = 2048
        hop_size = frame_size / 4
        STFT = librosa.core.stft(sample_data, n_fft=2048).transpose()
        # Filas= STFT.shape[0] #cantidad de instantes
        # Columnas= STFT.shape[1] #cantidad de bines/2+1 por simetría: 1025

        scaled_time_axis = np.arange(0, STFT.shape[0],
                                     time_scaling_factor)  # Nuevo arreglo de tiempos, original tomado cada time_scaling_factor
        time_scaled_STFT = np.zeros((len(scaled_time_axis), STFT.shape[1]),
                                    dtype=np.complex_)  # Arreglo de len(time_scaled_data) elementos, donde cada elemento es un arreglo de tamaño STFT_columns, y cada elemento de este último arreglo es un número complejo
        phase = np.angle(STFT[0])  # fase espectral de cada bin (valores entre -pi y pi)
        delta_t = hop_size / FFT_window_size
        expected_phase = 2 * np.pi * delta_t * np.arange(0, STFT.shape[1])
        # expected_phase=(2 * np.pi * hop_size * np.arange(0, STFT.shape[1]))/FFT_window_size #valores entre cero y (2*pi)*(1/4)*1025 (unwrapped)
        STFT = np.concatenate((STFT, np.zeros((1, STFT.shape[1]))), axis=0)

        # Implementación del algoritmo en sí. Se realiza la correción de fase para formar la matriz espectral escalada en tiempo.
        for i, time_data in enumerate(scaled_time_axis):
            left_frame = int(np.floor(time_data))
            right_frame = left_frame + 1
            weight = time_data - np.floor(time_data)  # Ver *
            current_frame = STFT[[left_frame, right_frame],
                            :]  # Los datos de mi stft que corresponden al frame temporal que estoy analizando
            local_magnitude = (1 - weight) * np.absolute(current_frame[0, :]) + weight * np.absolute(
                current_frame[1, :])  # Se computa la magnitud de la ventana temporal con peso

            # Hay que calcular la fase predicha con la frecuencia de bin sin wrapping,
            # luego hallar el error de fase entre ventanas, hacerle un wrapping para que esté entre -pi y pi, y
            # luego estimar la fase real
            predicted_phase = np.angle(current_frame[0, :]) + expected_phase
            phase_error = np.angle(current_frame[1, :]) - predicted_phase
            wrap_factor = np.floor(phase_error / (2 * np.pi))  # cuántos múltiplos de 2pi hay que restar
            phase_error_wrapped = phase_error - 2 * np.pi * wrap_factor
            time_scaled_STFT[i, :] = local_magnitude * np.exp(phase * 1j)
            phase += phase_error_wrapped + expected_phase

        return librosa.core.istft(time_scaled_STFT.transpose())
        # * Los tiempos son enteros, t=1,2,... Pero puede ser que por mi factor de escalamiento, los tenga que computar en tiempos no enteros, ej: t=1.7
        # Entonces, tomo mis ventanas left=1 y right=2, y tomo weight=0.7. Al considerar magnitud, la de t=2 tendrá más peso
        # Luego, mag=0.3*mag(t1)+0.7*mag(t2)

    # Método que se debe sobreescribir para cada clase de instrumento. Genera una nota.
    # freq: Frecuencia de la nota
    # dur: Duración de la nota
    # stretch_factor: Límite inferior de frecuencia para lingering
    # b: Parámetro propio de cada instrumento
    # La frecuencia de sampleo fs es propia de la instancia, y se obtiene con self.fs

    def pitch_shift(self, sample_data, samplerate, shift, time_scaling_factor):
        # El cambio de tonos se hace primero haciendo un cambio en el tiempo con la función time_scaling
        # Y luego resampleando a mayor velocidad para recuperar la longitud original del tiempo
        FFT_size = 2048
        pitch_shift_factor = 2 ** (1.0 * shift / 12.0)  # Recordar que el shift se consiguió en semitonos
        total_scaling_factor = len(sample_data) / (len(sample_data) * pitch_shift_factor) * time_scaling_factor
        # total_scaling_factor=len(sample_data)/(len(sample_data)*pitch_shift_factor+FFT_size)*time_scaling_factor #Cambio en el tiempo por cambio de tono + duración
        # total_scaling_factor=pitch_shift_factor*time_scaling_factor
        time_scaled_signal = self.time_scale(sample_data, total_scaling_factor)
        # print('factor:')
        # print(pitch_shift_factor)
        # print('Total scaling factor:')
        # print(total_scaling_factor)

        # Ahora se debe resamplear la señal para acomodar la longitud a la buscada
        # pitch_shifted_signal=signal.resample(x=np.floor(time_scaled_signal[FFT_size:]), num=pitch_shift_factor)
        # pitch_shifted_signal=self.resample(time_scaled_signal[FFT_size:],pitch_shift_factor)
        pitch_shifted_signal = self.resample(time_scaled_signal, pitch_shift_factor)
        return pitch_shifted_signal.astype(sample_data.dtype)

    def resample(self, input_, factor):
        # Primero se crea el nuevo arreglo espaciado según el factor de resampleo, y luego se copian los valores
        # del arreglo original que correspondan. La correción de new_times tiene que ver con cómo funciona astype(int) en numpy arrays
        new_times_temp = np.round(np.arange(0, len(input_), factor))
        new_times = new_times_temp[new_times_temp < len(input_)].astype(int)
        resampled_input = input_[new_times.astype(int)]
        return resampled_input
        # output_length=int((len(input_)-1)/factor)
        # output=np.zeros(output_length)
        # for i in range(output_length-1):
        #    x = float(i*factor)
        #    ix = np.floor(x)
        #    dx = x - ix
        #    output[i] = input_[ix]*(1.0 - dx) + input_[ix+1]*dx
        # return output

    def _gen_note(self, freq, dur, **kwargs):
        # Crea vector resultante con la duración correspondiente
        samples = np.zeros(int(np.round(self.fs * dur, 0)))
        # print(freq)

        # Busco la muestra que más se parezca en frecuencia a la frecuencia de la nota que se quiere sintetizar.
        closest_note = self.find_closest_note(freq)
        # print(closest_note)

        # Recupero los códigos midi de la frecuencia a sintetizar y de la más cercana que hay en mis muestras
        MIDI_note = self.get_midi_note(freq)
        MIDI_closest_note = self.get_midi_note(self.samples_dic[closest_note])
        # print('MIDI note')
        # print(MIDI_note)
        # print('MIDI closest')
        # print(MIDI_closest_note)

        # A partir de esos códigos, puede ver cuántos debo correr la nota de mi muestra para que sea igual a la que tengo que sintetizar.
        # Se hace en MIDI ya que ésta es la unidad de tonos
        # shift es cantidad de semitonos
        shift = MIDI_note - round(MIDI_closest_note)
        # print(shift)

        # Se recupera la información de la muestra que más se acerca a la nota deseada y sobre la que se trabajará.
        # sample_data es un array 1*number_of_samples que tiene el valor de amplitud de cada una de las samples del archivo .wav
        # samplerate es la frecuencia de muestreo del archivo .wav
        sample_data, samplerate = sf.read(
            self.samples_location + closest_note)  # Notamos que el argumento es ahora el path completo a la muestra.
        # Se recupera la duración en samples de la nota a sintetizar.
        note_dur_in_samples = int(round(dur * self.fs))

        # Puede ocurrir que la nota buscada esté contenida en mis muestras, de donde shift=0 y no se requiere procesamiento en tono alguno.
        # No obstante, puede ser que la duración de la muestra difiera de la de la nota buscada, de donde se precisa alargar o comprimir la muestra.
        # Como simplemente samplear a mayor o menor velocidad modifica la parte espectral de la señal (pitch), indefectiblemente se debe buscar otra manera
        # Se utiliza un algoritmo llamado Phase Vocoder. Primero se hace un cambio en frecuencia y luego se introduce el cambio temporal en frecuencia
        # Manteniendo el tono, y luego haciendo la transformada inversa para recuperar la señal en el tiempo

        if int(shift) == 0:
            if (dur == 0.0):
                return samples
            else:
                time_scaling_factor = len(
                    sample_data) / note_dur_in_samples  # En cuántos samples se debe alargar o comprimir mi muestra. Si es mayor a 1, se comprime, menor a 1 se alarga
                time_scaled_note = self.time_scale(sample_data, time_scaling_factor)
                # time_scaled_note=pyrb.time_stretch(sample_data,sr=samplerate,rate=time_scaling_factor)
                # if(len(time_scaled_note)>note_dur_in_samples):
                #    k=len(time_scaled_note)-note_dur_in_samples
                #    while(k>0):
                #        time_scaled_note=np.delete(time_scaled_note,len(time_scaled_note)-1)
                #        k=k-1
                # elif(len(time_scaled_note)<note_dur_in_samples):
                #    k=note_dur_in_samples-len(time_scaled_note)
                #    while(k>0):
                #        time_scaled_note=np.insert(time_scaled_note,len(time_scaled_note),0)
                #        k=k-1
                # print("\n")
                return time_scaled_note

        else:
            if (dur == 0.0):
                return samples
            else:
                # Hay que escalar en tiempo y en frecuencia
                time_scaling_factor_ = len(sample_data) / note_dur_in_samples
                pitch_shifted_note = self.pitch_shift(sample_data, samplerate, shift, time_scaling_factor_)
                # factor=2**(1.0*shift/12.0)
                # pitch_shifted_note=pyrb.pitch_shift(y=sample_data,sr=samplerate,n_steps=factor)
                # time_scaling_factor_=len(pitch_shifted_note)/note_dur_in_samples
                # time_shifted_note=pyrb.time_stretch(y=pitch_shifted_note,sr=samplerate,rate=time_scaling_factor_)
                # print('longitud de la señal')
                # print(len(pitch_shifted_note))
                # if(len(pitch_shifted_note)>note_dur_in_samples):
                #    k=len(pitch_shifted_note)-note_dur_in_samples
                #    while(k>0):
                #        pitch_shifted_note=np.delete(pitch_shifted_note,len(pitch_shifted_note)-1)
                #        k=k-1
                # elif(len(pitch_shifted_note)<note_dur_in_samples):
                #    k=note_dur_in_samples-len(pitch_shifted_note)
                #    while(k>0):
                #        pitch_shifted_note=np.insert(pitch_shifted_note,len(pitch_shifted_note),0)
                #        k=k-1
                # print("\n")
                return pitch_shifted_note


class SampleBasedPiano(SampleBasedInstrument):

    def __init__(self, *args, **kwargs):
        self.instrument = 'Piano'
        # print(self.instrument)
        self.samples_location = path + '/Note_samples/' + self.instrument + '/'
        # print(self.samples_location)
        self.create_frec_index()  # Crea índice para luego generar el diccionario con las muestras (Quizá se podría usar directamente el notes.csv)
        self.generate_samples_dic()  # Crea el diccionario con las muestras

    def _gen_note(self, freq, dur, **kwargs):
        return super()._gen_note(freq=freq, dur=dur)


class SampleBasedGuitar(SampleBasedInstrument):

    def __init__(self, *args, **kwargs):
        self.instrument = 'AcousticGuitar'
        # print(self.instrument)
        self.samples_location = path + '/Note_samples/' + self.instrument + '/'
        # print(self.samples_location)
        self.create_frec_index()  # Crea índice para luego generar el diccionario con las muestras (Quizá se podría usar directamente el notes.csv)
        self.generate_samples_dic()  # Crea el diccionario con las muestras

    def _gen_note(self, freq, dur, **kwargs):
        return super()._gen_note(freq=freq, dur=dur)


class SampleBasedBanjo(SampleBasedInstrument):

    def __init__(self, *args, **kwargs):
        self.instrument = 'Banjo'
        # print(self.instrument)
        self.samples_location = path + '/Note_samples/' + self.instrument + '/'
        # print(self.samples_location)
        self.create_frec_index()  # Crea índice para luego generar el diccionario con las muestras (Quizá se podría usar directamente el notes.csv)
        self.generate_samples_dic()  # Crea el diccionario con las muestras

    def _gen_note(self, freq, dur, **kwargs):
        return super()._gen_note(freq=freq, dur=dur)


class SampleBasedElectricBass(SampleBasedInstrument):

    def __init__(self, *args, **kwargs):
        self.instrument = 'ElectricBass'
        # print(self.instrument)
        self.samples_location = path + '/Note_samples/' + self.instrument + '/'
        # print(self.samples_location)
        self.create_frec_index()  # Crea índice para luego generar el diccionario con las muestras (Quizá se podría usar directamente el notes.csv)
        self.generate_samples_dic()  # Crea el diccionario con las muestras

    def _gen_note(self, freq, dur, **kwargs):
        return super()._gen_note(freq=freq, dur=dur)


class SampleBasedSaxophone(SampleBasedInstrument):

    def __init__(self, *args, **kwargs):
        self.instrument = 'Saxophone'
        # print(self.instrument)
        self.samples_location = path + '/Note_samples/' + self.instrument + '/'
        # print(self.samples_location)
        self.create_frec_index()  # Crea índice para luego generar el diccionario con las muestras (Quizá se podría usar directamente el notes.csv)
        self.generate_samples_dic()  # Crea el diccionario con las muestras

    def _gen_note(self, freq, dur, **kwargs):
        return super()._gen_note(freq=freq, dur=dur)


class SampleBasedBassoon(SampleBasedInstrument):

    def __init__(self, *args, **kwargs):
        self.instrument = 'Bassoon'
        # print(self.instrument)
        self.samples_location = path + '/Note_samples/' + self.instrument + '/'
        # print(self.samples_location)
        self.create_frec_index()  # Crea índice para luego generar el diccionario con las muestras (Quizá se podría usar directamente el notes.csv)
        self.generate_samples_dic()  # Crea el diccionario con las muestras

    def _gen_note(self, freq, dur, **kwargs):
        return super()._gen_note(freq=freq, dur=dur)

