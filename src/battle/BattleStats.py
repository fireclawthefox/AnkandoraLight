#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class BattleStats:
    """Data storage for battle statistics which will be sent over the network"""
    def __init__(self, entryTuple=None):
        if entryTuple is None:
            self.isEnemy = 0
            self.name = ""
            self.atack = 0
            self.defense = 0
            self.healthPotions = 0
        else:
            self.isEnemy = entryTuple[0]
            self.name = entryTuple[1]
            self.atack = entryTuple[2]
            self.defense = entryTuple[3]
            self.healthPotions = entryTuple[4]
