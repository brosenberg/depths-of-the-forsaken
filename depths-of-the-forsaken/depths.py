#!/usr/bin/env python

import sys

from actors import actors
from actors import player
from combat import combat
from rooms import rooms
from utils import files
from utils import utils

def load_game(pc):
    print "Specify the path to the save file:"
    save_file = raw_input("> ")
    files.load_game(pc, save_file)

def load_game_prompt(pc):
    loaded = False
    while not loaded:
        print "Would you like to load your game?"
        if utils.get_yesno_input():
            loaded = load_game(pc)
        else:
            return

def save_game(pc):
    print "Specify the path to the save file:"
    save_file = raw_input("> ")
    files.save_game(pc, save_file)

def save_game_prompt(pc):
    saved = False
    while not saved:
        print "Would you like to save your game?"
        if utils.get_yesno_input():
            saved = save_game(pc)
        else:
            return

# Taken from: http://stackoverflow.com/a/3010495
def terminal_size():
    import fcntl, termios, struct
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h

def print_banner():
    banner = "DEPTHS OF THE FORSAKEN"
    try:
        (term_w, term_h) = terminal_size()
        s = open("banner").read()
        banner_w = len(max(s.split("\n")))
        banner_h = len(s.split("\n"))
        # We'll be printing 4 lines after the banner
        if term_w >= banner_w and term_h >= banner_h+4:
            banner = open("banner").read()
    except:
        pass
    print utils.color_text("red", banner)

def main_menu():
    pc = player.Player("")
    print_banner()

    prompt =  "%s a new adventure\n" % (utils.color_text("green", "Start"),)
    prompt += "%s a saved game\n" % (utils.color_text("green", "Load"),)
    prompt += "%s to DOS\n" % (utils.color_text("green", "Quit"),)

    s = utils.get_expected_input(["start", "load", "quit"], prompt)
    if s == "quit":
        print "\nC:\>"
        sys.exit(0)
    elif s == "load":
        load_game(pc)
    elif s == "start":
        pc = player.chargen()
        save_game_prompt()
    return pc

def intro_blurb():
    print utils.color_text("grey", "You awaken on the cold stone floor of a desolate room. A demonic nine foot tall creature with huge bat wings for arms and flesh that appears to be made from obsidian towers before you. It gazes down at you with fiery eyes. With a booming voice it declares:")
    print utils.color_text("red", "\"Welcome to the Infinite Depths of the Forsaken. You are one of the Discarded; reincarnated from souls unwanted or worthless to the gods. You may have a horrid, pitiful person who amounted to nothing. Or perhaps you disgraced your god and your life. What ever you did, you are now here. Weak and under prepared. Here you will bring meaning back to your worthless soul.", bold=True)
    print utils.color_text("red", "You will die here. No one will remember or care what you have done here. Accomplish something here so that in the next life you do not return here, so that I do not have to look upon you ever again.\"", bold=True)
    print utils.color_text("grey", "Its eyes close and it wraps its wings around itself and stands motionless. You stand there stunned for a time before regaining your senses and looking around the room. On the floor nearby you see a corpse laying in dried pool of blood, its wrists slashed open and a crude stone knife clenced in one hand.")

def enter_dungeon(dungeon, pc, actor_db):
    intro_blurb()
    room = "0"
    while True:
        print utils.color_text("purple", "-"*80)
        print "You are in a %s" % (dungeon[room],)
        if dungeon[room].inhabitants:
            monster_name = dungeon[room].inhabitants[0]
            print "You encounter %s" % (monster_name,)
            monster = actors.load_actor(actor_db[monster_name])
            encounter = combat.Combat(pc, monster)
            encounter.main_loop()
        i = 1
        expected = ["rest", "inventory"]
        exits = {}
        prompt = "What would you like to do?\n"
        for exit in dungeon[room].egress:
            exit_name = "%s %d" % (exit[1], i)
            expected.append(exit_name)
            exits[exit_name] = str(exit[0])
            prompt += "Go through %s on the %s wall\n" % (utils.color_text("green", exit_name), exit[2])
            i += 1
        prompt += "Set up camp and %s\n" % (utils.color_text("green", "rest"),)
        prompt += "Manage your %s\n" % (utils.color_text("green", "inventory"),)
        s = utils.get_expected_input(expected, prompt)
        if exits.get(s):
            room = exits[s]
        elif s == "rest":
            rest()
        elif s == "inventory":
            inventory()

def rest():
    print "You rest."

def inventory():
    print "Your inventory is now diamonds."

def main():
    dungeon = rooms.load_dungeon("test-dungeon.json")
    actor_db = files.load_file("actors.json")
    item_db = files.load_file("items.json")
    while True:
        pc = main_menu()
        enter_dungeon(dungeon, pc, actor_db)

if __name__ == '__main__':
    main()
