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

    def show(self):
        if self.model is not None:
            self.model.show()
            self.model.setTransparency(1)
            LerpColorInterval(self.model, 1, self.model.getColor(), (0,0,0,0)).start()
        else:
            tasMgr.doMethodLater(0.5, self.show, "retryShowQuestCard")

    def setCard(self, cardName):
        if cardName == "": return

        print("SET CARD", cardName)

        modelName = "assets/models/questCards/QuestCard.bam"
        textureName = "assets/models/questCards/{}.png".format(cardName)
        cardTex = loader.loadTexture(textureName)

        self.model = base.loader.loadModel(modelName)
        self.model.setTexture(self.model.findTextureStage("0"), cardTex, 1)
        self.model.reparentTo(self)
        self.model.hide()

    def cardCollected(self):
        self.model.hide()
