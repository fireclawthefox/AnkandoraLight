#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedNode import DistributedNode
from panda3d.core import TextureStage
from direct.interval.IntervalGlobal import LerpColorInterval

class DQuestCard(DistributedNode):
    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        self.model = None
        self.acceptOnce("BoardAnimationDone", self.show)

    def announceGenerate(self):
        DistributedNode.announceGenerate(self)
        self.reparentTo(render)

    def delete(self):
        """Cleanup just before the object gets deleted"""
        self.ignoreAll()
        if self.model is not None:
            self.model.removeNode
        DistributedNode.delete(self)

    def show(self):
        """Fade in the card model if it is already set otherwise wait until it's
        ready to be shown"""
        if self.model is not None:
            self.model.show()
            self.model.setTransparency(1)
            LerpColorInterval(self.model, 1, self.model.getColor(), (0,0,0,0)).start()
        else:
            tasMgr.doMethodLater(0.5, self.show, "retryShowQuestCard")

    def setCard(self, cardName):
        """Load the card model and texture"""
        if cardName == "": return

        modelName = "assets/models/questCards/QuestCard.bam"
        textureName = "assets/models/questCards/{}.png".format(cardName)
        cardTex = loader.loadTexture(textureName)

        self.model = base.loader.loadModel(modelName)
        self.model.setTexture(self.model.findTextureStage("0"), cardTex, 1)
        self.model.reparentTo(self)
        self.model.hide()

    def cardCollected(self):
        """Set the card to be collected. Simply hides the cards model"""
        self.model.hide()
