import random

COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'reset': '\033[0m'
}

def color_text(color, text):
    if color in COLORS:
        return "%s%s%s" % (COLORS[color], text, COLORS['reset'])
    else:
        return text

def oppose(attacker, defender, attack_stat, defend_stat):
    attack = roll(100) + stat_modp(attacker.stats[attack_stat]) + attacker.stats["luck"]
    defend = roll(100) + stat_modp(defender.stats[defend_stat]) + defender.stats["luck"]
    if attack > defend:
        return True
    else:
        return False

def roll(sides):
    return random.randint(1, sides)

def stat_mod(stat):
    return (stat-10)/2;

def stat_modp(stat):
    return ((stat-10)/2)*5;
