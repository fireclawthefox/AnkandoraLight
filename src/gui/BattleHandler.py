#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG
from gui.Battle import GUI as Battle
from gui.BattleStats import GUI as BattleStats
from direct.interval.IntervalGlobal import Sequence, Func, Wait

class BattleHandler(DirectObject):
    def __init__(self, cr):
        self.battle = Battle()

        self.battle.frmBattle["frameSize"] = [base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop]
        self.battle.frmBattle["sortOrder"] = 980
        self.battle.frmBattle["state"] = DGG.NORMAL
        self.battle.frmBattle.setState()


        self.battle.frmRollInitiative["frameSize"] = [base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop]
        self.battle.frmRollInitiative["state"] = DGG.NORMAL
        self.battle.frmRollInitiative.setState()

        self.show = self.battle.show
        self.hide = self.battle.hide

        self.acceptOnce("rollInitiative", self.rolledInitiative)

        self.hide()

        self.playerStatsList = []
        self.enemyStatsList = []

    def setBattleBackground(self, imageName):
        self.battle.frmBattle["image"] = f"assets/battle/{imageName}.png"
        self.battle.frmBattle["image_scale"] = (1.56, 1, 1)

    def addBattleStats(self, stats):
        """Add the given stats values on the left or right side of the
        battlefield, dependend on whether they are players or enemies."""
        s = None
        if stats.isEnemy:
            i = len(self.playerStatsList)
            s = BattleStats(self.battle.frmEnemies)
            s.lblHealtPotions.hide()
            s.lblHealthPotionsValue.hide()
            s.frmStats.setZ((self.battle.frmEnemies["frameSize"][3]-0.15) - i*0.3)
            s.imgPlayer["image"] = f"assets/battle/enemies/{stats.imageName}.png"
            self.playerStatsList.append(s)
        else:
            i = len(self.enemyStatsList)
            s = BattleStats(self.battle.frmPlayers)
            s.frmStats.setZ((self.battle.frmPlayers["frameSize"][3]-0.15) - i*0.3)
            s.imgPlayer["image"] = f"assets/battle/players/{stats.imageName}.png"
            self.enemyStatsList.append(s)
        s.lblNameValue["text"] = stats.name
        s.lblAttackValue["text"] = str(stats.atack)
        s.lblDefenseValue["text"] = str(stats.defense)
        s.lblHealthPotionsValue["text"] = str(stats.healthPotions)
        s.lblHit.hide()

    def showHit(self, name, hitpoints):
        """Display the hitpoints dealt to the given player/enemy"""
        seq = None
        for s in self.playerStatsList:
            if s.lblNameValue["text"] == name:
                s.lblHit["text"] = str(hitpoints)
                Sequence(
                    Func(s.lblHit.show),
                    s.lblHit.scaleInterval(1.0, s.lblHit.getScale(), startScale=0),
                    Wait(1),
                    Func(s.lblHit.hide)).start()
                return
        for s in self.enemyStatsList:
            if s.lblNameValue["text"] == name:
                s.lblHit["text"] = str(hitpoints)
                Sequence(
                    Func(s.lblHit.show),
                    s.lblHit.scaleInterval(1.0, s.lblHit.getScale(), startScale=0),
                    Wait(1),
                    Func(s.lblHit.hide)).start()
                return

    def clearBattleStats(self):
        """Cleanup and destroy the battlefield"""
        # remove player stats
        for s in self.playerStatsList:
            s.destroy()
        self.playerStatsList = []

        # remove enemy stats
        for s in self.enemyStatsList:
            s.destroy()
        self.enemyStatsList = []

    def setActivePlayer(self, name):
        """Highlights the given player/enemy on the batlefield"""
        # check for player fighters
        for s in self.playerStatsList:
            if s.lblNameValue["text"] == name:
                # grow the active player
                s.frmStats.setScale(1.05)
                s.frmStats["frameColor"] = (1, 0.0, 0.0, 1)
            else:
                # shrink all others
                s.frmStats.setScale(1)
                s.frmStats["frameColor"] = (1, 1, 1, 1)

        # same for the enemy fighters
        for s in self.enemyStatsList:
            print("compare:")
            print(s.lblNameValue["text"])
            print(name)
            if s.lblNameValue["text"] == name:
                s.frmStats.setScale(1.05)
                s.frmStats["frameColor"] = (1, 0.0, 0.0, 1)
            else:
                s.frmStats.setScale(1)
                s.frmStats["frameColor"] = (1, 1, 1, 1)

    def enableAttackButton(self):
        self.battle.btnAttack["state"] = DGG.NORMAL
        self.battle.btnAttack.setState()

    def disableAttackButton(self):
        self.battle.btnAttack["state"] = DGG.DISABLED
        self.battle.btnAttack.setState()

    def rolledInitiative(self):
        self.battle.frmRollInitiative.hide()

    def destroy(self):
        self.ignoreAll()
        self.battle.destroy()
        del self.battle

    def setSpectate(self):
        self.battle.frmRollInitiative.hide()
        self.battle.btnAttack.hide()
