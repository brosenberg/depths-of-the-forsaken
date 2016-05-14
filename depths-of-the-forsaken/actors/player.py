import actors
import json

from items import items
from utils import utils

class Player(actors.Actor):
    def __init__(self, name, stats=None):
        super(self.__class__, self).__init__(name, stats=stats)
        self.experience = 0
        self.karma = 0
        self.kills = 0
        self.lifespan = 0 # In turns
        self.rests = 0 # Number of times rested

    def __repr__(self):
        r = self.pre_repr()
        r["experience"] = self.experience
        r["karma"] = self.karma
        r["kills"] = self.kills
        r["lifespan"] = self.lifespan
        r["rests"] = self.rests
        return json.dumps(r)

    def load(self, s):
        super(self.__class__, self).load(s)
        if type(s) == str:
            r = json.loads(s)
        elif type(s) == dict:
            r = s
        self.experience = r.get("experience", self.experience)
        self.karma = r.get("karma", self.karma)
        self.kills = r.get("kills", self.kills)
        self.lifespan = r.get("lifespan", self.lifespan)
        self.rests = r.get("rests", self.rests)
        self.recalculate_secondary_stats()

    def level_up(self):
        old_level = self.level
        while self.experience >= next_level_xp(self.level):
            self.level += 1
            self.recalculate_secondary_stats()
        if old_level == self.level:
            return False
        else:
            return True

    def character_record(self):
        s = "%s  Level %d\n" % (utils.color_text("purple", self.name), self.level)
        s += "Experience: %d/%d\n\n" % (self.experience, next_level_xp(self.level))
        s += utils.color_text("cyan", "- Statistics -\n")
        for stat in actors.BASE_STATS:
            s += "%22s %s\n" % (utils.color_text("yellow", stat.title())+":", self.stats[stat])
        s += "\n"
        for stat in ["HP", "Fatigue", "AP", "SP"]:
            lstat = stat.lower()
            s += "%s %d/%d  " % (stat, self.stats[lstat+"_cur"], self.stats[lstat+"_max"])
        s += "\n"
        # These should probably not be displayed. But show them for debug purposes
        s += "Karma: %d\n" % (self.karma,)
        s += "Kills: %d\n" % (self.kills,)
        s += "Times rested: %d\n" % (self.rests,)
        s += "Time in the Depths: %d\n" % (self.lifespan,)

        s += utils.color_text("cyan", "\n- Equipped items -\n")
        for slot in sorted(self.equipment):
            item = items.str_item(self.equipment[slot])
            s += "%11s %s\n" % (slot.title()+":", item)

        s += utils.color_text("cyan", "\n- Inventory -\n")
        for item in sorted(self.inventory):
            s += "%s\n" % (items.str_item(item),)
        return s


def next_level_xp(level):
    return 500*(level*(level+1))

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
    print "Used to determine your spell points."
    print utils.color_text("yellow", "Willpower")
    print "Used to determine your spell points."
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
