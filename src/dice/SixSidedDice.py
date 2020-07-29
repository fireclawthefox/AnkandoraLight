from direct.directnotify import DirectNotifyGlobal
#from direct.showbase import RandomNumGen
import random

class SixSidedDice:
    notify = DirectNotifyGlobal.directNotify.newCategory('SixSidedDice')

    def __init__(self):
        random.seed()

    def roll(self):
        return random.randint(1, 6)

    '''
    # The following code will produce reproducible random numbers

    def __init__(self, avId):
        self.avId = avId
        self.mainRNG = RandomNumGen.RandomNumGen(self.avId)
        seedVal = self.mainRNG.randint(0, (1 << 16) - 1)
        self.diceRNG = RandomNumGen.RandomNumGen(seedVal)

    def delete(self):
        del self.diceRNG

    def reSeed(self):
        seedVal = self.mainRNG.randint(0, (1 << 16) - 1)
        self.diceRNG = RandomNumGen.RandomNumGen(seedVal)

    def roll(self):
        return self.diceRNG.randint(1, 6)
    '''
