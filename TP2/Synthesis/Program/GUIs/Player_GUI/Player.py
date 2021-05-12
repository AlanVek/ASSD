import pyaudio as pa
from threading import Thread
import numpy as np
from PyQt5.QtWidgets import QWidget, QStyle
from GUIs.Player_GUI.Player_QT import Ui_Form
from GUIs.Player_GUI.Effects import effect

# echo: Recibe fs, tau < 1, t60, zi
# freeverb: Recibe N, f < 1, d < 1, zi
# flanger: full_data, i * chunksize, delay : int, range_sound : int, sweep_freq : float

# Clase reproductor.
class Player(QWidget, Ui_Form):
    
    CHUNKSIZE = 1024
    working = False
    
    # Constructor. Si no tiene PyAudio, lo crea. Setea los parámetros iniciales.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        #self.setFixedSize(QSize(self.Play_Button.width() * 3, self.Play_Button.height() * 2 + self.Time_Label.height() * 2))

        if not Player.working: 
            Player.pAudio = pa.PyAudio() 
            Player.working = True
        
        self.paused = self.stop_playing = False
        self.th = Thread(target = self._keep_playing)

        self.Play_Button.clicked.connect(self.play)
        self.Pause_Button.clicked.connect(self.pause)
        self.Stop_Button.clicked.connect(self.stop)

        self.Play_Button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.Play_Button.setEnabled(False)
        self.Play_Button.repaint()

        self.Pause_Button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.Pause_Button.setEnabled(False)
        self.Pause_Button.repaint()

        self.Stop_Button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.Stop_Button.setEnabled(False)
        self.Stop_Button.repaint()

        self.zi = None
        self.effect_generator = effect()


        self.flanger_check.toggled.connect(self.reset_zi)
        self.freeverb_check.toggled.connect(self.reset_zi)
        self.echo_check.toggled.connect(self.reset_zi)

        self.flanger_check.toggled.connect(self.freeverb_check.setDisabled)
        self.flanger_check.toggled.connect(self.echo_check.setDisabled)

        self.freeverb_check.toggled.connect(self.flanger_check.setDisabled)
        self.freeverb_check.toggled.connect(self.echo_check.setDisabled)

        self.echo_check.toggled.connect(self.freeverb_check.setDisabled)
        self.echo_check.toggled.connect(self.flanger_check.setDisabled)
        # self.flanger_check.setCheckState()


    def reset_zi(self, keep):
        if not keep: self.zi = None

    # Carga de nuevo sonido
    def load(self, data, fs):

        self.Play_Button.setEnabled(False)
        self.Pause_Button.setEnabled(False)
        self.Stop_Button.setEnabled(False)
        
        # Normaliza el sonido y actualiza los parámetros
        self.norm = np.abs(data).max()
        self.sound = (data / self.norm).astype(np.float32)
        self.fs = fs
        self._close_stream()
        
        # Crea nuevo stream
        self.stream = self.pAudio.open(rate = self.fs, format = pa.paFloat32, channels = 1, output = True)
        self.stream.start_stream()

        length = self.sound.size / self.fs / 60
        seconds = int(np.round((length - int(length)) * 60, 0))
        self.time_full = f'{int(length)}:{seconds if seconds > 9 else "0" + str(seconds)}'
        self.Time_Label.setText(f'00:00 / ' + self.time_full)

        self.Play_Button.setEnabled(True)

    # Thread de loopeo. Va tomando datos de a CHUNKSIZE y mandándolos al stream
    def _keep_playing(self):
        data = self.sound[ : self.CHUNKSIZE]

        self.zi = None
        parameters = self.gen_parameters(data, 0)

        if parameters is not None: data_play, self.zi = self.effect_generator.effect_select(parameters)
        else: data_play = data

        data_play = data_play.tobytes()
        self.idx += 1
        curr_min = 0
        
        while len(data) and not self.stop_playing:
            if not self.paused:

                self.stream.write(data_play)
                data = self.sound[self.idx * self.CHUNKSIZE : (self.idx + 1) * self.CHUNKSIZE]
                curr_min += data.size / self.fs / 60

                parameters = self.gen_parameters(data, self.idx)
                if parameters is not None:
                    data_play, self.zi = self.effect_generator.effect_select(parameters)
                    data_play = data_play.astype(np.float32)

                    if np.any(data_play > 1):
                        data_play = (data_play / np.abs(data_play).max())

                else:
                    data_play = data

                data_play = data_play.tobytes()

                self.idx += 1
                minutes = int(curr_min)
                seconds = int((curr_min - minutes) * 60)

                self.Time_Label.setText(
                    f'{minutes}:{seconds if seconds > 9 else "0" + str(seconds)} / ' + self.time_full)

        self.stop_playing = False
        self.Play_Button.setEnabled(True)
        self.Pause_Button.setEnabled(False)
        self.Stop_Button.setEnabled(False)
        
    # Play. Inicia nueva reproducción o saca la pausa, dependiendo del estado actual
    def play(self, **kwargs):

        if self.paused:
            self.paused = False
            self.Play_Button.setEnabled(False)
            self.Pause_Button.setEnabled(True)

        elif hasattr(self, 'sound'):
            self.Stop_Button.setEnabled(True)
            self.Play_Button.setEnabled(False)
            self.Pause_Button.setEnabled(True)

            self.stop_playing = True
            if self.th.is_alive(): self.th.join() 

            self.idx, self.stop_playing = 0, False
            self.th = Thread(target = self._keep_playing)
            self.th.start()
    
    # Cierra el stream previo
    def _close_stream(self):
        self.stop_playing = True
        if self.th.is_alive(): self.th.join()
            
        if hasattr(self, 'stream') and self.stream.is_active(): 
            self.stream.stop_stream()
            self.stream.close()   
    
    # Termina la reproducción
    def stop(self): 
        self.stop_playing = True
        self.paused = False
        if self.th.is_alive(): self.th.join()
        self.Pause_Button.setEnabled(False)
        self.Play_Button.setEnabled(True)
        self.Stop_Button.setEnabled(False)
    
    # Pausa la reproducción
    def pause(self): 
        if not self.paused:
            self.paused = True
            self.Play_Button.setEnabled(True)
            self.Pause_Button.setEnabled(False)

    def playing(self): return self.th.is_alive()

    def gen_parameters(self, data, i):
        if self.echo_check.isChecked():
            return \
            {
                'echo':
                    (
                        self.fs,
                        data,
                        self.tau_slider.value() * 1e-3,
                        self.t60_slider.value(),
                        self.zi
                    )
            }
        if self.freeverb_check.isChecked():
            return \
                {
                'freeverb' :
                    (
                        data,
                        self.N_slider.value(),
                        self.f_slider.value() * 1e-2,
                        self.d_slider.value() * 1e-2,
                        self.zi
                    )
                }
        if self.flanger_check.isChecked():
            return \
                {

                'flanger' :
                    (
                        self.sound,
                        data,
                        i * self.CHUNKSIZE,
                        self.delay_slider.value(),
                        self.range_slider.value(),
                        self.sweep_slider.value() / 8,
                        self.fs
                    )
                }
        return None

    # Libera recursos de PyAudio. Llamar siempre antes de cerrar el programa.
    def close(self): 
        self._close_stream()
        self.pAudio.terminate()
        Player.working = False

        return super().close()