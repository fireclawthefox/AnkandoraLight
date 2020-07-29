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
        print("SET MODEL SERVER TO:", modelName)
        self.modelName = modelName

    def getModel(self):
        print("GET MODEL SERVER:", self.modelName)
        return self.modelName

    def getNameForNameTag(self):
        requesterId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(requesterId, "createNameTag", [self.player.name])
