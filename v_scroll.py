import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import config
import dsp

class VScroll():
    def __init__(self):
        self._gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                             alpha_decay=0.001, alpha_rise=0.99)

        self._p = np.tile(1.0, (3, config.N_PIXELS // 2))

    def visualize(self, y):
        """Effect that originates in the center and scrolls outwards"""
        p_scroll = self._p

        y = y**2.0
        self._gain.update(y)
        y /= self._gain.value
        y *= 255.0
        r = int(np.max(y[:len(y) // 3]))
        g = int(np.max(y[len(y) // 3: 2 * len(y) // 3]))
        b = int(np.max(y[2 * len(y) // 3:]))
        # Scrolling effect window
        p_scroll[:, 1:] = p_scroll[:, :-1]
        p_scroll *= 0.98
        p_scroll = gaussian_filter1d(p_scroll, sigma=0.2)
        # Create new color originating at the center
        p_scroll[0, 0] = r
        p_scroll[1, 0] = g
        p_scroll[2, 0] = b

        self._p = p_scroll
        # Update the LED strip
        return np.concatenate((p_scroll[:, ::-1], p_scroll), axis=1)
