BASE_STATS = ["str", "dex", "con", "wis", "int", "cha"]

class Actor(object):
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.stats = {}
        for stat in BASE_STATS:
            self.stats[stat] = 10
        self.stats["ap_max"] = 2*self.stats["dex"]
        self.stats["hp_max"] = self.stats["con"]
        self.stats["sp_max"] = 2*self.stats["int"]
        self.stats["fatigue_max"] = 2*self.stats["con"]

        self.stats["ap_cur"] = self.stats["ap_max"]
        self.stats["hp_cur"] = self.stats["hp_max"]
        self.stats["sp_cur"] = self.stats["sp_max"]
        self.stats["fatigue_cur"] = self.stats["fatigue_max"]

    def __str__(self):
        s = "%s (level %d)\n" % (self.name, self.level)
        for stat in BASE_STATS:
            s += "%s %d  " % (stat, self.stats[stat])
        s += "\n"
        s += "Action Points: %d/%d\n" % (self.stats["ap_cur"], self.stats["ap_max"])
        s += "Hit Points:    %d/%d\n" % (self.stats["hp_cur"], self.stats["hp_max"])
        s += "Fatigue:       %d/%d\n" % (self.stats["fatigue_cur"], self.stats["fatigue_max"])
        s += "Spell Points:  %d/%d\n" % (self.stats["sp_cur"], self.stats["sp_max"])
        return s
