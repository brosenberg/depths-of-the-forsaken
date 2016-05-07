import actors
import json

from utils import utils

class Player(actors.Actor):
    def __init__(self, name, stats=None):
        super(self.__class__, self).__init__(name, stats=stats)
        self.experience = 0
        self.kills = 0
        self.lifespan = 0 # In turns

    def __repr__(self):
        r = self.pre_repr()
        r["experience"] = self.experience
        r["kills"] = self.kills
        r["lifespan"] = self.lifespan
        return json.dumps(r)

    def load(self, s):
        super(self.__class__, self).load(s)
        r = json.loads(s)
        self.experience = r["experience"]
        self.kills = r["kills"]
        self.lifespan = r["lifespan"]


def chargen():
    name = raw_input("What is your name? > ")
    stats = {}
    values = [16, 14, 12, 11, 10, 10, 8]
    print "You have the following stat values to assign:"
    print " ".join([str(x) for x in values])
    for stat in actors.BASE_STATS:
        stats[stat] = ""
    while values:
        value = values.pop(0)
        choosing = True
        while choosing:
            prompt = ""
            for stat in actors.BASE_STATS:
                prompt += "%s: %s  " % (stat.title(), stats[stat])
            prompt += "\nWhich stat would you like to assign the %d to?\n" % (value,)
            chosen_stat = utils.get_expected_input(actors.BASE_STATS, prompt)
            if stats[chosen_stat] != "":
                print "That stat has already been assigned."
            else:
                choosing = False
                stats[chosen_stat] = value
    pc = Player(name, stats=stats)
    return pc
