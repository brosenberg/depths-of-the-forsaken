BASE_STATS = ["str", "dex", "con", "wis", "int", "cha"]

class Actor(object):
    def __init__(self, name, display_name=None):
        self.name = name
        if display_name:
            self.display_name = display_name
        else:
            self.display_name = name

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

        self.weapon = None
        self.armor = None

        self.actions = {
            "attack": 8,
            "move": 1,
            "run": 10,
            "wait": 0
        }

    def __str__(self):
        s = "%s (level %d)\n" % (self.name, self.level)
        for stat in BASE_STATS:
            s += "%s %d  " % (stat, self.stats[stat])
        s += "\n"
        s += "Action Points: %d/%d\n" % (self.stats["ap_cur"], self.stats["ap_max"])
        s += "Hit Points:    %d/%d\n" % (self.stats["hp_cur"], self.stats["hp_max"])
        s += "Fatigue:       %d/%d\n" % (self.stats["fatigue_cur"], self.stats["fatigue_max"])
        s += "Spell Points:  %d/%d\n" % (self.stats["sp_cur"], self.stats["sp_max"])
        s += "\nWeapon: %s\nArmor: %s\n" % (self.weapon, self.armor)
        return s

    def get_state(self):
        s = "%s: %d/%d HP  %d/%d Fatigue  %d/%d AP  %d/%d SP" % (self.name,
            self.stats["hp_cur"], self.stats["hp_max"], self.stats["fatigue_cur"], self.stats["fatigue_max"], self.stats["ap_cur"], self.stats["ap_max"], self.stats["sp_cur"], self.stats["sp_max"])
        return s

    def get_fuzzy_state(self):
        s = "%s appears to be " % (self.display_name,)
        if self.stats["hp_cur"] == self.stats["hp_max"]:
            s += "unharmed"
        elif float(self.stats["hp_cur"])/float(self.stats["hp_max"]) > .80:
            s += "barely injured"
        elif float(self.stats["hp_cur"])/float(self.stats["hp_max"]) > .40:
            s += "injured"
        elif float(self.stats["hp_cur"])/float(self.stats["hp_max"]) > .20:
            s += "severely injured"
        else:
            s += "near death"
        return s
