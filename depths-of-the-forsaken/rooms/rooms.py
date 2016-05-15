class Room(object):
    def __init__(self):
        self.shape = "square"
        self.length = 31
        self.width = 31
        self.height = 12
        self.egress = []
        self.inhabitants = []
        self.desc = ""

    def __str__(self):
        if self.desc == "":
            s = "A %s room, %d by %d feet, with %d foot high ceilings." % (self.shape, self.length, self.width, self.height)
            for exit in self.egress:
                s += "\nThere's a %s on the %sern edge of the room." % (exit[1], exit[2])
            return s
        else:
            return desc

    def load(self, room):
        self.shape = room.get("shape", self.shape)
        self.shape = room.get("shape", self.shape)
        self.length = room.get("length", self.length)
        self.width = room.get("width", self.width)
        self.height = room.get("height", self.height)
        self.egress = room.get("egress", self.egress)
        self.inhabitants = room.get("inhabitants", self.inhabitants)
        self.desc = room.get("desc", self.desc)
        print self.egress
