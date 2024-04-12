#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedObject import DistributedObject
from gui.BattleHandler import BattleHandler
from gui.BattleOverHandler import BattleOverHandler
from battle.BattleStats import BattleStats

class DBattle(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.battleHandler = BattleHandler(self.cr)

    def announceGenerate(self):
        self.battleHandler.show()
        self.acceptOnce("rollInitiative", self.d_rollInitiative)
        self.sendUpdate("isSpectating")
        # call the base class method
        DistributedObject.announceGenerate(self)

    def delete(self):
        self.ignoreAll()
        self.battleHandler.destroy()
        DistributedObject.delete(self)

    def doSpectate(self):
        self.battleHandler.setSpectate()

    def initializeBattlefield(self, imageName):
        self.battleHandler.setBattleBackground(imageName)

    def d_rollInitiative(self):
        base.messenger.send("playSFXDice")
        self.sendUpdate("rollInitiative")

    def d_attack(self):
        base.messenger.send("playSFXDice")
        self.sendUpdate("playerAttack")

    def startBattle(self):
        pass

    def updateBattleStats(self, activePlayerName, battleStatsList):
        self.battleHandler.clearBattleStats()
        for entry in battleStatsList:
            stats = BattleStats(entry)
            self.battleHandler.addBattleStats(stats)
        self.battleHandler.setActivePlayer(activePlayerName)

    def startRound(self):
        self.accept("attack", self.d_attack)
        self.battleHandler.enableAttackButton()

    def endRound(self):
        self.ignore("attack")
        self.battleHandler.disableAttackButton()

    def rolledInitiativeFailed(self):
        # probably ignore for now
        pass

    def rolledInitiative(self, roll):
        # wait for other players to roll and official start of battle
        pass

    def showHit(self, name, hitpoints):
        self.battleHandler.showHit(name, hitpoints)

    def gotDefeated(self, lostAllLifes, healthPotionsLeft):
        # check if we lost the battle or got some healing potions left which we
        # should refresh the gui with now
        base.messenger.send("updateHealthPotions", [healthPotionsLeft])

    def attackFailed(self):
        # probably ignore for now
        pass

    def enemyDefeated(self):
        pass

    def endBattle(self, wonBattle):
        boh = BattleOverHandler()
        if wonBattle == 1:
            boh.show("You won")
        else:
            boh.show("You lost\nReturn to the start field...")

        self.battleHandler.hide()
