import math
import numpy as np
import pygame
import config
from painter import Painter

BAR_TOP_THICKNESS = 2
BAR_STAY_MAX_COUNT = 45
BAR_DROP_SPEED = 10

BAR_COLOR = (175, 175, 175)
BAR_TOP_COLOR = (0, 255, 125)

class PainterBar(Painter):
    def __init__(self, holder):
        Painter.__init__(self, holder)
        self.clear((0, 0, 0))
        self._old_bar_posis = None
        self._bar_posi_stay_count = None

    def paint(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result):
        Painter.paint(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result)

        w, h = pygame.display.get_surface().get_size()

        self.clear((0, 0, 0))
        #self.clear_with_alpha((0, 0, 0), 30)
        #self.blur(2)

        count = len(y)
        if count > 0:
            x_step = w / count

            bar_posis = []

            y = np.log10(y + 1) * 4

            for i in range(count):
                bar_height = y[i] * 500
                if bar_height > h - BAR_TOP_THICKNESS:
                    bar_height = h - BAR_TOP_THICKNESS

                bar_posi = h - bar_height

                bar_posis.append(bar_posi)

                pygame.draw.rect(self._holder.surface, BAR_COLOR,
                                 (i * x_step + 1, bar_posi, x_step - 2, bar_height))

            if self._old_bar_posis is None:
                self._old_bar_posis = bar_posis
                self._bar_posi_stay_count = [0 for i in range(len(bar_posis))]

            for i in range(len(bar_posis)):
                if bar_posis[i] < self._old_bar_posis[i]:
                    self._old_bar_posis[i] = bar_posis[i]
                    self._bar_posi_stay_count[i] = 0
                else:
                    self._bar_posi_stay_count[i] += 1
                    if self._bar_posi_stay_count[i] > BAR_STAY_MAX_COUNT:
                        drop_speed = h * BAR_DROP_SPEED / 768

                        self._old_bar_posis[i] += BAR_DROP_SPEED
                        if bar_posis[i] < self._old_bar_posis[i]:
                            self._old_bar_posis[i] = bar_posis[i]
                            self._bar_posi_stay_count[i] = 0

                pygame.draw.rect(self._holder.surface, BAR_TOP_COLOR,
                                 (i * x_step + 1, self._old_bar_posis[i] - BAR_TOP_THICKNESS, x_step - 2, BAR_TOP_THICKNESS))

            #pygame.draw.lines(self._holder.surface, (0, 255, 0), False,
            #                  list(zip(
            #                      x / x[-1] * w,
            #                      h - y * 300)))
