#!/usr/bin/env python

from actors import actors
from combat import combat
from items import items

def main():
    player = actors.Actor("Player", display_name="You")
    monster = actors.Actor("Orc")
    fight = combat.Combat(player, monster)
    fight.main_loop()

if __name__ == '__main__':
    main()
