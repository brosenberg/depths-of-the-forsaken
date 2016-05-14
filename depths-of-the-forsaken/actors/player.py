import actors
import json

from items import items
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
        if type(s) == str:
            r = json.loads(s)
        elif type(s) == dict:
            r = s
        self.experience = r.get("experience", self.experience)
        self.kills = r.get("kills", self.kills)
        self.lifespan = r.get("lifespan", self.lifespan)

    def character_record(self):
        s = "%s  Level %d\n\n" % (utils.color_text("purple", self.name), self.level)
        s += utils.color_text("cyan", "- Statistics -\n")
        for stat in actors.BASE_STATS:
            s += "%22s %s\n" % (utils.color_text("yellow", stat.title())+":", self.stats[stat])
        s += "\n"
        for stat in ["HP", "Fatigue", "AP", "SP"]:
            lstat = stat.lower()
            s += "%s %d/%d  " % (stat, self.stats[lstat+"_cur"], self.stats[lstat+"_max"])
        s += "\n"
        s += "Time in the Depths: %d\n" % (self.lifespan,)

        s += utils.color_text("cyan", "\n- Equipped items -\n")
        for slot in sorted(self.equipment):
            item = items.str_item(self.equipment[slot])
            s += "%11s %s\n" % (slot.title()+":", item)

        s += utils.color_text("cyan", "\n- Inventory -\n")
        for item in sorted(self.inventory):
            s += "%s\n" % (items.str_item(item),)
        return s


def chargen():
    name = raw_input("What is your name? > ")
    stats = {}
    values = [16, 14, 12, 11, 10, 10, 8]
    print "You will now assign values to your stats"
    print
    print utils.color_text("yellow", "Toughness")
    print "Determines your hit points, fatigue, and modifies your melee damage."
    print utils.color_text("yellow", "Agility")
    print "Determines your initiative in combat, your chance to hit enemies, and your chance to dodge."
    print utils.color_text("yellow", "Perception")
    print "Determines nothing right now!"
    print utils.color_text("yellow", "Intelligence")
    print "Determines nothing right now!"
    print utils.color_text("yellow", "Willpower")
    print "Determines nothing right now!"
    print utils.color_text("yellow", "Charisma")
    print "Determines nothing right now!"
    print utils.color_text("yellow", "Luck")
    print "Slightly effects every action you perform."
    print
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
                prompt += "%s: %2s  " % (stat.title(), stats[stat])
            prompt += "\nWhich stat would you like to assign the %d to?\n" % (value,)
            chosen_stat = utils.get_expected_input(actors.BASE_STATS, prompt).lower()
            if stats[chosen_stat] != "":
                print "That stat has already been assigned."
            else:
                choosing = False
                stats[chosen_stat] = value
    pc = Player(name, stats=stats)
    return pc
