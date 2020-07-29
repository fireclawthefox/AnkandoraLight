from direct.distributed.DistributedObjectAI import DistributedObjectAI

from piece.DPieceAI import DPieceAI
from player.ClassManager import ClassManager


class DPlayerAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.name = ""
        self.avId = -1
        self.currentField = None
        self.piece = None
        self.playerClassID = -1
        self.playerClassType = "Unknown"
        self.level = 1
        self.numHealPotions = 3

        self.cm = ClassManager()

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def requestName(self):
        requesterId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(requesterId, "setName", [self.name])

    def startTurn(self):
        """ Start this players turn """
        print("START THIS PLAYERS TURN")
        base.messenger.send("startTurn", [])

    def moveTo(self, field, shiftX, shiftY):
        print("MOVE PLAYER")
        self.currentField = field
        print("TO:", field.nodepath.getPos())
        print("DISTANCE:", self.piece.getPos() - field.nodepath.getPos())
        #self.piece.setPos(field.nodepath.getPos())
        self.piece.d_setXY(field.nodepath.getX() + shiftX, field.nodepath.getY() + shiftY)

    def getAttack(self):
        print("GET ATTACK")
        return self.cm.getAttack(self.playerClassType, self.level)

    def getDefense(self):
        print("GET DEFENSE")
        return self.cm.getDefense(self.playerClassType, self.level)
