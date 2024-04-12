#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedObject import DistributedObject
from panda3d.core import CollisionNode, CollisionRay, BitMask32, CollisionHandlerQueue
from gui.DirectTooltip import DirectTooltip

class DPlayer(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.name = "Player"
        self.piece = None

        self.pickerQueue = CollisionHandlerQueue()
        self.pickerRay = CollisionRay()
        pickerNode = CollisionNode('mouseRay')
        pickerNode.setFromCollideMask(BitMask32(0x80))
        pickerNode.addSolid(self.pickerRay)
        self.pickerNP = base.camera.attachNewNode(pickerNode)
        base.cTrav.addCollider(self.pickerNP, self.pickerQueue)

        self.pathCostTooltip = DirectTooltip(
            scale=0.05,
            pad=(0.02, 0.02),
            frameColor=(0,0,0,0.5),
            text_fg=(1,1,1,1))

        self.accept("mouse1", self.checkClick)
        base.taskMgr.doMethodLater(1, self.checkHoverPathCost, "pathCostOnHoverCheck")

    def delete(self):
        """Cleanup just before the object gets deleted"""
        self.ignoreAll()
        base.taskMgr.remove("pathCostOnHoverCheck")
        base.cTrav.removeCollider(self.pickerNP)
        self.pickerNP.removeNode()

        if self.piece is not None:
            self.piece.sendDeleteMsg()

        DistributedObject.delete(self)

    def d_getName(self):
        self.sendUpdate("requestName")

    def setName(self, newName):
        self.name = newName
        base.messenger.send(self.cr.uniqueName("setPlayerName"), [self.name])

    def setPiece(self, piece):
        self.piece = piece

    def checkHoverPathCost(self, task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mpos.x, mpos.y)

            base.cTrav.traverse(render)
            if self.pickerQueue.getNumEntries() > 0:
                self.pickerQueue.sortEntries()
                pickedObj = self.pickerQueue.getEntry(0).getIntoNodePath()
                fieldName = pickedObj.getParent().getName()
                self.sendUpdate("requestPathCost", [fieldName])
            else:
                self.pathCostTooltip.hide()
        else:
            self.pathCostTooltip.hide()
        return task.again

    def doSetPathCost(self, cost):
        self.pathCostTooltip.show(f"Cost: {cost}")

    def checkClick(self):
        """Check if the player has clicked on a field and send a request to move
        to it to the server."""
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mpos.x, mpos.y)

            base.cTrav.traverse(render)
            if self.pickerQueue.getNumEntries() > 0:
                self.pickerQueue.sortEntries()
                pickedObj = self.pickerQueue.getEntry(0).getIntoNodePath()
                fieldName = pickedObj.getParent().getName()
                base.messenger.send("requestMoveToField", [fieldName])

    def d_updateInventory(self):
        self.sendUpdate("updateInventory")

    def doUpdateInventory(self, level, inventoryDir):
        base.messenger.send("updateInventory", [level, inventoryDir])

    def doUpdatePotions(self, numPotions):
        base.messenger.send("updateHealthPotions", [numPotions])
