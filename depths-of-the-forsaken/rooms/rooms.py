class Room(object):
    def __init__(self):
        self.shape = "square"
        self.length = 30
        self.width = 30
        self.height = 10
        self.egress = []
        self.desc = ""

    def __str__(self):
        if self.desc = "":
            s = "A %s room, %d by %d feet, with %d foot high ceilings." % (self.shape, self.length, self.width, self.height)
            for exit in egress:
                s += "\nThere's a %s on the %sern edge of the room." % (exit[1], exit[2])
            return s
        else:
            return desc
