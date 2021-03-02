import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import config
import dsp
from v_scroll import VScroll
from v_energy import VEnergy
from v_spectrum import VSpectrum

class FFT():
    def __init__(self):
        self._fft_window = np.hamming(int(config.MIC_RATE / config.FPS) * config.N_ROLLING_HISTORY)
        self._mel_gain = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                             alpha_decay=0.01, alpha_rise=0.99)
        self._mel_smoothing = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                                  alpha_decay=0.2, alpha_rise=0.99)

        # Number of audio samples to read every time frame
        self._samples_per_frame = int(config.MIC_RATE / config.FPS)

        # Array containing the rolling audio sample window
        self._y_roll = np.random.rand(config.N_ROLLING_HISTORY, self._samples_per_frame) / 1e16

        self._fft_plot_filter = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                                        alpha_decay=0.5, alpha_rise=0.99)
        self._v_scroll = VScroll()
        self._v_energy = VEnergy()
        self._v_spectrum = VSpectrum()

    def process(self, audio_samples):
        # Normalize samples between 0 and 1
        y = audio_samples / 2.0 ** 15
        # Construct a rolling window of audio samples
        self._y_roll[:-1] = self._y_roll[1:]
        self._y_roll[-1, :] = np.copy(y)
        y_data = np.concatenate(self._y_roll, axis=0).astype(np.float32)

        vol = np.max(np.abs(y_data))
        if vol < config.MIN_VOLUME_THRESHOLD:
            # print('No audio input. Volume below threshold. Volume:', vol)
            return [], [], None, None, None, None
        else:
            mel, fft_result = self.get_mel(y_data)

            # Map filterbank output onto LED strip
            output_scroll = self._v_scroll.visualize(mel)
            output_ennergy = self._v_energy.visualize(mel)
            output_spectrum = self._v_spectrum.visualize(mel)

            # Plot filterbank output
            x = np.linspace(config.MIN_FREQUENCY, config.MAX_FREQUENCY, len(mel))

            return x, self._fft_plot_filter.update(mel), output_scroll, output_ennergy, output_spectrum, fft_result


    def get_mel(self, y_data):
        # Transform audio input into the frequency domain
        N = len(y_data)
        N_zeros = 2 ** int(np.ceil(np.log2(N))) - N
        # Pad with zeros until the next power of two
        y_data *= self._fft_window
        y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
        YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
        # Construct a Mel filterbank from the FFT data
        mel = np.atleast_2d(YS).T * dsp.mel_y.T
        # Scale data to values more suitable for visualization
        # mel = np.sum(mel, axis=0)
        mel = np.sum(mel, axis=0)
        mel = mel ** 2.0
        # Gain normalization
        self._mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
        mel /= self._mel_gain.value
        mel = self._mel_smoothing.update(mel)

        return mel, YS