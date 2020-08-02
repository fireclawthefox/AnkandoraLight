from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from panda3d.core import TextNode
from direct.interval.IntervalGlobal import LerpColorInterval


class DPiece(DistributedSmoothNode):
    def __init__(self, cr):
        print("INITIATED PIECE")
        self.modelName = ""
        DistributedSmoothNode.__init__(self, cr)

        self.setCacheable(1)
        self.model = None
        self.tagText = None
        self.nameTag = None

        self.acceptOnce("BoardAnimationDone", self.show)

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

    def show(self):
        if self.model is not None:
            if self.model.isHidden():
                self.model.show()
                self.model.setTransparency(1)
                LerpColorInterval(self.model, 1, self.model.getColor(), (0,0,0,0)).start()
        else:
            taskMgr.doMethodLater(0.5, self.show, "retryShowPiece", extraArgs=[])

        if self.nameTag is not None:
            if self.nameTag.isHidden():
                self.nameTag.setTransparency(1)
                LerpColorInterval(self.nameTag, 1, self.nameTag.getColor(), (0,0,0,0)).start()
        else:
            taskMgr.doMethodLater(0.5, self.show, "retryShowPiece", extraArgs=[])

    def setModel(self, modelName):
        if modelName == "": return
        self.modelName = modelName
        self.model = base.loader.loadModel(self.modelName)
        self.model.reparentTo(self)
        self.model.hide()
        print("RECHECK BOARD ANIMATION")
        base.messenger.send("checkBoardAnimationDone")

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
            self.nameTag.hide()
        else:
            self.tagText.setText(name)
