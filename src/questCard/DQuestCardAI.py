#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DQuestCardAI(DistributedNodeAI):
    def __init__(self, cr, fieldName):
        DistributedNodeAI.__init__(self, cr)
        self.fieldName = fieldName

    def getCard(self):
        return self.fieldName

    def d_collect(self):
        self.sendUpdate("cardCollected")
