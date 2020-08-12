#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedObject import DistributedObject
from panda3d.core import LPoint3
import random


from panda3d.core import KeyboardButton

class DRoomManager(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.roomZone = -1
        self.boardLoadDone = False
        self.manifested = False

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.cr.roomManager = self
        self.d_requestRoomList()
        base.messenger.send(self.cr.uniqueName("roomManager_ready"))

    def delete(self):
        print("DELETE DRoomManager")
        self.cr.roomManager = None
        self.roomZone = -1
        self.boardLoadDone = False
        self.manifested = False

    def setServerRoomList(self, roomList):
        # roomList is a list of tuples defining room data
        base.messenger.send("updateRoomList", [roomList])

    def d_requestJoin(self, roomID, playerClassID):
        self.acceptOnce(self.cr.uniqueName("board_generated"), self.boardGenerated)
        self.sendUpdate("requestJoin", [roomID, playerClassID])

    def d_requestLeave(self):
        self.sendUpdate("requestLeave", [self.roomZone, self.cr.localPlayerId])
        self.cr.sendDeleteMsg(self.cr.localPlayerId)
        self.cr.sendDeleteMsg(self.board.doId)
        self.cr.sendDeleteMsg(self.cr.localRoomId)

        player = self.cr.doId2do[self.cr.localPlayerId]
        player.delete()
        self.board.delete()
        room = self.cr.doId2do[self.cr.localRoomId]
        room.delete()

        interestZones = self.cr.interestZones
        interestZones.remove(self.roomZone)
        self.cr.setInterestZones(interestZones)

    def d_requestRoomList(self):
        self.sendUpdate("requestRoomList")

    def d_requestCreateRoom(self, roomInfo):
        self.sendUpdate("requestCreateRoom", [roomInfo])

    def joinFailed(self):
        base.messenger.send("roomManager_joinFailed")

    def joinSuccess(self, joinParams):
        """The server has granted us to join the requested room"""
        # parse our parameters
        i = 0
        roomZone = joinParams[i];i+=1
        roomId = joinParams[i];i+=1
        playerId = joinParams[i];i+=1
        playerPieceId = joinParams[i]

        # store the room zone
        self.roomZone = roomZone

        # update our interest zones
        interestZones = self.cr.interestZones
        self.cr.localPlayerId = playerId
        self.cr.localPlayerPieceId = playerPieceId
        self.cr.roomId = roomId
        interestZones.append(roomZone)
        self.cr.setInterestZones(interestZones)

        # wait for the DOs to be manifested
        self.cr.relatedObjectMgr.requestObjects(
            [
                playerId,
                playerPieceId,
                roomId
            ],
            allCallback = self.roomManifested)

        # wait for the board to be completed
        self.accept("boardDone", self.boardLoaded)

    def roomManifested(self, allObjects):
        """Function to be called as soon as all DOs have been created"""
        # update the player
        player = self.cr.doId2do[self.cr.localPlayerId]
        # set the players piece
        piece = self.cr.doId2do[self.cr.localPlayerPieceId]
        player.setPiece(piece)
        # update the players name
        player.d_getName()
        player.d_updateInventory()

        self.manifested = True

        self.checkStartRoom()

    def boardLoaded(self):
        self.boardLoadDone = True
        self.checkStartRoom()

    def checkStartRoom(self):
        if self.boardLoadDone and self.manifested:
            self.startRoom()

    def boardGenerated(self, boardDoID):
        self.board = self.cr.doId2do[boardDoID]

    def startRoom(self):
        self.board.start()
        base.messenger.send("roomManager_loaded")

        room = self.cr.doId2do[self.cr.roomId]
        room.sendUpdate("playerReady", [self.cr.localPlayerId])
