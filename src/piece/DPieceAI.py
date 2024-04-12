#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI


class DPieceAI(DistributedSmoothNodeAI):
    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)
        self.modelName = ""
        self.player = None

    def generate(self):
        DistributedSmoothNodeAI.generate(self)
        self.startPosHprBroadcast()

    def setModel(self, modelName):
        self.modelName = modelName

    def getModel(self):
        return self.modelName

    def getNameForNameTag(self):
        requesterId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(requesterId, "createNameTag", [self.player.name])
