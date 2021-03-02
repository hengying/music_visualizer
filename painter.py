import pygame

class Painter():
    def __init__(self, holder):
        self._holder = holder
        self._old_w = 0
        self._old_h = 0
        self._alpha_surface = None

    def paint(self, wave_data, x, y, output_scroll, output_ennergy, output_spectrum, fft_result):
        w, h = pygame.display.get_surface().get_size()
        if self._old_w != w or self._old_h != h:
            self._update_alpha_surface(w, h)
            self._old_w = w
            self._old_h = h

    def clear(self, color):
        w, h = pygame.display.get_surface().get_size()
        pygame.draw.rect(self._holder.surface, color,
                         (0, 0, w, h))

    # https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
    def clear_with_alpha(self, color, alpha):
        self._alpha_surface.set_alpha(alpha)
        self._alpha_surface.fill(color)
        self._holder.surface.blit(self._alpha_surface, (0, 0))

    def _update_alpha_surface(self, w, h):
        self._alpha_surface = pygame.Surface((w, h))

    # https://www.akeric.com/blog/?p=720
    # 这个速度快些，但是模糊后有偏移，超一个方向移动无法解决
    def blur(self, amt):
        if amt < 1.0:
            raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s" % amt)
        scale = 1.0 / float(amt)
        surf_size = self._holder.surface.get_size()
        scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
        surf = pygame.transform.smoothscale(self._holder.surface, scale_size)
        surf = pygame.transform.smoothscale(surf, surf_size)
        self._holder.surface.blit(surf, (0, -1))

# 下面的方法能工作，但是太慢了
"""
    # https://stackoverflow.com/questions/30723253/blurring-in-pygame
    def blur(self, r):
        from PIL import Image, ImageFilter

        strFormat = 'RGB'
        raw_str = pygame.image.tostring(self._holder.surface, strFormat, False)
        image = Image.frombytes(strFormat, self._holder.surface.get_size(), raw_str)
        image_blured = image.filter(ImageFilter.GaussianBlur(radius = r))

        blured_image = pygame.image.fromstring(image_blured.tobytes("raw", strFormat), self._holder.surface.get_size(), strFormat)
        self._holder.surface.blit(blured_image, (0, 0))
"""