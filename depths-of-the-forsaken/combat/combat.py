from actors import actors
from utils import utils


class Combat(object):
    def __init__(self, player, opponent, distance=1):
        self.player = player
        self.opponent = opponent
        self.distance = distance
        self.player_turn = True if self._to_hit(self.player, self.opponent) else False
        self.combat_complete = False

    def _to_hit(self, attacker, defender):
        return utils.oppose(attacker, defender, "agility", "agility")

    def _damage(self, attacker, defender):
        damage = utils.roll(6) + utils.stat_mod(attacker.stats["toughness"])
        defender.stats["hp_cur"] -= damage
        if defender.stats["hp_cur"] < 1:
            self.combat_complete = True
        return damage

    def can_reach(self, attacker, defender):
        if attacker.equipment["main hand"] is None:
            if self.distance < 3:
                return True
            else:
                return False
        else:
            raise

    # Returns (Hit, Damage, Crit)
    def _attack(self, attacker, defender):
        (hit, crit) = self._to_hit(attacker, defender)
        if hit:
            damage = self._damage(attacker, defender)
            if crit:
                damage += self._damage(attacker, defender)
            return (True, damage, crit)
        else:
            return (False, 0, False)

    def attack(self, attacker, defender):
        if self.can_reach(attacker, defender):
            (hit, damage, crit) = self._attack(attacker, defender)
            if crit:
                s = "%s critically hit %s for %d damage!!!" % (attacker.display_name, defender.display_name, damage)
            elif hit:
                s = "%s hit %s for %d damage!" % (attacker.display_name, defender.display_name, damage)
            else:
                s = "%s missed %s!" % (attacker.display_name, defender.display_name)
            return (hit, damage, s)
        else:
            attacker.stats["ap_cur"] += attacker.actions["attack"]
            return (0, 0, "%s is too far away to hit %s!" % (attacker.display_name, defender.display_name))

    # Returns ("String describing the action", Whether the action could be completed)
    def do_action(self, attacker, defender, action):
        if action == "wait":
            if attacker.stats["fatigue_cur"] < attacker.stats["fatigue_max"]:
                attacker.stats["fatigue_cur"] += attacker.stats["ap_cur"]
                if attacker.stats["fatigue_cur"] > attacker.stats["fatigue_max"]:
                    attacker.stats["fatigue_cur"] = attacker.stats["fatigue_max"]
            attacker.stats["ap_cur"] = 0
            return ("%s waits." % (attacker.display_name,), True)

        if attacker.stats["ap_cur"] < attacker.actions[action]:
            return ("%s is out of actions." % (attacker.display_name,), False)
        attacker.stats["ap_cur"] -= attacker.actions[action]

        if attacker.stats["fatigue_cur"] < 1:
            return ("%s is too tired and should wait." % (attacker.display_name,), False)

        if action == "attack":
            attacker.stats["fatigue_cur"] -= 1
            (hit, damage, s) = self.attack(attacker, defender)
            return (s, True)

        if action == "approach":
            if self.distance > 1:
                self.distance -= 1
                return ("%s moves closer." % (attacker.display_name,), True)
            else:
                return ("%s can't move any closer." % (attacker.display_name,), False)

        if action == "run":
            if self.distance < 20:
                self.distance += 12
                return ("%s attempts to run away!" % (attacker.display_name,), True)
            else:
                self.combat_complete = True
                return ("%s has run away!" % (attacker.display_name,), True)

        raise Exception("Unknown action: %s" % (action,))

    def print_player_status(self):
        print self.player.get_state()
        print self.opponent.get_fuzzy_state()
        if self.distance == 1:
            print "You are 1 foot from the %s." % (self.opponent.display_name,)
        else:
            print "You are %d feet from the %s." % (self.distance, self.opponent.display_name)

    def main_loop(self):
        turn = 2
        while not self.combat_complete:

            if turn%2 == 0:
                print utils.color_text('cyan', "Turn %d  %s" % (turn/2, "-"*20))

            if self.player_turn:
                while self.player.stats["ap_cur"] > 0 and not self.combat_complete:
                    self.print_player_status()
                    prompt = "Which action will you perform?\n"
                    for action in sorted(self.player.actions):
                        action_text = "%s:" % (utils.color_text('green', action),)
                        prompt += "\t%8s %2d AP\n" % (action_text, self.player.actions[action])
                    player_action = utils.get_expected_input(self.player.actions, prompt)
                    (action_output, _) = self.do_action(self.player, self.opponent, player_action)
                    print utils.color_text('yellow', action_output)
                self.player.stats["ap_cur"] = self.player.stats["ap_max"]

            else:
                action_success = True
                while self.opponent.stats["ap_cur"] > 0 and not self.combat_complete:
                    action_output = ""
                    action = "wait"

                    if self.distance > 1:
                        action = "approach"
                    elif self.opponent.stats["ap_cur"] >= self.opponent.actions["attack"]:
                        action = "attack"

                    if not action_success:
                        action = "wait"
                    (action_output, action_succes) = self.do_action(self.opponent, self.player, action)
                    print utils.color_text('red', action_output)
                self.opponent.stats["ap_cur"] = self.opponent.stats["ap_max"]

            self.player_turn = not self.player_turn
            turn += 1

        self.player.lifespan += turn/2
        if self.player.stats["hp_cur"] < 1:
            print utils.color_text("purple", "%s has been slain." % (self.player.display_name,))
        if self.opponent.stats["hp_cur"] < 1:
            print utils.color_text("purple", "%s has been slain." % (self.opponent.display_name,))
            self.player.kills += 1
            self.player.experience += 50*self.opponent.level
