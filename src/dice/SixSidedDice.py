#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.directnotify import DirectNotifyGlobal
#from direct.showbase import RandomNumGen
import random

class SixSidedDice:
    notify = DirectNotifyGlobal.directNotify.newCategory('SixSidedDice')

    def __init__(self):
        random.seed()

    def roll(self):
        """Returns a random number in the range of 1 to 6"""
        return 6#random.randint(1, 6)

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
