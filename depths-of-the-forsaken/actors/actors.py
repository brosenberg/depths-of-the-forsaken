import json

BASE_STATS = [
    "toughness",
    "agility",
    "perception",
    "intelligence",
    "willpower",
    "charisma",
    "luck"
]

class Actor(object):
    def __init__(self, name, display_name=None, stats=None):
        self.name = name
        if display_name:
            self.display_name = display_name
        else:
            self.display_name = name

        self.level = 1
        if stats is not None:
            for stat in BASE_STATS:
                if stat not in stats:
                    raise Exception("Stat '%s' undefined in actor!" % (stat,))
            self.stats = stats
        else:
            self.stats = {}
            for stat in BASE_STATS:
                self.stats[stat] = 10

        self._calculate_secondary_stats()

        self.equipment = {
            "arms": None,
            "feet": None,
            "hands": None,
            "head": None,
            "legs": None,
            "main hand": None,
            "off hand": None,
            "torso": None,
            "wrists": None
        }

        self.inventory = []

        self.base_actions = {
            "attack": 8,
            "approach": 1,
            "run": 10,
            "wait": 0,
            "withdraw": 1,
        }

        self.actions = self.base_actions

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

    def __repr__(self):
        return json.dumps(self.pre_repr())

    def pre_repr(self):
        r = {}
        r["actions"] = self.actions
        r["display_name"] = self.display_name
        r["equipment"] = self.equipment
        r["inventory"] = self.inventory
        r["level"] = self.level
        r["name"] = self.name
        r["stats"] = self.stats
        return r

    def _calculate_secondary_stats(self):
        self.stats["ap_max"] = 2*self.stats["agility"]
        self.stats["hp_max"] = self.stats["toughness"]
        self.stats["sp_max"] = 2*self.stats["intelligence"]
        self.stats["fatigue_max"] = 2*self.stats["toughness"]

        self.stats["ap_cur"] = self.stats["ap_max"]
        self.stats["hp_cur"] = self.stats["hp_max"]
        self.stats["sp_cur"] = self.stats["sp_max"]
        self.stats["fatigue_cur"] = self.stats["fatigue_max"]

    def get_state(self):
        s = "%s: HP %d/%d  Fatigue %d/%d  AP %d/%d  SP %d/%d" % (self.name,
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
        s += "."
        return s

    def load(self, s):
        r = json.loads(s)
        # TODO: This should set working defaults.
        self.actions = r.get("actions", {})
        self.display_name = r.get("display_name", "DEFAULT NAME")
        self.equipment = r.get("equipment", {})
        self.inventory = r.get("inventory", [])
        self.level = r.get("level", 1)
        self.name = r.get("name", "DEFAULT NAME")
        self.stats = r.get("stats", {})
