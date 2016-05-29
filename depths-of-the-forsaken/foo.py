#!/usr/bin/env python
# Heavily based on http://www.pygame.org/docs/tut/tom/games2.html

import pygame

FONT="fonts/Cousine-Regular.ttf"


class Button(object):
    def __init__(self, surface_ref, x_pos, y_pos, x_size, y_size, **kwargs):
        self.surface_ref = surface_ref
        self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
        self.inner_rect = self.rect.copy()
        self.inner_rect.inflate_ip(-2, -2)
        self.border_color = kwargs.get("border_color", (0, 200, 0))
        self.bg_color = kwargs.get("bg_color", (0, 0, 0))
        self.highlight_color = kwargs.get("border_color", (0, 175, 0))
        self.text_color = kwargs.get("text_color", self.border_color)
        text = kwargs.get("text")
        if text:
            self.text = font.render(text, 1, self.text_color)
        else:
            self.text = None
        self.font = kwargs.get("font", FONT)
        self.font_size = kwargs.get("font_size", 20)

    def draw(self):
        self.surface_ref.fill(self.border_color, self.rect)
        self.surface_ref.fill(self.bg_color, self.inner_rect)
        # FIXME
        if self.text:
            textpos = self.text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos[1] += 525
            background.blit(text, textpos)

    def get(self):
        return (self.rect.x, self.rect.y, self.rect.w, self.rect.h)

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Depths of the Forsaken")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Draw banner
    s = open("banner").read()
    offset = 15
    for line in s.split("\n"):
        font = pygame.font.Font(FONT, 10)
        text = font.render(line, 1, (240, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos[1] += offset
        background.blit(text, textpos)
        offset += 11

    # Draw button
    btn = Button(background, 300, 520, 200, 30)
    btn.draw()

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == '__main__':
    main()
