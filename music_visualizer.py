import config
import microphone
from fft import FFT
from gui import GUI

# 根据以下源码改编：
# https://github.com/scottlawsonbc/audio-reactive-led-strip

class App():
    def __init__(self):
        self._fft = FFT()
        self._gui = GUI()

    def start(self):
        def call_back(audio_samples):
            self._microphone_update(audio_samples)

        microphone.start_stream(call_back)

    def _microphone_update(self, audio_samples):
        x, y, output_scroll, output_ennergy, output_spectrum, fft_result = self._fft.process(audio_samples)
        self._gui.run(audio_samples, x, y, output_scroll, output_ennergy, output_spectrum, fft_result)


if __name__ == '__main__':
    app = App()
    app.start()
