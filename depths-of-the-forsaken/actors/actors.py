import json

from items import items
from template import template
from utils import utils

BASE_STATS = [
    "toughness",
    "agility",
    "perception",
    "intelligence",
    "willpower",
    "charisma",
    "luck"
]

def load_actor(actor):
    new_actor = Actor("DEFAULT NAME")
    new_actor.load(actor)
    return new_actor

class Actor(object):
    def __init__(self, name, display_name=None, stats=None):
        self.name = name
        self.article = None
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
            "attack": {
                "ap": 8,
                "damage": [1, 3, 0],
                "desc": "Attack your oppnent with %s (%d-%d damage  %d reach)",
                "hit_desc": ["punches", "jabs", "kicks"],
                "crit_desc": ["pummels", "mauls"],
                "reach": 1
            },
            "approach": {
                "ap": 1,
                "desc": "Move one foot closer to your opponent"
            },
            "run": {
                "ap": 10,
                "desc": "Run twelve feet away from your opponent and attempt to flee"
            },
            "wait": {
                "ap": 0,
                "desc": "Recover fatigue equal to your remaining AP and end your turn"
            },
            "withdraw": {
                "ap": 1,
                "desc": "Move one foot away from your opponent"
            },
        }

        self.actions = self.base_actions

    def __str__(self):
        s = ""
        for stat in ["HP", "Fatigue", "AP", "SP"]:
            lstat = stat.lower()
            s += "%s %d/%d  " % (stat, self.stats[lstat+"_cur"], self.stats[lstat+"_max"])
        return s

    def __repr__(self):
        return json.dumps(self.pre_repr())

    def pre_repr(self):
        r = {}
        r["article"] = self.article
        r["base_actions"] = self.base_actions
        r["actions"] = self.actions
        r["display_name"] = self.display_name
        r["equipment"] = self.equipment
        r["inventory"] = self.inventory
        r["level"] = self.level
        r["name"] = self.name
        r["stats"] = self.stats
        return r

    def load(self, s):
        if type(s) == str:
            r = json.loads(s)
        elif type(s) == dict:
            r = s
        self.article = r.get("article", self.article)
        self.base_actions = r.get("base_actions", self.actions)
        self.actions = r.get("actions", self.actions)
        self.display_name = r.get("display_name", self.display_name)
        self.equipment = r.get("equipment", self.equipment)
        self.inventory = r.get("inventory", self.inventory)
        self.inventory.sort()
        self.level = r.get("level", self.level)
        self.name = r.get("name", self.name)
        self.stats.update(r.get("stats", self.stats))
        if r.get("recalc_secondary"):
            self.recalculate_secondary_stats()

    def _calculate_secondary_stats(self):
        self.stats["ap_max"] = 2*self.stats["agility"]
        self.stats["hp_max"] = self.stats["toughness"]
        self.stats["sp_max"] = self.stats["intelligence"]+self.stats["willpower"]
        self.stats["fatigue_max"] = 2*self.stats["toughness"]

        self.stats["ap_cur"] = self.stats["ap_max"]
        self.stats["hp_cur"] = self.stats["hp_max"]
        self.stats["sp_cur"] = self.stats["sp_max"]
        self.stats["fatigue_cur"] = self.stats["fatigue_max"]

    def recalculate_secondary_stats(self):
        old_ap = self.stats["ap_max"]
        self.stats["ap_max"] = 2*self.stats["agility"]
        if old_ap !=  self.stats["ap_max"]:
            self.stats["ap_cur"] += self.stats["ap_max"] - old_ap

        old_hp = self.stats["hp_max"]
        level_hp = (self.level-1)*((self.stats["toughness"]/3) + 2)
        self.stats["hp_max"] = self.stats["toughness"] + level_hp
        if old_hp !=  self.stats["hp_max"]:
            self.stats["hp_cur"] += self.stats["hp_max"] - old_hp

        old_sp = self.stats["sp_max"]
        level_sp = (self.level-1)*(self.stats["intelligence"]-10 + self.stats["willpower"]-10)
        if level_sp < 0:
            level_sp = 0
        self.stats["sp_max"] = self.stats["intelligence"] + self.stats["willpower"] + level_sp
        if old_sp !=  self.stats["sp_max"]:
            self.stats["sp_cur"] += self.stats["sp_max"] - old_sp

        old_fatigue = self.stats["fatigue_max"]
        level_fatigue  = (self.level-1)*(utils.stat_mod(self.stats["toughness"])+1)
        if level_fatigue < self.level-1:
            level_fatigue = self.level-1
        self.stats["fatigue_max"] = 2*self.stats["toughness"] + level_fatigue
        if old_fatigue !=  self.stats["fatigue_max"]:
            self.stats["fatigue_cur"] += self.stats["fatigue_max"] - old_fatigue

    def equip(self, item):
        for slot in item["slots"]:
            if self.equipment[slot] is not None:
                return ("You must unequip %s first." % (self.equipment[slot]["name"],), False)
        for slot in item["slots"]:
            self.equipment[slot] = item
        for action in item["actions"]:
            self.actions[action] = item["actions"][action]
        return ("You've equipped %s" % (utils.strart(item).title(),), True)

    # If for some reason the actor's equipment is screwed up and they have
    # multiple items equipped with overlapping slots, unequip all the
    # offending items.
    def _unequip(self, item):
        if item is None:
            return {}
        r = {item["name"]: item}
        for slot in item["slots"]:
            if self.equipment[slot] is not None:
                slot_item = self.equipment[slot]
                self.equipment[slot] = None
                r.update(self._unequip(slot_item))

        for action in item["actions"]:
            self.actions[action] = self.base_actions[action]
        return r

    def unequip(self, first_item):
        unequipped = self._unequip(first_item)
        for item in unequipped:
            self.inventory_add(unequipped[item])
        r = [utils.strart(unequipped[x]) for x in unequipped]
        s = "You've unequipped %s" % (", ".join(r),)
        return s

    def get_state(self):
        return str(self)

    def get_fuzzy_state(self):
        s = "%s appears to be " % (utils.strart(self).title(),)
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

    def inventory_add(self, item):
        self.inventory.append(item)
        self.inventory.sort()

    def inventory_remove(self, item_no):
        item = self.inventory[item_no]
        del self.inventory[item_no]
        return item

    def get_inventory_template(self):
        t = "<cyan>- Inventory -</cyan>\n"
        i = 0
        for item in self.inventory:
            t += "<action>%d</action>: %s\n" % (i, items.str_item(item))
            i += 1

        return t

    def get_inventory_str(self):
        return template.process(self.get_inventory_template())[0]

    def get_equipment_template(self):
        t = "<cyan>- Equipped Items -</cyan>\n"
        if self.equipment["main hand"] == self.equipment["off hand"]:
            t += "%11s: <action>%s</action>\n" % ("Both Hands", utils.get_name(self.equipment["main hand"]))
        else:
            t += "%11s: <action>%s</action>\n" % ("Main Hand", utils.get_name(self.equipment["main hand"]))
            t += "%11s: <action>%s</action>\n" % ("Off Hand", utils.get_name(self.equipment["off hand"]))

        for slot in ["head", "torso", "arms", "wrists", "hands", "legs", "feet"]:
            t += "%11s: <action>%s</action>\n" % (slot.title(), utils.get_name(self.equipment[slot]))

        return t

    def get_equipment_str(self):
        return template.process(self.get_equipment_template())[0]
