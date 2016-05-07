import actors
import json

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
        chosen_stat = ""
        while chosen_stat not in actors.BASE_STATS:
            for stat in actors.BASE_STATS:
                print "%s: %s  " % (stat.title(), stats[stat]),
            print
            print "Which stat would you like to assign the %d to?" % (value,)
            chosen_stat = raw_input("> ").lower()
            if chosen_stat in actors.BASE_STATS and  stats[chosen_stat] != "":
                print "That stat has already been assigned."
                chosen_stat = ""
        stats[chosen_stat] = value
    pc = Player(name, stats=stats)
    return pc
