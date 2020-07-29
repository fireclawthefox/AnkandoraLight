from direct.distributed.DistributedObject import DistributedObject
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight, DirectionalLight, CollisionNode, CollisionSphere, BitMask32
from board import BoardMap

class DBoard(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        print("CREATE BOARD")

        base.messenger.send("registerLoadEvent", ["loadBoardDone"])
        base.messenger.send("registerLoadEvent", ["loadTableDone"])

        self.modelLoadList = {"board":False, "table":False}

        self.lightSun = DirectionalLight('light_sun')
        self.lightSun.setColorTemperature(5300)
        self.lightSun.setShadowCaster(True, 2048, 2048)
        self.lightSunNP = render.attachNewNode(self.lightSun)
        self.lightSunNP.setPos(-2, 2, 2)
        self.lightSunNP.lookAt(2, -2, -0.5)

        '''
        lp = loader.loadModel("misc/Pointlight")
        lp.setPos(-2,2,2)
        lp.setScale(1)
        lp.reparentTo(render)


        lp = loader.loadModel("misc/Pointlight")
        lp.setPos(2,-2,-0.5)
        lp.setScale(1)
        lp.reparentTo(render)
        '''

        self.lightAmb = AmbientLight('light_ambient')
        #self.lightAmb.setColor((0.02, 0.02, 0.02, 1))
        self.lightAmb.setColor((0.1, 0.1, 0.1, 1))
        self.lightAmbNP = render.attachNewNode(self.lightAmb)


        self.accept("loadDone", self.loadDone)

        self.boardSceneLoadTask = loader.loadModel("assets/models/BoardScene.bam", callback=self.boardLoaded)
        self.tableLoadTask = loader.loadModel("assets/models/Table.bam", callback=self.tableLoaded)

        # render lights
        render.setLight(self.lightSunNP)
        render.setLight(self.lightAmbNP)

    def boardLoaded(self, boardScene):
        self.boardScene = boardScene
        self.boardFlip = Actor(self.boardScene.find("**/BoardArmature"), copy=False)
        self.boardFlip.reparentTo(self.boardScene)

        self.camFly = Actor(self.boardScene.find("**/CameraArmature"), copy=False)
        self.camFly.reparentTo(self.boardScene)

        bone = self.camFly.exposeJoint(None, "modelRoot", "CamHolder")
        base.camLens.setNear(0.01)
        base.camLens.setFar(100)
        base.camera.reparentTo(bone)
        base.camera.setP(-90)

        # render board
        self.boardSceneNP = self.boardScene.reparentTo(render)

        self.setupCollisions()

        base.messenger.send("loadBoardDone")
        base.messenger.send("loadDone", ["board"])

    def tableLoaded(self, table):
        self.table = table
        # render table
        self.tableNP = self.table.reparentTo(render)

        base.messenger.send("loadTableDone")
        base.messenger.send("loadDone", ["table"])

    def loadDone(self, model):
        self.modelLoadList[model] = True

        for key, value in self.modelLoadList.items():
            if value == False: return

        base.messenger.send("boardDone")

    def announceGenerate(self):
        base.messenger.send(self.cr.uniqueName("board_generated"), [self.doId])
        # call the base class method
        DistributedObject.announceGenerate(self)

    def disable(self):
        print("DISABLE BOARD")
        self.ignore("loadDone")
        self.boardScene.detachNode()
        self.table.detachNode()
        DistributedObject.disable(self)

    def delete(self):
        self.ignore("loadDone")
        self.boardFlip.cleanup()
        self.camFly.cleanup()
        self.boardFlip.removeNode()
        self.camFly.removeNode()
        #self.boardSceneNP.removeNode()
        self.table.removeNode()

        render.clearLight(self.lightSunNP)
        render.clearLight(self.lightAmbNP)
        self.lightSunNP.removeNode()
        self.lightAmbNP.removeNode()

        DistributedObject.delete(self)
        print("DELETED BOARD ROOM")

    def start(self):
        self.boardFlip.play("BoardFlipUp")
        self.camFly.play("CamFly")

    def setupCollisions(self):
        for field in BoardMap.gameMap:
            # create a sphere collision solid
            cs = CollisionSphere(0, 0, 0, 0.01)
            cn = CollisionNode("{}-collision".format(field.name))
            cn.addSolid(cs)
            fieldNP = self.boardScene.find("**/{}".format(field.name))
            field.collisionNP = fieldNP.attachNewNode(cn)
            field.collisionNP.setCollideMask(BitMask32(0x80))
            #field.collisionNP.show()
