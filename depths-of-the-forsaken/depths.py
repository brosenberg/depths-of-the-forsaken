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
        (w, h) = terminal_size()
        if w >= 107 and h >= 50:
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
        sys.exit(0)
    elif s == "load":
        load_game(pc)
    elif s == "start":
        pc = player.chargen()
        save_game_prompt()
    print pc

def main():
    main_menu()

if __name__ == '__main__':
    main()
