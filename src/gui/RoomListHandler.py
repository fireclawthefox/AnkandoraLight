#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath

from globalData import RoomGlobals
from gui.RoomList import GUI as RoomList
from gui.RoomEntry import GUI as RoomEntry
from gui.RoomCreate import GUI as RoomCreate
from gui.MultiplayerPlayerInfo import GUI as PlayerInfo

class RoomListHandler(DirectObject):
    def __init__(self):
        self.rooms = []
        self.holderNode = NodePath("RoomListHolder")
        self.holderNode.reparentTo(base.aspect2d)
        self.roomList = RoomList(self.holderNode)
        self.roomWizzard = RoomCreate(self.holderNode)
        self.roomWizzard.frmCreateRoom.hide()
        self.roomWizzard.optionNumPlayers["items"] = ["2","3","4"]
        self.roomWizzard.optionGameType["items"] = RoomGlobals.ALL_GAMETYPES_AS_NAMES
        self.roomWizzard.optionDifficulty["items"] = RoomGlobals.DIFFICULTIES_AS_NAMES

        self.playerInfo = PlayerInfo(self.holderNode)
        self.playerInfo.optionPlayerClass["items"] = RoomGlobals.ALL_PLAYERCLASSES_AS_NAMES
        self.playerInfo.hide()

        self.roomList.btnCreateRoom["command"] = self.showCreateRoom

    def destroy(self):
        self.ignoreAll()
        self.holderNode.removeNode()
        del self.holderNode
        self.roomList = None

    def showCreateRoom(self):
        if not self.roomWizzard.frmCreateRoom.isHidden(): return
        self.roomWizzard.frmCreateRoom.show()
        self.roomWizzard.entryRoomName.setFocus()
        self.accept("createRoom_Ok", self.createRoom)
        self.accept("createRoom_Cancel", self.hideCreateRoom)

    def hideCreateRoom(self):
        self.roomWizzard.frmCreateRoom.hide()
        self.ignore("createRoom_Ok")
        self.ignore("createRoom_Cancel")

    def showPlayerInfo(self, room):
        self.playerInfo.show()
        self.room = room
        self.accept("multiplayerPlayerInfo_start", self.PlayerInfoStart)
        self.accept("multiplayerPlayerInfo_cancel", self.hidePlayerInfo)

    def PlayerInfoStart(self):
        playerClassID = RoomGlobals.Name2PlayerClassID[self.playerInfo.optionPlayerClass.get()]
        self.requestRoomJoin(self.room, playerClassID)

    def hidePlayerInfo(self):
        self.playerInfo.hide()
        self.ignore("multiplayerPlayerInfo_start")
        self.ignore("multiplayerPlayerInfo_cancel")

    def createRoom(self):
        name = self.roomWizzard.entryRoomName.get()
        maxNumPlayers = int(self.roomWizzard.optionNumPlayers.get())
        numAIPlayers = 0
        gameTypeStr = self.roomWizzard.optionGameType.get()
        gameType = 0
        if gameTypeStr == "Normal":
            gameType = RoomGlobals.GAMETYPE_NORMAL
        elif gameTypeStr == "Race":
            gameType = RoomGlobals.GAMETYPE_RACE
        difficulty = RoomGlobals.Name2Difficulty[self.roomWizzard.optionDifficulty.get()]
        room = (name, maxNumPlayers, 0, numAIPlayers, difficulty, gameType, 0)
        base.messenger.send("roomList_createRoom", [room])
        self.hideCreateRoom()

    def update(self, rooms):
        # clear rooms
        for room in self.rooms:
            room.frmRoomEntry.destroy()
        self.rooms = []

        # add rooms
        z = 0
        for room in rooms:
            newRoomEntry = RoomEntry()
            newRoomEntry.lblRoomName["text"] = room[RoomGlobals.ROOM_NAME]
            newRoomEntry.lblPlayerCount["text"] = "{}/{}".format(room[RoomGlobals.ROOM_PLAYER_COUNT], room[RoomGlobals.ROOM_MAX_PLAYER_COUNT])
            roomType = "UNKNOWN"
            if room[RoomGlobals.ROOM_TYPE] == RoomGlobals.GAMETYPE_NORMAL:
                roomType = "Normal"
            elif room[RoomGlobals.ROOM_TYPE] == RoomGlobals.GAMETYPE_RACE:
                roomType = "Race"
            newRoomEntry.lblGameType["text"] = roomType
            newRoomEntry.lblDifficulty["text"] = RoomGlobals.Difficulty2Name[room[RoomGlobals.ROOM_DIFFICULTY]]

            newRoomEntry.btnJoin["command"] = self.showPlayerInfo
            newRoomEntry.btnJoin["extraArgs"] = [room]

            newRoomEntry.frmRoomEntry.setZ(z)
            newRoomEntry.frmRoomEntry.reparentTo(self.roomList.frmRoomList.getCanvas())
            z -= 0.1
            self.rooms.append(newRoomEntry)

        # Resize the frame canvas
        self.roomList.frmRoomList["canvasSize"] = (
            self.roomList.frmRoomList["canvasSize"][0], self.roomList.frmRoomList["canvasSize"][1]-0.2,
            -(len(self.rooms) * 0.1), 0)
        self.roomList.frmRoomList.setCanvasSize()

    def requestRoomJoin(self, room, playerClassID):
        base.messenger.send("roomList_enterRoom", [room, playerClassID])

    def show(self):
        self.holderNode.show()

    def hide(self):
        self.holderNode.hide()
