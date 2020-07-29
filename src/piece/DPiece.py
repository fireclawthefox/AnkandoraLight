from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from panda3d.core import TextNode


class DPiece(DistributedSmoothNode):
    def __init__(self, cr):
        print("INITIATED PIECE")
        self.modelName = ""
        DistributedSmoothNode.__init__(self, cr)

        self.setCacheable(1)
        self.model = None
        self.tagText = None
        self.nameTag = None

    def generate(self):
        DistributedSmoothNode.generate(self)
        self.activateSmoothing(True, False)
        self.startSmooth()

    def announceGenerate(self):
        DistributedSmoothNode.announceGenerate(self)
        self.reparentTo(render)
        self.d_getNameForNameTag()

    def disable(self):
        self.stopSmooth()
        DistributedSmoothNode.disable(self)

    def setModel(self, modelName):
        if modelName == "": return
        self.modelName = modelName
        self.model = base.loader.loadModel(self.modelName)
        self.model.reparentTo(self)

    def d_getNameForNameTag(self):
        # this will call the createNameTag function through the server as the
        # server has stored the name
        self.sendUpdate("getNameForNameTag")

    def createNameTag(self, name):
        if self.nameTag is None:
            self.tagText = TextNode("NameTag")
            self.tagText.setText(name)
            self.tagText.setTextColor(0,0,0,1)
            self.tagText.setAlign(TextNode.ACenter)
            self.nameTag = self.attachNewNode(self.tagText)
            self.nameTag.setBillboardAxis()
            self.nameTag.setZ(0.025)
            self.nameTag.setScale(0.007)
            self.nameTag.setShaderAuto(True)
        else:
            self.tagText.setText(name)
