#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedObject import DistributedObject
from panda3d.core import CollisionNode, CollisionRay, BitMask32, CollisionHandlerQueue

class DBotPlayer(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.name = "Player"
        self.piece = None

    def announceGenerate(self):
        self.sendUpdate("requestName")

    def delete(self):
        """Cleanup just before the object gets deleted"""
        if self.piece is not None:
            self.piece.sendDeleteMsg()
        DistributedObject.delete(self)

    def setName(self, newName):
        self.name = newName
        base.messenger.send(self.cr.uniqueName("setPlayerName"), [self.name])

    def setPiece(self, piece):
        self.piece = piece
