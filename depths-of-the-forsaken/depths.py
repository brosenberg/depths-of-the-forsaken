#!/usr/bin/env python

import sys

from actors import actors
from actors import player
from combat import combat
from items import items
from rooms import rooms
from template import template
from utils import files
from utils import utils

ACTORS = files.load_file("actors.json")
ITEMS = files.load_file("items.json")

def load_game(pc):
    loaded = False
    while not loaded:
        print "Specify the path to the save file:"
        save_file = raw_input("> ")
        loaded = files.load_game(pc, save_file)
        if not loaded:
            print "Could not load file '%s'" % (save_file,)

def load_game_prompt(pc):
    print "Would you like to load your game?"
    if utils.get_yesno_input():
        load_game(pc)
    else:
        return

def save_game(pc):
    print "Specify the path to the save file:"
    save_file = raw_input("> ")
    return files.save_game(pc, save_file)

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

    t =  "<action>Start</action> a new adventure\n"
    t += "<action>Load</action> a saved game\n"
    t += "<action>Quit</action> to DOS\n"

    (prompt, tags) = template.process(t)
    actions = tags.get("action")

    s = utils.get_expected_input(actions + ["debug"], prompt)
    if s == "quit":
        quit()
    elif s == "debug":
        debug()
    elif s == "load":
        load_game(pc)
    elif s == "start":
        pc = player.chargen()
        save_game_prompt(pc)
    return pc

def quit():
    print "\nC:\>"
    sys.exit(0)

def intro_blurb():
    t = "<desc>You awaken on the cold stone floor of a desolate room. A demonic nine foot tall creature with huge bat wings for arms and flesh that appears to be made from obsidian towers before you. It gazes down at you with fiery eyes. With a booming voice it declares:</desc>\n"
    t += "<quote>\"Welcome to the Infinite Depths of the Forsaken. You are one of the Discarded; reincarnated from souls unwanted or worthless to the gods. You may have a horrid, pitiful person who amounted to nothing. Or perhaps you disgraced your god and your life. What ever you did, you are now here. Weak and under prepared. Here you will bring meaning back to your worthless soul."
    t += "You will die here. No one will remember or care what you have done here. Accomplish something here so that in the next life you do not return here, so that I do not have to look upon you ever again.\"</quote>\n"
    t += "<desc>Its eyes close and it wraps its wings around itself and stands motionless. You stand there stunned for a time before regaining your senses and looking around the room. On the floor nearby you see a corpse laying in dried pool of blood, its wrists slashed open and a crude stone knife clenced in one hand.</desc>"
    print template.process(t)[0]

def enter_dungeon(dungeon, pc):
    intro_blurb()
    room = "0"
    while True:
        if not dungeon.dungeon.get(room):
            new_rooms = 1 + int(room) - dungeon.rooms
            dungeon.gen_room(count=new_rooms)
        print utils.color_text("purple", "-"*80)
        print "You are in a %s" % (dungeon.dungeon[room],)
        if dungeon.dungeon[room].inhabitants:
            monster_name = dungeon.dungeon[room].inhabitants[0]
            print "You encounter %s" % (monster_name,)
            monster = actors.load_actor(ACTORS[monster_name])
            encounter = combat.Combat(pc, monster)
            encounter.main_loop()
        i = 1
        expected = ["camp", "inventory"]
        exits = {}
        prompt = "What would you like to do?\n"
        for exit in dungeon.dungeon[room].egress:
            exit_name = "%s %d" % (exit[1], i)
            expected.append(exit_name)
            exits[exit_name] = str(exit[0])
            prompt += "Go through %s on the %s wall.\n" % (utils.color_text("green", exit_name), exit[2])
            i += 1
        prompt += "Set up %s.\n" % (utils.color_text("green", "camp"),)
        prompt += "Manage your %s.\n" % (utils.color_text("green", "inventory"),)
        s = utils.get_expected_input(expected, prompt)
        if exits.get(s):
            room = exits[s]
        elif s == "camp":
            camp(pc)
        elif s == "inventory":
            inventory(pc)

def camp(pc):
    print "You attempt to make some semblance of a camp."
    while True:

        t =  "What would you like to do?\n"
        t += "<action>Rest</action> for a bit.\n"
        t += "<action>Save</action> the game.\n"
        t += "<action>Load</action> a saved game.\n"
        t += "<action>Review</action> your character sheet.\n"
        t += "<action>Break</action> camp.\n"
        t += "<action>Quit</action> to DOS.\n"

        (prompt, tags) = template.process(t)

        actions = tags.get("action")

        s = utils.get_expected_input(actions, prompt)
        if s == "rest":
            pc.stats["ap_cur"] = pc.stats["ap_max"]
            pc.stats["hp_cur"] = pc.stats["hp_max"]
            pc.stats["sp_cur"] = pc.stats["sp_max"]
            pc.stats["fatigue_cur"] = pc.stats["fatigue_max"]
            pc.lifespan += 100
            pc.rests += 1
            if pc.level_up():
                print utils.color_text("purple", "You have leveled up! You are now level %d!" % (pc.level,))
        elif s == "save":
            save_game(pc)
        elif s == "load":
            load_game(pc)
        elif s == "review":
            print pc.character_record()
        elif s == "quit":
            quit()
        elif s == "break":
            break

def inventory(pc):
    while True:
        print pc.get_equipment_str()
        print pc.get_inventory_str()
        t  = "What would you like to do?\n"
        t += "<action>Equip</action> an item.\n"
        t += "<action>Unequip</action> an item.\n"
        t += "<action>Destroy</action> an item.\n"
        t += "<action>Finish</action> managing your inventory.\n"
        (prompt, tags) = template.process(t)

        actions = tags.get("action")

        s = utils.get_expected_input(actions, prompt)
        if s == "equip":
            (_, tags) = template.process(pc.get_inventory_template())
            actions = tags.get("action")
            item_no = int(utils.get_expected_input(actions, "Which item?"))
            item = pc.inventory_remove(item_no)
            (equip_s, equipped) = pc.equip(item)
            if equipped:
                print equip_s
            else:
                pc.inventory_add(item)
                print equip_s

        elif s == "unequip":
            (_, tags) = template.process(pc.get_equipment_template())
            actions = tags.get("action")
            prompt = "Which equipment slot?"
            slot = utils.get_expected_input(actions, prompt)
            if slot == "both hands":
                slot = "main hand"
            print pc.unequip(slot)

        if s == "destroy":
            (_, tags) = template.process(pc.get_inventory_template())
            actions = tags.get("action")
            item_no = int(utils.get_expected_input(actions, "Which item?"))
            pc.inventory_remove(item_no)

        if s == "finish":
            break

def main():
    try:
        if sys.argv[1] == "debug":
            debug()
    except IndexError:
        pass
    while True:
        pc = main_menu()
        dungeon = rooms.EndlessLinearDungeon(ACTORS)
        enter_dungeon(dungeon, pc)

# This should probably all be tests.
def debug():
    pc = player.Player("")
    files.load_game(pc, "debug_char")
    pc.inventory = []
    pc.inventory_add(ITEMS["hatchet"])
    pc.inventory_add(ITEMS["stone spear"])
    pc.inventory_add(ITEMS["stone knife"])
    pc.inventory_add(ITEMS["Father of Swords"])
    dungeon = rooms.EndlessLinearDungeon(ACTORS)
    dungeon.gen_room(count=5)
    rooms.dump_dungeon(dungeon.dungeon)
    files.save_game(pc, "debug_char")
    quit()

if __name__ == '__main__':
    main()
