class BattleStats:
    def __init__(self, entryTuple=None):
        if entryTuple is None:
            self.isEnemy = 0
            self.name = ""
            self.atack = 0
            self.defense = 0
        else:
            self.isEnemy = entryTuple[0]
            self.name = entryTuple[1]
            self.atack = entryTuple[2]
            self.defense = entryTuple[3]
