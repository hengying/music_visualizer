import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import config
import dsp

class VEnergy():
    def __init__(self):
        self._gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                             alpha_decay=0.001, alpha_rise=0.99)
        self._p = np.tile(1.0, (3, config.N_PIXELS // 2))

        self._p_filt = dsp.ExpFilter(np.tile(1, (3, config.N_PIXELS // 2)),
                               alpha_decay=0.1, alpha_rise=0.99)

    def visualize(self, y):
        """Effect that expands from the center with increasing sound energy"""
        p_energy = self._p

        y = np.copy(y)
        self._gain.update(y)
        y /= self._gain.value
        # Scale by the width of the LED strip
        y *= float((config.N_PIXELS // 2) - 1)
        # Map color channels according to energy in the different freq bands
        scale = 0.9
        r = int(np.mean(y[:len(y) // 3] ** scale))
        g = int(np.mean(y[len(y) // 3: 2 * len(y) // 3] ** scale))
        b = int(np.mean(y[2 * len(y) // 3:] ** scale))
        # Assign color to different frequency regions
        p_energy[0, :r] = 255.0
        p_energy[0, r:] = 0.0
        p_energy[1, :g] = 255.0
        p_energy[1, g:] = 0.0
        p_energy[2, :b] = 255.0
        p_energy[2, b:] = 0.0
        self._p_filt.update(p_energy)
        p_energy = np.round(self._p_filt.value)
        # Apply substantial blur to smooth the edges
        p_energy[0, :] = gaussian_filter1d(p_energy[0, :], sigma=4.0)
        p_energy[1, :] = gaussian_filter1d(p_energy[1, :], sigma=4.0)
        p_energy[2, :] = gaussian_filter1d(p_energy[2, :], sigma=4.0)
        # Set the new pixel value
        return np.concatenate((p_energy[:, ::-1], p_energy), axis=1)
