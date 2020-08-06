from direct.distributed.DistributedObject import DistributedObject
from panda3d.core import CollisionNode, CollisionRay, BitMask32, CollisionHandlerQueue

class DPlayer(DistributedObject):
    def __init__(self, cr):
        print("INITIALIZED PLAYER")
        DistributedObject.__init__(self, cr)
        self.name = "Player"
        self.piece = None

        self.pickerQueue = CollisionHandlerQueue()
        self.pickerRay = CollisionRay()
        pickerNode = CollisionNode('mouseRay')
        pickerNode.setFromCollideMask(BitMask32(0x80))
        pickerNode.addSolid(self.pickerRay)
        pickerNP = base.camera.attachNewNode(pickerNode)
        base.cTrav.addCollider(pickerNP, self.pickerQueue)

        self.accept("mouse1", self.checkClick)

    def d_getName(self):
        self.sendUpdate("requestName")

    def setName(self, newName):
        self.name = newName
        #self.piece.createNameTag(self.name)
        base.messenger.send(self.cr.uniqueName("setPlayerName"), [self.name])

    def setPiece(self, piece):
        self.piece = piece

    def checkClick(self):
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
