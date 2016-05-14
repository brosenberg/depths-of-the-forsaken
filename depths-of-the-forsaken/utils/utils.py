import json
import random

COLORS = {
    'grey':   '\033[90m',
    'red':    '\033[91m',
    'green':  '\033[92m',
    'yellow': '\033[93m',
    'blue':   '\033[94m',
    'purple': '\033[95m',
    'cyan':   '\033[96m',
    'white':  '\033[97m',
    'reset':  '\033[0m'
}

def color_text(color, text):
    if color in COLORS:
        return "%s%s%s" % (COLORS[color], text, COLORS['reset'])
    else:
        return text

def get_expected_input(expected, prompt=None):
    s = ""
    while s.lower() not in expected:
        if prompt:
            print prompt,
        try:
            s = raw_input("> ")
        except EOFError:
            pass
    return s

def get_yesno_input(prompt=None):
    s = ""
    if prompt:
        print prompt,
    else:
        print "%s or %s?" % (color_text('green', 'yes'), color_text('green', 'no'))
    try:
        s = raw_input("> ")
    except EOFError:
        return False
    if s.lower() == "y" or s.lower() == "yes":
        return True
    else:
        return False

def load_file(file_name):
    return json.loads(open(file_name).read())

# Returns (Hit, Crit)
def oppose(attacker, defender, attack_stat, defend_stat, attack_mod=0, defend_mod=0, crit_mod=0):
    attack_raw = roll(100)
    attack = attack_raw + stat_modp(attacker.stats[attack_stat]) + attacker.stats["luck"] + attack_mod
    defend = roll(100) + stat_modp(defender.stats[defend_stat]) + defender.stats["luck"] + defend_mod
    crit = True if attack_raw - crit_mod >= 95 else False
    if attack >= defend:
        return (True, crit)
    else:
        return (False, False)

def roll(*args):
    if len(args) == 0:
        return random.randint(1, 100)
    elif len(args) == 1:
        return random.randint(1, args[0])
    else:
        return random.randint(args[0], args[1])

def stat_mod(stat):
    return int((stat-10)/2)

def stat_modp(stat):
    return int(((stat-10)/2)*5)
