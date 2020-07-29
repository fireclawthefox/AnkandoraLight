class Field:
    def __init__(self, name, cost, special=""):
        self.connections = []

        self.name = name

        self.cost = cost

        self.special = special

        self.nodepath = None
