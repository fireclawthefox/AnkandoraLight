#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedObject import DistributedObject
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight, DirectionalLight, CollisionNode, CollisionSphere, BitMask32
from board import BoardMap
from direct.interval.IntervalGlobal import Parallel, Sequence, Func

class DBoard(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.accept("checkBoardAnimationDone", self.checkBoardAnimationDone)

        base.messenger.send("registerLoadEvent", ["loadBoardDone"])
        base.messenger.send("registerLoadEvent", ["loadTableDone"])

        self.modelLoadList = {"board":False, "table":False}

        self.boardAnimation = None
        self.boardAnimationStarted = False

        self.lightSun = DirectionalLight('light_sun')
        self.lightSun.setColorTemperature(5300)
        self.lightSun.setShadowCaster(True, 2048, 2048)
        self.lightSunNP = render.attachNewNode(self.lightSun)
        self.lightSunNP.setPos(-2, 2, 2)
        self.lightSunNP.lookAt(2, -2, -0.5)

        self.lightAmb = AmbientLight('light_ambient')
        #self.lightAmb.setColor((0.1, 0.1, 0.1, 1))
        self.lightAmb.setColorTemperature(4500)
        c = self.lightAmb.getColor()
        self.lightAmb.setColor((c.x/2, c.y/2, c.z/2, 1))
        self.lightAmbNP = render.attachNewNode(self.lightAmb)

        self.accept("loadDone", self.loadDone)

        self.boardSceneLoadTask = loader.loadModel("assets/models/BoardScene.bam", callback=self.boardLoaded)
        self.tableLoadTask = loader.loadModel("assets/models/Table.bam", callback=self.tableLoaded)

        # render lights
        render.setLight(self.lightSunNP)
        render.setLight(self.lightAmbNP)

    def boardLoaded(self, boardScene):
        """Callback event for when the board model has fully loaded"""
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
        """Callback event for when the table model has fully loaded"""
        self.table = table
        # render table
        self.tableNP = self.table.reparentTo(render)

        base.messenger.send("loadTableDone")
        base.messenger.send("loadDone", ["table"])

    def loadDone(self, model):
        """Check function to determine if all models have loaded. If all models
        have been loaded, the boardDone event will be fired."""
        self.modelLoadList[model] = True

        for key, value in self.modelLoadList.items():
            if value == False: return

        self.ignore("loadDone")
        base.messenger.send("boardDone")

    def announceGenerate(self):
        # tell everyone interested, that the board DO has been generated
        base.messenger.send(self.cr.uniqueName("board_generated"), [self.doId])
        # call the base class method
        DistributedObject.announceGenerate(self)

    def disable(self):
        self.ignoreAll()
        self.boardScene.detachNode()
        self.table.detachNode()
        DistributedObject.disable(self)

    def delete(self):
        """Cleanup just before deletion of the DO"""
        # cleanup events
        self.ignoreAll()

        # cleanup models
        self.boardFlip.cleanup()
        self.camFly.cleanup()
        self.boardFlip.removeNode()
        self.camFly.removeNode()
        self.table.removeNode()

        self.boardAnimation = None

        # cleanup light
        try:
            render.clearLight(self.lightSunNP)
            render.clearLight(self.lightAmbNP)
        except:
            print("clear lights failed.")
        self.lightSunNP.removeNode()
        self.lightAmbNP.removeNode()

        # cleanup collisions
        for field in BoardMap.gameMap:
            field.collisionNP.removeNode()

        # cleanup other variables
        self.modelLoadList = {"board":False, "table":False}

        self.boardAnimation = None
        self.boardAnimationStarted = False

        DistributedObject.delete(self)

    def start(self):
        """Start the board animation"""
        taskMgr.step()
        self.boardAnimationStarted = True
        self.boardAnimation = Sequence(
            Parallel(
                self.boardFlip.actorInterval("BoardFlipUp"),
                self.camFly.actorInterval("CamFly")
            ),
            Func(base.messenger.send, "BoardAnimationDone")
        )
        self.boardAnimation.start()

    def checkBoardAnimationDone(self):
        """Check if the board animation has been stopped and resend the
        respective event if it has."""
        # check if we have an animation and it has actually been started once
        if self.boardAnimation is not None and self.boardAnimationStarted:
            # now check if the animation is done
            if self.boardAnimation.isStopped():
                # resend the event
                base.messenger.send("BoardAnimationDone")

    def setupCollisions(self):
        """Setup the collision solids for all fields.

        NOTE: This can be removed once blend2bam supports invisible collision
        model export"""
        for field in BoardMap.gameMap:
            # create a sphere collision solid
            cs = CollisionSphere(0, 0, 0, 0.01)
            cn = CollisionNode("{}-collision".format(field.name))
            cn.addSolid(cs)
            fieldNP = self.boardScene.find("**/{}".format(field.name))
            field.collisionNP = fieldNP.attachNewNode(cn)
            field.collisionNP.setCollideMask(BitMask32(0x80))

            # Debugging visualization
            #field.collisionNP.show()
