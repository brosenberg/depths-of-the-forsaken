#!/usr/bin/env python

from rooms import rooms
from utils import utils


def load_dungeon():
    dungeon_rooms = utils.load_file("test-dungeon.json")
    dungeon = {}
    for room in dungeon_rooms:
        new_room = rooms.Room()
        new_room.load(dungeon_rooms[room])
        dungeon[room] = new_room
    return dungeon

def main():
    dungeon = load_dungeon()
    print [x for x in dungeon]
    room = "0"
    while True:
        print "Current room:"
        print dungeon[room]
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

if __name__ == '__main__':
    main()
