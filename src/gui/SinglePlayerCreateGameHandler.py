#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from gui.SinglePlayerCreateGame import GUI as SinglePlayerCreateGame
from player.ClassManager import ClassManager

from globalData import RoomGlobals

class SinglePlayerCreateGameHandler(DirectObject, SinglePlayerCreateGame):
    def __init__(self):
        SinglePlayerCreateGame.__init__(self)

        self.cm = ClassManager()

        self.optionPlayerClass["items"] = RoomGlobals.ALL_PLAYERCLASSES_AS_NAMES
        self.optionPlayerClass["command"] = self.updateInfoBox
        self.optionPlayerClass.setItems()
        self.optionNumNPCs["items"] = ["0", "1","2","3"]
        self.optionGameType["items"] = RoomGlobals.ALL_GAMETYPES_AS_NAMES
        self.optionDifficulty["items"] = RoomGlobals.DIFFICULTIES_AS_NAMES

        self.optionPlayerClass.popupMarker.hide()
        self.optionNumNPCs.popupMarker.hide()
        self.optionGameType.popupMarker.hide()
        self.optionDifficulty.popupMarker.hide()

        self.accept("singlePlayerCreateGame_start", self.create)

        # update the info box at the start
        self.updateInfoBox(self.optionPlayerClass.get())

    def create(self):
        """Gather all information and pack them ready to be sent to the server"""
        name = "SingleplayerGame"
        aiPlayerCount = int(self.optionNumNPCs.get())
        numPlayers = aiPlayerCount + 1
        gameTypeStr = self.optionGameType.get()
        playerClassID = RoomGlobals.Name2PlayerClassID[self.optionPlayerClass.get()]
        gameType = 0
        if gameTypeStr == "Normal":
            gameType = RoomGlobals.GAMETYPE_NORMAL
        elif gameTypeStr == "Race":
            gameType = RoomGlobals.GAMETYPE_RACE
        difficulty = RoomGlobals.Name2Difficulty[self.optionDifficulty.get()]
        room = (name, numPlayers, 0, aiPlayerCount, difficulty, gameType, 0)
        base.messenger.send("singlePlayerCreateGame_createAndStart", [room, playerClassID])

    def destroy(self):
        self.ignoreAll()
        SinglePlayerCreateGame.destroy(self)

    def updateInfoBox(self, selection):
        img = "assets/charInfo/hero{}.png".format(selection)
        self.frmImageHero["image"] = img
        self.lblClassDescription["text"] = self.cm.getSpecialAbilityDescription(selection)
        self.lblHealthValue["text"] = str(self.cm.getDefense(selection, 1))
        self.lblAttackValue["text"] = str(self.cm.getAttack(selection, 1))
