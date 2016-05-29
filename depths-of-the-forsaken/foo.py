#!/usr/bin/env python
# Heavily based on http://www.pygame.org/docs/tut/tom/games2.html

import pygame

FONT="fonts/Cousine-Regular.ttf"


class DrawThing(object):
    def __init__(self):
        # If this thing will change if the cursor hovers over it.
        self.can_highlight = False
        # If this thing will change if the cursor clicks it.
        self.can_press = False
        pass

    def draw(self):
        pass

class Text(DrawThing):
    def __init__(self, surface_ref, string, **kwargs):
        super(self.__class__, self).__init__()

        self.surface_ref = surface_ref

        self.string = string
        font = kwargs.get("font", FONT)
        self.font_size = kwargs.get("font_size", 20)
        self.font = pygame.font.Font(font, self.font_size)
        self.font_color = kwargs.get("font_color", (240, 240, 240))
        self.centerx = kwargs.get("centerx")
        self.centery = kwargs.get("centery")

    def draw(self):
        offset = 0
        for line in self.string.split("\n"):
            text = self.font.render(line, 1, self.font_color)
            textpos = text.get_rect()
            if self.centerx:
                textpos.centerx = self.centerx
            if self.centery:
                textpos.centery = self.centery
            textpos[1] += offset
            self.surface_ref.blit(text, textpos)
            offset += self.font_size+1

class Button(DrawThing):
    def __init__(self, surface_ref, x_pos, y_pos, x_size, y_size, **kwargs):
        super(self.__class__, self).__init__()
        self.can_highlight = True
        self.can_press = True

        self.surface_ref = surface_ref

        self.rect = pygame.Rect(x_pos, y_pos, x_size, y_size)
        self.inner_rect = self.rect.copy()
        self.inner_rect.inflate_ip(-2, -2)

        self.border_color = kwargs.get("border_color", (0, 200, 0))
        self.bg_color = kwargs.get("bg_color", (0, 0, 0))
        self.highlight_color = kwargs.get("border_color", (0, 100, 0))

        text = kwargs.get("text")
        if text:
            font = kwargs.get("font", FONT)
            font_size = kwargs.get("font_size", 20)
            self.font = pygame.font.Font(font, font_size)
            self.text_color = kwargs.get("text_color", self.border_color)
            self.text = self.font.render(text, 1, self.text_color)
            self.text_raw = text
        else:
            self.text = None
            self.text_raw = None

    def draw(self, highlight=False):
        self.surface_ref.fill(self.border_color, self.rect)
        if highlight:
            self.surface_ref.fill(self.highlight_color, self.inner_rect)
        else:
            self.surface_ref.fill(self.bg_color, self.inner_rect)
        if self.text:
            textpos = self.text.get_rect()
            textpos.centerx = self.rect.centerx
            textpos.centery = self.rect.centery
            self.surface_ref.blit(self.text, textpos)

    def press(self):
        print "[%s] pressed" % (self.text_raw,)

    def get(self):
        return (self.rect.x, self.rect.y, self.rect.w, self.rect.h)

def main():
    # Init all the things
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Depths of the Forsaken")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    screen.blit(background, (0, 0))
    pygame.display.flip()


    draw_queue = []

    draw_queue.append(Button(background, 50, 520, 200, 30, text="Create Character"))
    draw_queue.append(Button(background, 300, 520, 200, 30, text="Continue"))
    draw_queue.append(Button(background, 550, 520, 200, 30, text="Flee to DOS"))

    s = open("banner").read()
    draw_queue.append(Text(background, s, font=FONT, font_size=10, font_color=(200, 0, 0),
                           centerx=background.get_rect().centerx, centery=15))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for thing in draw_queue:
                    if thing.can_press:
                        (x1, y1, x2, y2) = thing.get()
                        if x1+x2 >= mouse_pos[0] >= x1 and y1+y2 >= mouse_pos[1] >= y1:
                            thing.press()

        screen.blit(background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        for thing in draw_queue:
            # Draw things
            if thing.can_highlight:
                (x1, y1, x2, y2) = thing.get()
                if x1+x2 >= mouse_pos[0] >= x1 and y1+y2 >= mouse_pos[1] >= y1:
                    thing.draw(highlight=True)
                else:
                    thing.draw()
            else:
                thing.draw()

        # FIXME: Call update() on each changed thing
        pygame.display.update()
        clock.tick(15)

if __name__ == '__main__':
    main()
