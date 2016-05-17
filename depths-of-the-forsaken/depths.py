#!/usr/bin/env python

from actors import actors
from actors import player
from combat import combat
from rooms import rooms
from utils import files
from utils import utils

ACTORS = files.load_file("actors.json")
DUNGEON = files.load_file("test-dungeon.json")
ITEMS = files.load_file("items.json")

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

def load_dungeon():
    dungeon = {}
    for room in DUNGEON:
        new_room = rooms.Room()
        new_room.load(DUNGEON[room])
        dungeon[room] = new_room
    return dungeon

def enter_dungeon(pc):
    dungeon = load_dungeon()
    room = "0"
    while True:
        print utils.color_text("purple", "-"*80)
        print "You are in a %s" % (dungeon[room],)
        if dungeon[room].inhabitants:
            print "You encounter %s" % (" and ".join(dungeon[room].inhabitants),)
            fight(pc, dungeon[room].inhabitants[0])
        i = 1
        expected = []
        for exit in dungeon[room].egress:
            print "%s: %s to the %s" % (utils.color_text("green", i), exit[1], exit[2])
            expected.append(str(i))
            i += 1
        print
        prompt = "Which door would you like to take?"
        s = int(utils.get_expected_input(expected, prompt))-1
        room = str(dungeon[room].egress[s][0])

def fight(pc, monster):
    monster = actors.load_actor(ACTORS[monster])
    fight = combat.Combat(pc, monster)
    fight.main_loop()

def main():
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
        # This is awful. Make it cleaner.
        print "What would you like to do?"
        prompt =  "%s character sheet.\n" % (utils.color_text("green", "Show"),)
        prompt += "%s or %s the game.\n" % (utils.color_text("green", "Save"), utils.color_text("green", "load"))
        prompt += "%s an enemy.\n" % (utils.color_text("green", "Fight"),)
        prompt += "Enter the %s\n" % (utils.color_text("green", "Depths"),)
        prompt += "%s for a short while. If you have enough experience to level up, you will level up upon resting.\n" % (utils.color_text("green", "Rest"),)
        prompt += "%s the game.\n" % (utils.color_text("green", "Quit"),)
        s = utils.get_expected_input(["show", "save", "load", "fight", "depths", "rest", "quit"], prompt).lower()
        if s == "show":
            print pc.character_record()
        elif s == "save":
            _save_game(pc)
        elif s == "load":
            _load_game(pc)
        elif s == "fight":
            fight(pc, "decaying skeleton")
            if pc.stats["hp_cur"] < 1:
                p = "%s game or %s?\n" % (utils.color_text("green", "Load"), utils.color_text("green", "quit"))
                r = utils.get_expected_input(["load", "quit"], p).lower()
                if r == "load":
                    load_game(pc)
                else:
                    break
        elif s == "depths":
            enter_dungeon(pc)
        elif s == "rest":
            # This should probably be its own function
            pc.stats["ap_cur"] = pc.stats["ap_max"]
            pc.stats["hp_cur"] = pc.stats["hp_max"]
            pc.stats["sp_cur"] = pc.stats["sp_max"]
            pc.stats["fatigue_cur"] = pc.stats["fatigue_max"]
            pc.lifespan += 100
            pc.rests += 1
            if pc.level_up():
                print utils.color_text("purple", "You have leveled up! You are now level %d!" % (pc.level,))
        elif s == "quit":
            break
    print "Good bye!"

if __name__ == '__main__':
    main()
