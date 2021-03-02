import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import config
import dsp
from utils import *

class VSpectrum():
    def __init__(self):
        self._r_filt = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                               alpha_decay=0.2, alpha_rise=0.99)
        self._g_filt = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                               alpha_decay=0.05, alpha_rise=0.3)
        self._b_filt = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                               alpha_decay=0.1, alpha_rise=0.5)
        self._common_mode = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                                    alpha_decay=0.99, alpha_rise=0.01)

        self._prev_spectrum = np.tile(0.01, config.N_PIXELS // 2)

    def visualize(self, y):
        """Effect that maps the Mel filterbank frequencies onto the LED strip"""
        y = np.copy(interpolate(y, config.N_PIXELS // 2))
        self._common_mode.update(y)
        diff = y - self._prev_spectrum
        _prev_spectrum = np.copy(y)
        # Color channel mappings
        r = self._r_filt.update(y - self._common_mode.value)
        g = np.abs(diff)
        b = self._b_filt.update(np.copy(y))
        # Mirror the color channels for symmetric output
        r = np.concatenate((r[::-1], r))
        g = np.concatenate((g[::-1], g))
        b = np.concatenate((b[::-1], b))
        output = np.array([r, g, b]) * 255
        return output

