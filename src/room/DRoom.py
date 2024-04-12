#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedObject import DistributedObject
from direct.gui.DirectDialog import YesNoDialog

class DRoom(DistributedObject):
    """The Distributed Room is the topmost object of a game. In a room all
    players that play together, the board and the consensus of what should be
    played. It doesn't define finer game rules as these will be board specific
    and should be implemented in the DBoard"""

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.dlgStartFight = None

    def announceGenerate(self):
        self.cr.localRoomId = self.doId
        DistributedObject.announceGenerate(self)

        self.accept("requestMoveToField", self.d_requestMoveToField)

    def delete(self):
        self.ignoreAll()
        DistributedObject.delete(self)

    def startRoom(self):
        base.messenger.send("startRoom")

    def nextPlayer(self, playerName):
        base.messenger.send("setNextActivePlayerName", [playerName])

    def d_endTurn(self):
        self.sendUpdate("endTurn")

    def endTurn(self):
        """ End this players turn """
        base.messenger.send("endThisPlayerTurn", [])

    def startTurn(self):
        """ Start this players turn """
        base.messenger.send("startTurn", [])

    def d_rollDice(self):
        self.sendUpdate("rollDice")

    def rolledDice(self, roll):
        base.messenger.send("playSFXDice")
        base.messenger.send("rolledDice", [roll])

    def updateRolledDice(self, remainingRoll):
        base.messenger.send("rolledDice", [remainingRoll])

    def rolledDiceFailed(self):
        pass

    def d_requestMoveToField(self, fieldName):
        self.sendUpdate("requestMoveToField", [fieldName])

    def gameOver(self, winningPlayerName):
        msg = ""
        if winningPlayerName == "ALL":
            msg = "Congratulations\nYou Won!"
            base.messenger.send("playAudioWin")
        else:
            if winningPlayerName == self.cr.doId2do[self.cr.localPlayerId].name:
                msg = "Congratulations\nYou Won!".format(winningPlayerName)
                base.messenger.send("playAudioWin")
            else:
                msg = "Player\n{}\nwon!".format(winningPlayerName)
                base.messenger.send("playAudioLoose")
        base.messenger.send("gameOver", [msg])

    def canInitiateFight(self):
        if self.dlgStartFight is not None: return
        base.messenger.send("canInitiateFight")

        self.dlgStartFight = YesNoDialog(
            state='normal',
            text='Start Fight?',
            fadeScreen=True,
            command=self.doInitiateFight
        )

    def doInitiateFight(self, yes):
        if yes:
            self.d_initiateFight()
        self.dlgStartFight.cleanup()
        self.dlgStartFight = None

    def d_initiateFight(self):
        self.sendUpdate("initiateFight")

    def startBattle(self):
        pass

    def endBattle(self, won):
        print("Player won:", won)

    def spectateBattle(self):
        pass

    def endSpectateBattle(self):
        pass
