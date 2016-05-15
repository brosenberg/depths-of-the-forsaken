#!/usr/bin/env python

from rooms import rooms
from utils import utils


def main():
    dungeon_rooms = utils.load_file("test-dungeon.json")
    dungeon = {}
    for room in dungeon_rooms:
        new_room = rooms.Room()
        new_room.load(dungeon_rooms[room])
        dungeon[room] = new_room
    for room in dungeon:
        print dungeon[room]

if __name__ == '__main__':
    main()
