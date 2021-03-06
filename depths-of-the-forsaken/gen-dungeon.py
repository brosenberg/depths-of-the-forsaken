#!/usr/bin/env python

import random
import sys

from rooms import rooms

# Should probably have a separate class for room crap
class RandomDungeon(object):
    def __init__(self, size=30):
        self.size = size
        self.m = []
        self.rooms = {}
        self.generate()

    def __str__(self):
        s = ""
        for i in self.m:
            s += "%s\n" % ("".join(i),)
        s += "\n"
        for room in self.rooms:
            s += "%s: " % (room,)
            s += "%2s %2s %2s %2s " % self.rooms[room]
            s += "(%s)" % (self.room_nearest_neighbor(room),)
            s += "\n"
        return s

    def generate(self):
        self.m = [[" " for x in range(self.size)] for y in range(self.size)]
        self.gen_room()
        for i in range(30):
            self.gen_room()

    # Because why not do O(N^2) twice?
    def gen_room(self):
        x = random.randint(1, self.size-7)
        y = random.randint(1, self.size-7)
        w = random.randint(3, 6)
        l = random.randint(3, 6)
        c = (x+(w/2), y+(l/2))
        if not self.room_fits(x, y, w, l):
            return False
        room_no = len(self.rooms)
        for i in range(x, x+w):
            for j in range(y, y+l):
                if (i, j) == (x, y):
                    self.m[j][i]     = "%d" % (room_no,)
                else:
                    self.m[j][i]     = '.'
        self.rooms[room_no] = (x, x+w, y, y+l)
        return True

    def room_fits(self, x, y, w, l):
        x_min = x-1 if x-1 > 1 else x
        x_max = x+w+1 if x+w+1 < self.size else x+w
        y_min = y-1 if y-1 > 1 else y
        y_max = y+l+1 if y+l+1 < self.size else y+l
        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                if self.m[j][i] != ' ':
                    return False
        return True

    # Should probably code this not at 1:40am
    def room_nearest_neighbor(self, room):
        nearest = -1
        closest = (sys.maxint/2, sys.maxint/2)
        for i in range(len(self.rooms)):
            if i == room:
                continue
            x_dist = self.get_distance(room, i)
            y_dist = self.get_distance(room, i, x=False)
            if x_dist+y_dist < closest[0]+closest[1]:
                closest = (x_dist, y_dist)
                nearest = i
        return nearest

    def get_distance(self, room1, room2, x=True):
        if x:
            offset = 0
        else:
            offset = 2
        # Determine if the room is to the right or the left
        dist_test1 = abs(self.rooms[room2][offset]-self.rooms[room1][offset])
        dist_test2 = abs(self.rooms[room2][offset+1]-self.rooms[room1][offset])
        # To the left
        if (dist_test2 < dist_test1):
            return dist_test2
        else:
            return abs(self.rooms[room2][offset]-self.rooms[room1][offset+1])


def main():
    d = RandomDungeon()
    print d

if __name__ == '__main__':
    main()
