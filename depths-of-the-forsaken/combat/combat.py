import random

from actors import actors
from utils import utils


class Combat(object):
    def __init__(self, player, opponent, distance=1):
        self.player = player
        self.opponent = opponent
        self.distance = distance
        self.turn = 1
        if self._to_hit(self.player, self.opponent):
            self.initiative = [self.player, self.opponent]
        else:
            self.initiative = [self.opponent, self.player]
        self.combat_complete = False

    def _to_hit(self, attacker, defender):
        return utils.oppose(attacker, defender, "agility", "agility")

    def _damage(self, attacker, defender, damage_array):
        damage = utils.roll(damage_array[0], damage_array[1]) + damage_array[2] + utils.stat_mod(attacker.stats["toughness"])
        defender.stats["hp_cur"] -= damage
        if defender.stats["hp_cur"] < 1:
            self.combat_complete = True
        return damage

    def can_reach(self, attacker):
        if attacker.actions["attack"]["reach"] >= self.distance:
            return True
        else:
            return False

    # Returns (Hit, Damage, Crit)
    def _attack(self, attacker, defender, damage_array):
        (hit, crit) = self._to_hit(attacker, defender)
        if hit:
            damage = self._damage(attacker, defender, damage_array)
            if crit:
                damage += self._damage(attacker, defender, damage_array)
            return (True, damage, crit)
        else:
            return (False, 0, False)

    def attack(self, attacker, defender, action):
        if self.can_reach(attacker):
            (hit, damage, crit) = self._attack(attacker, defender, action["damage"])
            if crit:
                desc = random.choice(action["crit_desc"])
                s = "%s critically %s %s for %d damage!!!" % (attacker.display_name, desc, defender.display_name, damage)
            elif hit:
                desc = random.choice(action["hit_desc"])
                s = "%s %s %s for %d damage!" % (attacker.display_name, desc, defender.display_name, damage)
            else:
                s = "%s missed %s!" % (attacker.display_name, defender.display_name)
            return (hit, damage, s)
        else:
            attacker.stats["ap_cur"] += attacker.actions["attack"]["ap"]
            return (0, 0, "%s is too far away to hit %s!" % (attacker.display_name, defender.display_name))

    # Returns ("String describing the action", Whether the action could be completed)
    def do_action(self, attacker, defender, action_type, action):
        if action_type == "wait":
            if attacker.stats["fatigue_cur"] < attacker.stats["fatigue_max"]:
                attacker.stats["fatigue_cur"] += attacker.stats["ap_cur"]
                if attacker.stats["fatigue_cur"] > attacker.stats["fatigue_max"]:
                    attacker.stats["fatigue_cur"] = attacker.stats["fatigue_max"]
            attacker.stats["ap_cur"] = 0
            return ("%s waits." % (attacker.display_name,), True)

        if attacker.stats["ap_cur"] < action["ap"]:
            return ("%s is out of actions." % (attacker.display_name,), False)
        attacker.stats["ap_cur"] -= action["ap"]

        if attacker.stats["fatigue_cur"] < 1:
            return ("%s is too tired and should wait." % (attacker.display_name,), False)

        if action_type == "attack":
            attacker.stats["fatigue_cur"] -= 1
            (hit, damage, s) = self.attack(attacker, defender, action)
            return (s, True)

        if action_type == "approach":
            if self.distance > 1:
                self.distance -= 1
                return ("%s moves closer." % (attacker.display_name,), True)
            else:
                return ("%s can't move any closer." % (attacker.display_name,), False)

        if action_type == "withdraw":
            self.distance += 1
            return ("%s withdraws a foot." % (attacker.display_name,), True)

        if action_type == "run":
            if self.distance < 20:
                self.distance += 12
                return ("%s attempts to run away!" % (attacker.display_name,), True)
            else:
                self.combat_complete = True
                return ("%s has run away!" % (attacker.display_name,), True)

        raise Exception("Unknown action: %s" % (action,))

    def print_player_status(self):
        print self.player.get_state()
        ## ONE DAY... THIS
        #if self.player.perks.get("awareness"):
        #    print self.opponent.get_state()
        print self.opponent.get_fuzzy_state()
        if self.distance == 1:
            print "You are 1 foot from the %s." % (self.opponent.display_name,)
        else:
            print "You are %d feet from the %s." % (self.distance, self.opponent.display_name)

    def player_turn(self):
        while self.player.stats["ap_cur"] > 0 and not self.combat_complete:
            self.print_player_status()
            prompt = "Which action will you perform?\n"
            for action in sorted(self.player.actions):
                action_text = "%s:" % (utils.color_text('green', action),)
                desc = self.player.base_actions[action]["desc"]
                if action == "attack":
                    damage = self.player.actions[action]["damage"]
                    weapon_name = "bare fists"
                    if self.player.equipment.get("main hand"):
                        weapon_name = self.player.equipment["main hand"]["name"]
                    min_dmg = damage[0]+damage[2]
                    max_dmg = (damage[0]*damage[1])+damage[2]
                    desc = desc % (weapon_name, min_dmg, max_dmg, self.player.actions[action]["reach"])
                prompt += "\t%8s %2d AP\n" % (action_text, self.player.actions[action]["ap"])
                prompt += "\t  %s\n" % (desc,)
            player_action = utils.get_expected_input(self.player.actions, prompt)
            (action_output, _) = self.do_action(self.player, self.opponent,  player_action, self.player.actions[player_action])
            print utils.color_text('yellow', action_output)
        self.player.stats["ap_cur"] = self.player.stats["ap_max"]

    def opponent_turn(self):
        action_success = True
        while self.opponent.stats["ap_cur"] > 0 and not self.combat_complete:
            action_output = ""
            action = "wait"

            if self.distance > 1:
                action = "approach"
            elif self.opponent.stats["ap_cur"] >= self.opponent.actions["attack"]["ap"]:
                action = "attack"

            if not action_success:
                action = "wait"
            (action_output, action_succes) = self.do_action(self.opponent, self.player, action, self.opponent.actions[action])
            print utils.color_text('red', action_output)
        self.opponent.stats["ap_cur"] = self.opponent.stats["ap_max"]

    def main_loop(self):
        print "%s goes first!" % (self.initiative[0].display_name,)
        while not self.combat_complete:
            print utils.color_text('cyan', "Turn %d  %s" % (self.turn, "-"*20))

            for combatant in self.initiative:
                if combatant is self.player:
                    self.player_turn()
                elif combatant is self.opponent:
                    self.opponent_turn()

            self.turn += 1

        if self.player.stats["hp_cur"] < 1:
            print utils.color_text("purple", "%s has been slain." % (self.player.display_name,))
        if self.opponent.stats["hp_cur"] < 1:
            print utils.color_text("purple", "%s has been slain." % (self.opponent.display_name,))
            self.player.lifespan += self.turn
            self.player.kills += 1
            self.player.experience += 50*self.opponent.level
