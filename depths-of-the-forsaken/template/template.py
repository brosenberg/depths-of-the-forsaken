import re

from utils import utils

RESET = utils.COLORS['reset']
ACTION_COLOR = utils.COLORS['green']
DESC_COLOR = utils.COLORS['grey']
QUOTE_COLOR = utils.COLORS['yellow']

def process(t):
    tags = {
        "action": ACTION_COLOR,
        "desc": DESC_COLOR,
        "quote": QUOTE_COLOR,
    }
    for color in utils.COLORS:
        tags[color] = utils.COLORS[color]
    found_tags = {}
    for tag in tags:
        find = r'<%s>(.*?)</%s>' % (tag, tag)
        repl = r'%s\1%s' % (tags[tag], RESET)
        found_tags[tag] = [x for x in list(set(re.findall(find, t))) if x != ""]

        t = re.sub(find, repl, t)
    return (t, found_tags)
