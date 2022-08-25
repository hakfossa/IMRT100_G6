



class Intersection():

    def __init__(self, openings: list, parent: Intersection):
        self.openings = openings
        self.parent = parent
        self.direction_parent
        self.parent.add_child(self)
        self.children = []

        self.dead_end = False


    def add_child(self, child, direction):
        self.children.append(child)
        child.set_direction(direction)

    def set_direction(self, direction):

