import json

def load_game(pc, save_file):
    try:
        with open(save_file, 'r') as f:
            pc.load(f.read())
    except IOError:
        return False
    return True

def save_game(pc, save_file):
    try:
        with open(save_file, 'w') as f:
            f.write(repr(pc))
    except IOError:
        return False
    return True

def load_file(file_name):
    return json.loads(open(file_name).read())
