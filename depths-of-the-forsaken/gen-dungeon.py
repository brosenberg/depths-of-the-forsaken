#!/usr/bin/env python

import random

from rooms import rooms

class RandomDungeon(object):
    def __init__(self, size=30):
        self.size = size
        self.m = []
        self.generate()

    def __str__(self):
        s = ""
        for i in self.m:
            s += "%s\n" % (" ".join(i),)
        return s

    def generate(self):
        self.m = [[" " for x in range(self.size)] for y in range(self.size)]
        self.gen_room()
        for i in range(30):
            self.gen_room()

    def gen_room(self):
        x = random.randint(1, self.size-7)
        y = random.randint(1, self.size-7)
        w = random.randint(3, 6)
        l = random.randint(3, 6)
        c = (x+(w/2), y+(l/2))
        if not self.room_fits(x, y, w, l):
            return False
        for i in range(x, x+w):
            for j in range(y, y+l):
                if (i, j) == c:
                    self.m[i][j] = '#'
                else:
                    self.m[i][j] = '.'

    def room_fits(self, x, y, w, l):
        x_min = x-1 if x-1 > 1 else x
        x_max = x+w+1 if x+w+1 < self.size else x+w
        y_min = y-1 if y-1 > 1 else y
        y_max = y+l+1 if y+l+1 < self.size else y+l
        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                if self.m[i][j] != ' ':
                    return False
        return True

def main():
    d = RandomDungeon()
    print d

if __name__ == '__main__':
    main()
