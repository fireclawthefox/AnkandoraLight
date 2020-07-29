from direct.distributed.DistributedNode import DistributedNode
from panda3d.core import TextureStage

class DQuestCard(DistributedNode):
    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        self.model = None

    def announceGenerate(self):
        DistributedNode.announceGenerate(self)
        self.reparentTo(render)

    def setCard(self, cardName):
        if cardName == "": return

        modelName = "assets/models/questCards/QuestCard.bam"
        textureName = "assets/models/questCards/{}.png".format(cardName)
        cardTex = loader.loadTexture(textureName)

        self.model = base.loader.loadModel(modelName)
        self.model.setTexture(self.model.findTextureStage("0"), cardTex, 1)
        self.model.reparentTo(self)

    def cardCollected(self):
        self.model.hide()
