from utils import utils

def _to_hit(attacker, defender):
    attack = utils.roll(100) + utils.stat_modp(attacker.stats["dex"])
    defend = utils.roll(100) + utils.stat_modp(defender.stats["dex"])
    if attack > defend:
        return True
    else:
        return False

def _damage(attacker, defender):
    damage = utils.roll(6) + utils.stat_mod(attacker.stats["str"])
    defender.stats["hp_cur"] -= damage
    return damage

def _attack(attacker, defender):
    if (_to_hit(attacker, defender)):
        damage = _damage(attacker, defender)
        return (True, damage)
    else:
        return (False, 0)

def attack(attacker, defender):
    (hit, damage) = _attack(attacker, defender)
    s = ""
    if hit:
        s = "%s hit %s for %d damage!" % (attacker.name, defender.name, damage)
    else:
        s = "%s missed %s!" % (attacker.name, defender.name)
    return (hit, damage, s)
