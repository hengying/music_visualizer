import numpy as np
import pygame
import config
from painter import Painter

class PainterAll(Painter):
    def __init__(self, holder):
        Painter.__init__(self, holder)

    def paint(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result):
        Painter.paint(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result)

        w, h = pygame.display.get_surface().get_size()

        self.clear((0, 0, 0))
        #self.blur(2)

        pygame.draw.lines(self._holder.surface, (200, 0, 0), False,
                          list(zip(
                              np.arange(len(wave_data)) / len(wave_data) * w,
                              wave_data / 100 + h / 2)))

        if len(x) > 0:
            pygame.draw.lines(self._holder.surface, (0, 255, 0), False,
                              list(zip(
                                  x / x[-1] * w,
                                  h - y * 300)))

        if fft_result is not None:
            pygame.draw.lines(self._holder.surface, (0, 0, 255), False,
                              list(zip(
                                  np.arange(len(fft_result)) / len(fft_result) * w,
                                  h / 5 * 4 - fft_result * 8 - 50)))

        self.draw_led(output_scroll, 600)
        self.draw_led(output_ennergy, 650)
        self.draw_led(output_spectrum, 700)

    def draw_led(self, led_colors, y_posi):
        if led_colors is not None:
            for i in range(len(led_colors[0])):
                pixels = np.clip(led_colors, 0, 255).astype(int)
                pygame.draw.rect(self._holder.surface, (pixels[0][i], pixels[1][i], pixels[2][i]),
                                 (i*10, y_posi, 10, 10))
