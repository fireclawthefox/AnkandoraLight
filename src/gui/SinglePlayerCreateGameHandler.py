#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from gui.SinglePlayerCreateGame import GUI as SinglePlayerCreateGame

from globalData import RoomGlobals

class SinglePlayerCreateGameHandler(DirectObject, SinglePlayerCreateGame):
    def __init__(self):
        SinglePlayerCreateGame.__init__(self)
        self.optionPlayerClass["items"] = RoomGlobals.ALL_PLAYERCLASSES_AS_NAMES
        self.optionNumNPCs["items"] = ["0", "1","2","3"]
        self.optionGameType["items"] = RoomGlobals.ALL_GAMETYPES_AS_NAMES

        self.accept("singlePlayerCreateGame_start", self.create)

    def create(self):
        """Gather all information and pack them ready to be sent to the server"""
        name = "SingleplayerGame"
        numPlayers = 1
        aiPlayerCount = int(self.optionNumNPCs.get())
        gameTypeStr = self.optionGameType.get()
        playerClassID = RoomGlobals.Name2PlayerClassID[self.optionPlayerClass.get()]
        gameType = 0
        if gameTypeStr == "Normal":
            gameType = RoomGlobals.GAMETYPE_NORMAL
        elif gameTypeStr == "Race":
            gameType = RoomGlobals.GAMETYPE_RACE
        difficulty = 0
        room = (name, numPlayers, 0, aiPlayerCount, difficulty, gameType, 0)
        base.messenger.send("singlePlayerCreateGame_createAndStart", [room, playerClassID])

    def destroy(self):
        self.ignoreAll()
        SinglePlayerCreateGame.destroy(self)
