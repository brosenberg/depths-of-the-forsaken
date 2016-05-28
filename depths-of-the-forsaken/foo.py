#!/usr/bin/env python
# Heavily based on http://www.pygame.org/docs/tut/tom/games2.html

import pygame

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
        font = pygame.font.SysFont("monospace", 10)
        text = font.render(line, 1, (240, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos[1] += offset
        background.blit(text, textpos)
        offset += 11

    # Draw button
    pygame.draw.rect(background, (200, 0, 0), (300, 520, 200, 30))
    pygame.draw.rect(background, (0, 0, 0), (303, 523, 194, 24))
    font = pygame.font.Font(None, 30)
    text = font.render("Enter", 1, (200, 0, 0))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos[1] += 525
    background.blit(text, textpos)

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
