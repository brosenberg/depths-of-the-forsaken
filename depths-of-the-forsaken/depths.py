#!/usr/bin/env python

from actors import actors
from actors import player
from combat import combat
from utils import utils

# TODO: Move save and load to utils.
def _load_game(pc):
    print "Specify the path to the save file:"
    save_file = raw_input("> ")
    try:
        with open(save_file, 'r') as f:
            pc.load(f.read())
    except IOError:
        print "Could not load the save game file '%s'" % (save_file,)
        return False
    return True

def load_game(pc):
    loaded = False
    while not loaded:
        print "Would you like to load your game?"
        if utils.get_yesno_input():
            loaded = _load_game(pc)
        else:
            return

def _save_game(pc):
    print "Specify the path to the save file:"
    save_file = raw_input("> ")
    try:
        with open(save_file, 'w') as f:
            f.write(repr(pc))
    except IOError:
        print "Could not write save game file '%s'" % (save_file,)
        return False
    return True

def save_game(pc):
    saved = False
    while not saved:
        print "Would you like to save your game?"
        if utils.get_yesno_input():
            saved = _save_game(pc)
        else:
            return

def main():
    actors = utils.load_file("actors.json")
    items = utils.load_file("items.json")
    pc = player.Player("Bob")
    print "You have been banished to the Depths of the Forsaken!"
    prompt = "Would you like to %s a new character or %s an old one?\n" % (utils.color_text("green", "create"), utils.color_text("green", "load"))
    s = utils.get_expected_input(["create", "load"], prompt)
    if s == "load":
        loaded = False
        while not loaded:
            loaded = _load_game(pc)
    else:
        pc = player.chargen()
        save_game(pc)
    while True:
        print "What would you like to do?"
        prompt =  "%s character sheet.\n" % (utils.color_text("green", "Show"),)
        prompt += "%s or %s the game.\n" % (utils.color_text("green", "Save"), utils.color_text("green", "load"))
        prompt += "%s an enemy.\n" % (utils.color_text("green", "Fight"),)
        prompt += "%s the game.\n" % (utils.color_text("green", "Quit"),)
        s = utils.get_expected_input(["show", "save", "load", "fight", "quit"], prompt).lower()
        if s == "show":
            print pc.character_record()
        elif s == "save":
            _save_game(pc)
        elif s == "load":
            _load_game(pc)
        elif s == "fight":
            monster = actors.Actor("Decaying Skeleton")
            fight = combat.Combat(pc, monster)
            fight.main_loop()
            if pc.stats["hp_cur"] < 1:
                p = "%s game or %s?\n" % (utils.color_text("green", "Load"), utils.color_text("green", "quit"))
                r = utils.get_expected_input(["load", "quit"], p).lower()
                if r == "load":
                    load_game(pc)
                else:
                    break
        elif s == "quit":
            break
    print "Good bye!"

if __name__ == '__main__':
    main()
