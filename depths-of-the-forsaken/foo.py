#!/usr/bin/env python
# Heavily based on http://www.pygame.org/docs/tut/tom/games2.html

import pygame

FONT="fonts/Cousine-Regular.ttf"


class View(object):
    def __init__(self):
        self.draw_queue = []

    def draw(self, mouse_pos):
        for thing in self.draw_queue:
            if thing.can_highlight:
                (x1, y1, x2, y2) = thing.get()
                if x1+x2 >= mouse_pos[0] >= x1 and y1+y2 >= mouse_pos[1] >= y1:
                    thing.draw(highlight=True)
                else:
                    thing.draw()
            else:
                thing.draw()

    def press(self, mouse_pos):
        events = []
        for thing in self.draw_queue:
            if thing.can_press:
                (x1, y1, x2, y2) = thing.get()
                if x1+x2 >= mouse_pos[0] >= x1 and y1+y2 >= mouse_pos[1] >= y1:
                    events.append(thing.press())
        return events

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
    def __init__(self, name, surface_ref, x_pos, y_pos, x_size, y_size, **kwargs):
        super(self.__class__, self).__init__()
        self.can_highlight = True
        self.can_press = True

        self.name = name
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
        else:
            self.text = None

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
        return self.name

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

    views = {}
    current_view = "main menu"

    # Main Menu ########
    views["main menu"] = View()
    views["main menu"].draw_queue.append(Button("create", background, 50, 520, 200, 30, text="Create Character"))
    views["main menu"].draw_queue.append(Button("load screen", background, 300, 520, 200, 30, text="Continue"))
    views["main menu"].draw_queue.append(Button("quit", background, 550, 520, 200, 30, text="Flee to DOS"))

    s = open("banner").read()
    t = Text(background, s, font_size=10, font_color=(200, 0, 0),
             centerx=background.get_rect().centerx, centery=15)
    views["main menu"].draw_queue.append(t)

    # Load Screen ######
    views["load screen"] = View()
    views["load screen"].draw_queue.append(Button("load", background, 50, 520, 200, 30, text="Load"))
    views["load screen"].draw_queue.append(Button("main menu", background, 300, 520, 200, 30, text="Main Menu"))
    views["load screen"].draw_queue.append(Button("quit", background, 550, 520, 200, 30, text="Flee to DOS"))

    t = Text(background, "Load Game", centerx=background.get_rect().centerx, centery=30)
    views["load screen"].draw_queue.append(t)
    
    screen_dirty = False
    while True:
        view_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONUP:
                view_events += views[current_view].press(pygame.mouse.get_pos())

        screen.blit(background, (0, 0))
        views[current_view].draw(pygame.mouse.get_pos())

        for event in view_events:
            if event == "quit":
                return
            if event == "load screen":
                current_view = "load screen"
                screen_dirty = True
            if event == "main menu":
                current_view = "main menu"
                screen_dirty = True

        if screen_dirty:
            background.fill((0, 0, 0))
            pygame.display.flip()
            screen_dirty = False
        else:
            # FIXME: Call update() on each changed thing
            pygame.display.update()

        clock.tick(15)

if __name__ == '__main__':
    main()
