import math
import numpy as np
import pygame
import config
from painter import Painter
import cv2

class PainterSpectrogram(Painter):
    def __init__(self, holder):
        Painter.__init__(self, holder)
        self._current_x = 0

        self.clear((0, 0, 0))

    def paint(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result):
        Painter.paint(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result)

        w, h = pygame.display.get_surface().get_size()

        if fft_result is not None:
            #print(np.max(fft_result), np.mean(fft_result))
            fft_size = len(fft_result)
            scale_y = h / fft_size * 3
            if scale_y < 1:
                scale_y = 1
            scale_x = math.floor(scale_y)

            a = np.log10(fft_result[::-1] + 1) * 8
            #a = np.log10(np.log10(fft_result[::-1] + 1) + 1) * 55
            a = np.clip(a * 10, 0, 255).astype(np.uint8)
            a = 255 - a
            a = a.reshape((1, len(fft_result)))
            # 1 byte to 3 byte per pixel
            #a = np.stack((a,) * 3, axis=-1)

            #https://learnopencv.com/applycolormap-for-pseudocoloring-in-opencv-c-python/
            im_color = cv2.applyColorMap(a, cv2.COLORMAP_JET)

            spectrum_line = pygame.surfarray.make_surface(im_color)

            large_image = pygame.transform.smoothscale(spectrum_line,
                                               (scale_x, int(fft_size * scale_y)))
            #large_image = pygame.transform.scale(spectrum_line,
            #                                   (scale_x, int(fft_size * scale_y)))

            self._holder.surface.blit(large_image, (self._current_x, h - fft_size * scale_y))

            self._current_x += scale_x
            if self._current_x >= w:
                self._current_x = 0
