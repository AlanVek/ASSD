import pyaudio as pa
from threading import Thread
import numpy as np
from PyQt5.QtWidgets import QWidget, QStyle
from GUIs.Player_GUI.Player_QT import Ui_Form

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

    # Carga de nuevo sonido
    def load(self, data, fs):


        self.Play_Button.setEnabled(False)
        self.Pause_Button.setEnabled(False)
        self.Stop_Button.setEnabled(False)
        
        # Normaliza el sonido y actualiza los parámetros
        self.sound = (data / np.abs(data).max()).astype(np.float32)
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
        data = self.sound[ : self.CHUNKSIZE].tobytes()
        self.idx += 1
        curr_min = 0
        
        while len(data) and not self.stop_playing:
            if not self.paused:
                self.stream.write(data)
                data = self.sound[self.idx * self.CHUNKSIZE : (self.idx + 1) * self.CHUNKSIZE]
                curr_min += data.size / self.fs / 60
                data = data.tobytes()

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

    # Libera recursos de PyAudio. Llamar siempre antes de cerrar el programa.
    def close(self): 
        self._close_stream()
        self.pAudio.terminate()
        Player.working = False

        return super().close()