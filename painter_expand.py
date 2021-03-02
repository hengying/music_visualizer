import math
import numpy as np
import pygame
import config
from painter import Painter

class PainterExpand(Painter):
    def __init__(self, holder):
        Painter.__init__(self, holder)
        self.clear((0, 0, 0))
        self._led_size = 0
        self._small_surface = None
        self._small_surface_w = None
        self._small_surface_h = None

    def paint(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result):
        Painter.paint(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result)

        w, h = pygame.display.get_surface().get_size()

        #led_data = output_scroll
        led_data = output_ennergy
        #led_data = output_spectrum

        if led_data is not None:
            if self._small_surface is None:
                self._small_surface_h = len(led_data[0])
                self._small_surface_w = int(self._small_surface_h / h * w)
                self._small_surface = pygame.Surface((self._small_surface_w, self._small_surface_h))
                self._small_surface.fill((0, 0, 0))

            alpha_surface = pygame.Surface((self._small_surface_w, self._small_surface_h))
            alpha = 2
            alpha_surface.set_alpha(alpha)
            alpha_surface.fill((0, 0, 0))
            self._small_surface.blit(alpha_surface, (0, 0))

            self.draw_led_points(led_data)

            x_posi = self._small_surface.get_width() // 2
            self._small_surface.blit(self._small_surface, (x_posi + 1, 0), (x_posi, 0, self._small_surface_w - x_posi, self._small_surface_h))
            self._small_surface.blit(self._small_surface, (0, 0), (1, 0, x_posi, self._small_surface_h))

            #large_image = pygame.transform.smoothscale(self._small_surface, (w, h))
            large_image = pygame.transform.scale(self._small_surface, (w, h))

            self._holder.surface.blit(large_image, (0, 0))

            """
            # 这是原来的方法，速度较慢
            self._led_size = h // len(led_data[0])
            x_posi = (w - self._led_size) // 2
            y_posi = (h - self._led_size * len(led_data[0])) // 2

            self._holder.surface.blit(self._holder.surface, (x_posi + self._led_size, 0), (x_posi, 0, w - x_posi, h))
            x = x_posi % self._led_size
            self._holder.surface.blit(self._holder.surface, (x - self._led_size, 0), (x, 0, x_posi - x + self._led_size, h))

            self.clear_with_alpha((0, 0, 0), 2)
            #self.blur(2)

            self.draw_led(led_data, x_posi, y_posi)
            """


    def draw_led(self, led_colors, x_posi, y_posi):
        if led_colors is not None:
            for i in range(len(led_colors[0])):
                pixels = np.clip(led_colors, 0, 255).astype(int)
                pygame.draw.rect(self._holder.surface, (pixels[0][i], pixels[1][i], pixels[2][i]),
                                 (x_posi, y_posi + i*self._led_size, self._led_size, self._led_size))

    def draw_led_points(self, led_colors):
        if led_colors is not None:
            x_posi = self._small_surface.get_width() // 2
            for i in range(len(led_colors[0])):
                pixels = np.clip(led_colors, 0, 255).astype(int)
                self._small_surface.set_at((x_posi, i), (pixels[0][i], pixels[1][i], pixels[2][i]))

