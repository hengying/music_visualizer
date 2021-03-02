import os
import sys
import time
import numpy as np
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import config

from painter_all import PainterAll
from painter_spectrogram import PainterSpectrogram
from painter_bar import PainterBar
from painter_expand import PainterExpand

class GUI():
    def __init__(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self.__font = pygame.font.Font('fonts/uni_dzh.ttf', 24)
        self._fullscreen = False
        self.toggle_fullscreen(False)
        self.set_painter()

    @property
    def surface(self):
        return self._surface

    def run(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result):
        try:
            e = pygame.event.poll()
            if e.type == pygame.QUIT:
                raise StopIteration
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    self.quit()
                elif e.key == pygame.K_f:
                    self.toggle_fullscreen()
                elif e.key == pygame.K_ESCAPE:
                    self.toggle_fullscreen(False)
                elif e.key == pygame.K_a or e.key == pygame.K_1:
                    self.set_painter('all')
                elif e.key == pygame.K_s or e.key == pygame.K_2:
                    self.set_painter('spectrogram')
                elif e.key == pygame.K_b or e.key == pygame.K_3:
                    self.set_painter('bar')
                elif e.key == pygame.K_e or e.key == pygame.K_4:
                    self.set_painter('expand')

            self.paint(wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result)

            #self._clock.tick(config.FPS)
            self._clock.tick()
            pygame.display.flip()

        except StopIteration:
            self.quit()
        except KeyboardInterrupt:
            self.quit()

    def paint(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result):
        self._painter.paint(wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result)
        self.show_fps()

    def quit(self):
        pygame.quit()
        sys.exit()

    def show_fps(self):
        w, h = pygame.display.get_surface().get_size()

        text_surface = self.__font.render(str(int(self._clock.get_fps())), False, (125, 200, 125))
        self._surface.blit(text_surface, (w - 35, h - 30))

    def toggle_fullscreen(self, fullscreen = None):
        if fullscreen is None:
            self._fullscreen = not self._fullscreen
        else:
            self._fullscreen = fullscreen

        if self._fullscreen:
            self._surface = pygame.display.set_mode((config.FULLSCREEN_WIN_WIDTH, config.FULLSCREEN_WIN_HEIGHT), pygame.FULLSCREEN, vsync=1)
        else:
            self._surface = pygame.display.set_mode((config.WIN_WIDTH, config.WIN_HEIGHT), 0, vsync=1)

    def set_painter(self, painter_name = 'all'):
        if painter_name == 'all':
            self._painter = PainterAll(self)
        elif painter_name == 'spectrogram':
            self._painter = PainterSpectrogram(self)
        elif painter_name == 'bar':
            self._painter = PainterBar(self)
        elif painter_name == 'expand':
            self._painter = PainterExpand(self)
        else:
            raise Exception('Painter not known: {}!'.format(painter_name))
