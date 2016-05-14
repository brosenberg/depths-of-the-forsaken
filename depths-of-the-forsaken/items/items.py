from utils import utils

def str_item(item):
    if item is None:
        return ""
    elif item["type"] == "weapon":
        attack = item["actions"]["attack"]
        min_dmg = attack["damage"][0] + attack["damage"][2]
        max_dmg = attack["damage"][1] + attack["damage"][2]
        s =  "("
        s += "%d - %d damage  " % (min_dmg, max_dmg)
        s += "%d AP  %d reach" % (attack["ap"], attack["reach"])
        s += ")"
        s = "%s %s" % (item["name"], utils.color_text("grey", s))
        return s
    else:
        return item["name"]
