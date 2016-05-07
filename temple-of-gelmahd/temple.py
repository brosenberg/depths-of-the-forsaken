#!/usr/bin/env python

from actors import actors
from actors import player
from combat import combat
from items import items

def main():
    pc = actors.Actor("Bob the Adventurer")
    monster = actors.Actor("Orc")
    fight = combat.Combat(pc, monster)
    fight.main_loop()

if __name__ == '__main__':
    main()
