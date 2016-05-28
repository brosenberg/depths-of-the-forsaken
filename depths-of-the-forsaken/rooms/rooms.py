import random

from utils import files

def load_dungeon(dungeon_file):
    raw_dungeon = files.load_file(dungeon_file)
    dungeon = {}
    for room in raw_dungeon:
        new_room = Room()
        new_room.load(raw_dungeon[room])
        dungeon[room] = new_room
    return dungeon

def dump_dungeon(dungeon):
    for room in sorted(dungeon):
        s  = "%s: " % (room,)
        s += "%d x %d x %d %s room" % (dungeon[room].length,
                                       dungeon[room].width,
                                       dungeon[room].height,
                                       dungeon[room].shape)
        if dungeon[room].desc:
            s += "\n%s" % (dungeon[room].desc,)
        for egress in dungeon[room].egress:
            s += "\n\t%s to the %s, leads to room %d" % (egress[1],
                                                       egress[2],
                                                       egress[0])
        print s

class EndlessLinearDungeon(object):
    def __init__(self, monster_db):
        self.dungeon = {}
        self.rooms = 0
        self.monster_db = monster_db

    def gen_room(self, count=1):
        while count > 0:
            w = random.randint(15, 40)
            l = w + random.randint(0, 20)
            h = random.randint(8, w)
            shape = random.choice(["rectangular", "round", "irregular"])
            if l == w and shape == "rectangular":
                shape = "square"
            egress = []
            egress.append([self.rooms+1, "door", "north"])
            if self.rooms != 0:
                egress.append([self.rooms-1, "door", "south"])
            inhabitants = []
            room = Room(width=w, length=l, height=h, shape=shape,
                        egress=egress, inhabitants=inhabitants)
            self.dungeon[self.rooms] = room
            self.rooms += 1
            count -= 1


class Room(object):
    def __init__(self, **kwargs):
        self.shape = kwargs.get("shape", "square")
        self.length = kwargs.get("length", 31)
        self.width = kwargs.get("width", 31)
        self.height = kwargs.get("height", 12)
        self.egress = kwargs.get("egress", [])
        self.inhabitants = kwargs.get("inhabitants", [])
        self.desc = kwargs.get("desc")

    def __str__(self):
       s = "a %s room, %d by %d feet, with %d foot high ceilings." % (self.shape, self.length, self.width, self.height)
       if self.desc:
           s += "\n%s" % (self.desc,)
       for exit in self.egress:
           s += "\nThere's a %s on the %sern edge of the room." % (exit[1], exit[2])
       return s

    def load(self, room):
        self.shape = room.get("shape", self.shape)
        self.shape = room.get("shape", self.shape)
        self.length = room.get("length", self.length)
        self.width = room.get("width", self.width)
        self.height = room.get("height", self.height)
        self.egress = room.get("egress", self.egress)
        self.inhabitants = room.get("inhabitants", self.inhabitants)

        self.desc = room.get("desc", self.desc)
