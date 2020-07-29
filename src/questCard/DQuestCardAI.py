from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DQuestCardAI(DistributedNodeAI):
    def __init__(self, cr, fieldName):
        DistributedNodeAI.__init__(self, cr)
        self.fieldName = fieldName

    def getCard(self):
        return self.fieldName

    def d_collect(self):
        self.sendUpdate("cardCollected")
