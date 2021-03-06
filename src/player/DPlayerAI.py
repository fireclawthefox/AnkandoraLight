#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import random

from direct.distributed.DistributedObjectAI import DistributedObjectAI

from piece.DPieceAI import DPieceAI
from player.ClassManager import ClassManager


class DPlayerAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.name = ""
        self.avId = -1
        self.currentField = None
        self.startField = None
        self.piece = None
        self.playerClassID = -1
        self.playerClassType = "Unknown"
        self.level = 1
        self.numHealPotions = 3
        self.jitter_max = 0.002
        self.jitter_rotation_max = 45

        self.cm = ClassManager()

    def delete(self):
        """Cleanup just before the object gets deleted"""
        if self.piece is not None:
            self.air.sendDeleteMsg(self.piece.doId)

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def requestName(self):
        """Roundtrip to set the name of this Player on the client"""
        requesterId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(requesterId, "setName", [self.name])

    def startTurn(self):
        """ Start this players turn """
        base.messenger.send("startTurn", [])

    def resetToStartField(self):
        """Reset the player to its own start field and set the health potions
        back to the maximum"""
        self.moveTo(self.startField, 0, 0)
        self.updatePotions(3)

    def updatePotions(self, numPotions):
        self.numHealPotions = numPotions
        self.sendUpdateToAvatarId(self.avId, "doUpdatePotions", [self.numHealPotions])

    def moveTo(self, field, shiftX, shiftY):
        """Move the piece to the given location"""
        self.currentField = field
        jitter_x = random.uniform(-self.jitter_max, self.jitter_max)
        jitter_y = random.uniform(-self.jitter_max, self.jitter_max)
        self.piece.d_setXY(field.nodepath.getX() + shiftX + jitter_x, field.nodepath.getY() + shiftY + jitter_y)
        h = random.uniform(-self.jitter_rotation_max, self.jitter_rotation_max)
        self.piece.d_setH(h)

    def getAttack(self):
        """Returns the attack strength of the players class"""
        return self.cm.getAttack(self.playerClassType, self.level)

    def getDefense(self):
        """Returns the defensive strength of the players class"""
        return self.cm.getDefense(self.playerClassType, self.level)

    def updateInventory(self):
        """Update the players inventory with the current level and class
        specific inventory path."""
        self.sendUpdateToAvatarId(self.avId, "doUpdateInventory", [self.level, self.cm.getInventoryDir(self.playerClassType)])

    def getSpecialAbility(self):
        """Returns the special ability definition for this players class"""
        return self.cm.getSpecialAbility(self.playerClassType)
