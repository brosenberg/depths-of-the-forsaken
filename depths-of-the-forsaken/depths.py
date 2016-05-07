#!/usr/bin/env python

from actors import actors
from actors import player
from combat import combat
from items import items
from utils import utils

def load_game(pc):
    print "Specify the path to the save file:"
    save_file = raw_input("> ")
    with open(save_file, 'r') as f:
        pc.load(f.read())

def save_game(pc):
    print "Specify the path to the save file:"
    save_file = raw_input("> ")
    with open(save_file, 'w') as f:
        f.write(repr(pc))

def main():
    pc = player.Player("Bob")
    print "Welcome to the Temple of Gelmahd!"
    prompt = "Would you like to %s a new character or %s an old one?\n" % (utils.color_text("green", "create"), utils.color_text("green", "load"))
    s = utils.get_expected_input(["create", "load"], prompt)
    if s == "load":
        load_game(pc)
    else:
        pc = player.chargen()
        save_game(pc)
    monster = actors.Actor("Orc")
    fight = combat.Combat(pc, monster)
    fight.main_loop()
    if pc.stats["hp_cur"] < 1:
        print "Would you like to load your game?"
        if utils.get_yesno_input():
            load_game(pc)
    else:
        print "Would you like to save your game?"
        if utils.get_yesno_input():
            save_game(pc)
    print "Good bye!"

if __name__ == '__main__':
    main()
