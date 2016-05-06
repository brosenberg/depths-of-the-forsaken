import random

def stat_mod(stat):
    return (stat-10)/2;

def stat_modp(stat):
    return ((stat-10)/2)*5;

def roll(sides):
    return random.randint(1, sides)
