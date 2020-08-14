#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from enemy.EnemyAI import EnemyAI
from operator import itemgetter
from battle.BattleStats import BattleStats
from dice.SixSidedDice import SixSidedDice

from globalData.RoomGlobals import DIFFICULTY_EASY

class DBattleAI(DistributedObjectAI):
    def __init__(self, air, field, playersOnField, spectatorPlayers, difficulty):
        DistributedObjectAI.__init__(self, air)

        self.playersAttending = playersOnField.copy()
        self.playersOnField = playersOnField.copy()
        self.spectatorPlayers = spectatorPlayers
        self.readyPlayers = []
        self.playerInitiatives = {}
        self.activePlayerId = None
        self.fightOrder = []

        self.difficulty = difficulty

        self.afterShowHitDelay = 3

        self.dice = SixSidedDice()

        self.enemyAI = EnemyAI(field.special, self.difficulty)

        self.field = field

    def isSpectating(self):
        """Check if this player is spectating and set him in spectator mode"""
        playerId = self.air.getAvatarIdFromSender()
        for player in self.spectatorPlayers:
            if playerId == player.avId:
                self.sendUpdateToAvatarId(playerId, "doSpectate", [])
                return

    def rollInitiative(self, botAvId=None):
        """Roll the initiative for this player to decide where he lands in the
        fight order list"""
        playerId = botAvId
        if botAvId is None:
            playerId = self.air.getAvatarIdFromSender()

        if playerId in self.playerInitiatives.keys():
            if botAvId is None:
                self.sendUpdateToAvatarId(playerId, "rolledInitiativeFailed", [])
            return

        roll = self.dice.roll()
        self.playerInitiatives[playerId] = roll
        if botAvId is None:
            self.sendUpdateToAvatarId(playerId, "rolledInitiative", [roll])

        if len(self.playerInitiatives) == len(self.playersOnField):
            self.sortByInitiativesAndStart()

    def sortByInitiativesAndStart(self):
        """Sort all players and the enemy AI in the fight order list according
        to their initiative values"""
        enemyInit = self.enemyAI.getInitiative()
        for i in range(self.enemyAI.numEnemies):
            self.playerInitiatives[-1000-i] = enemyInit
        self.fightOrder = sorted(
            self.playerInitiatives.items(),
            key=itemgetter(1),
            reverse=True)
        self.d_startBattle()

    def d_startBattle(self):
        """Send start battle to all clients in this battle"""
        self.activePlayerId = self.fightOrder[0][0]

        self.sendUpdate("startBattle", [])

        # initially set the battle stats
        self.d_updateBattleStats()

        if self.activePlayerId > -1000:
            if self.activePlayerId > 0:
                # player starts turn
                self.sendUpdateToAvatarId(self.activePlayerId, "startRound", [])
            else:
                # Bot turn
                base.messenger.send(self.uniqueName("startRoundBot-{}".format(self.activePlayerId)))
        else:
            # enemy starts turn
            self.enemyAttack()

    def d_updateBattleStats(self):
        """Send a list of information about the battle to all players"""
        statslist = []

        activePlayerName = ""

        # check players
        for player in self.playersOnField:
            stats = BattleStats()
            stats.isEnemy = 0
            stats.name = player.name
            stats.atack = player.getAttack()
            stats.defense = player.getDefense()
            stats.healthPotions = player.numHealPotions
            statslist.append(stats)
            if self.fightOrder[0][0] == player.avId:
                activePlayerName = player.name

        # check enemies
        for enemyIdx in range(self.enemyAI.numEnemies):
            stats = BattleStats()
            stats.isEnemy = 1
            stats.name = "Enemy {}".format(enemyIdx+1)
            stats.atack = self.enemyAI.getAttack()
            stats.defense = self.enemyAI.getDefense()
            stats.healthPotions = 0
            statslist.append(stats)
            enemyID = -1000 * (enemyIdx+1)
            if self.fightOrder[0][0] == enemyID:
                activePlayerName = stats.name

        self.sendUpdate("updateBattleStats", [activePlayerName, statslist])

    def nextFighter(self):
        """Rotate the fight order and send an upate to the players"""
        # rotate the fight order
        self.fightOrder = self.fightOrder[1:] + self.fightOrder[:1]

        self.activePlayerId = self.fightOrder[0][0]

        # update the battle stats with the new order
        self.d_updateBattleStats()

        # check which turn it is
        if self.activePlayerId <= -1000:
            # all IDs less then or equal -1000 (e.g. -1000, -1001, etc), are enemy IDs
            # enemies turn
            base.taskMgr.doMethodLater(2, self.enemyAttack, "delayedEnemyAttackTask", extraArgs=[], appendTask=False)
        else:
            if self.activePlayerId < 0:
                base.messenger.send(self.uniqueName("startRoundBot-{}".format(self.activePlayerId)))
            else:
                # players turn
                self.sendUpdateToAvatarId(self.activePlayerId, "startRound", [])

    def enemyAttack(self):
        """Simulate an enemy attacking the players"""
        atk = self.enemyAI.rollAttack()

        """
        #TODO: Check difficulty:
        # Easy: Search for player with highest defense
        # Medium: Search for next player in Order
        # Hard: Search for player with lowest defense

        attackedPlayer = None
        # look for next player in order
        for fighterInfo in self.fightOrder:
            for player in self.playersOnField:
                if player.avId == fighterInfo[0]:
                    attackedPlayer = player
                    break
            if attackedPlayer is not None:
                break
        """

        # enemies attack all players at once according to original game rules
        for attackedPlayer in self.playersOnField:
            if attackedPlayer.getDefense() <= atk:
                #attacked player defeated
                if attackedPlayer.numHealPotions == 0:
                    # has no potions left
                    self.spectatorPlayers.append(attackedPlayer)
                    self.playersOnField.remove(attackedPlayer)
                    if attackedPlayer.avId > 0:
                        self.sendUpdateToAvatarId(attackedPlayer.avId, "gotDefeated", [True, 0])
                        self.sendUpdateToAvatarId(attackedPlayer.avId, "doSpectate", [])
                    for entry in self.fightOrder[:]:
                        if entry[0] == attackedPlayer.avId:
                            self.fightOrder.remove(entry)
                            break

                    if len(self.playersOnField) == 0:
                        # This was the last player alive
                        # show it's hit here as we're going to leave this
                        # function early
                        self.sendUpdate("showHit", [attackedPlayer.name, atk])

                        base.taskMgr.doMethodLater(
                            self.afterShowHitDelay, self.battleOver,
                            "delayedBattleOver", extraArgs=[False],
                            appendTask=False)
                        return
                else:
                    # can heal himself
                    attackedPlayer.numHealPotions -= 1
                    if attackedPlayer.avId > 0:
                        self.sendUpdateToAvatarId(
                            attackedPlayer.avId, "gotDefeated",
                            [False, attackedPlayer.numHealPotions])

            # tell the players to show the hitpoints dealt to the given player
            self.sendUpdate("showHit", [attackedPlayer.name, atk])

        # Give a little time untill the next fighters turn
        base.taskMgr.doMethodLater(
            self.afterShowHitDelay, self.nextFighter,
            "delayedNextFighter", extraArgs=[],
            appendTask=False)

    def playerAttack(self, botAvId=None):
        """Calculate a players attack"""
        # get the requesting player
        playerId = botAvId
        if botAvId is None:
            playerId = self.air.getAvatarIdFromSender()

        # check if it's actually this players turn
        if playerId != self.fightOrder[0][0]:
            if playerId > 0:
                self.sendUpdateToAvatarId(playerId, "attackFailed", [])
            return

        # get the last enemy in the line. It actually doesn't matter which enemy
        # we attack, as all of them have the same initiative level and so it
        # won't change the order or have any other strategic effect
        enemyName = "Enemy {}".format(self.enemyAI.numEnemies)
        atk = 0
        # find the player and roll the players attack value
        for player in self.playersOnField:
            if player.avId == playerId:
                atk = self.dice.roll() + player.getAttack()
                break

        # check if the player defeated an enemy
        if self.enemyAI.defeatedOne(atk):
            # tell the players they defeated an enemy
            self.sendUpdate("enemyDefeated", [])
            # update the fight order
            for entry in self.fightOrder[:]:
                if entry[0] == -(self.enemyAI.numEnemies+1000):
                    self.fightOrder.remove(entry)
                    break

            # check if all enemies have beend efeated
            if self.enemyAI.defeatedAll():
                self.sendUpdate("showHit", [enemyName, atk])
                base.taskMgr.doMethodLater(
                    self.afterShowHitDelay, self.battleOver,
                    "delayedBattleOver", extraArgs=[True],
                    appendTask=False)
                return

        # Tell the players to show the hit on the enemy
        self.sendUpdate("showHit", [enemyName, atk])

        # Tell this player it's turn is over
        if playerId > 0:
            self.sendUpdateToAvatarId(playerId, "endRound", [])
        base.taskMgr.doMethodLater(
            self.afterShowHitDelay, self.nextFighter,
            "delayedNextFighter", extraArgs=[],
            appendTask=False)

    def battleOver(self, playersWon):
        """Function to tell anyone this battle is over. Given with the outcome
        of this battle wether players or foes have won it"""
        self.sendUpdate("endBattle", [playersWon])
        base.taskMgr.doMethodLater(3, self.endBattle, "delayedEndBattle", extraArgs=[playersWon], appendTask=False)

    def endBattle(self, playersWon):
        """This method is to tell the server that the battle is over and should
        be cleaned up"""
        base.messenger.send(self.uniqueName("endBattle"), [self.field, playersWon])
