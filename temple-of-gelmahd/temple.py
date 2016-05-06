#!/usr/bin/env python

from combat import combat
from actors import actors

def main():
    bob = actors.Actor("Bob")
    sam = actors.Actor("Sam")
    while bob.stats["hp_cur"] > 0:
        print "%s\n%s" % (bob, sam)

        (hit, damage, s) = combat.attack(bob, sam)
        print s
        if sam.stats["hp_cur"] < 1:
            break

        (hit, damage, s) = combat.attack(sam, bob)
        print s

        raw_input()
    if sam.stats["hp_cur"] < 1:
        print "Sam is dead."
    else:
        print "Bob is dead."

if __name__ == '__main__':
    main()
