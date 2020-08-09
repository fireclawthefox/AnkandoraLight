#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import random

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from dice.SixSidedDice import SixSidedDice
from globalData import RoomGlobals
from battle.DBattleAI import DBattleAI

class DRoomAI(DistributedObjectAI):

    def __init__(self, air, name, maxPlayers, difficulty, gameType, roomZone):
        DistributedObjectAI.__init__(self, air)
        self.name = name
        self.maxPlayers = maxPlayers
        self.difficulty = difficulty
        self.gameType = gameType

        self.roomZone = roomZone

        self.playerList = []
        self.readyPlayers = []
        self.aiPlayerList = []
        self.activePlayerId = -1

        self.currentRoll = -1

        self.canJoin = True

        # Create a board in this room
        self.boardAI = self.air.createDistributedObject(
            className = 'DBoardAI',
            zoneId = self.roomZone)

        self.boardAI.setupQuestCards(self.roomZone)
        self.boardAI.gameType = self.gameType
        self.accept(self.boardAI.uniqueName("PlayerWonRace"), self.gameOver)
        self.accept(self.boardAI.uniqueName("canInitiateFight"), self.canInitiateFight)
        self.accept(self.boardAI.uniqueName("initiateDirectFight"), self.initiateDirectFight)
        self.accept(self.boardAI.uniqueName("levelUpAllPlayers"), self.levelUpAllPlayers)

        self.dice = SixSidedDice()

    def delete(self):
        self.air.roomZoneAllocator.free(self.roomZone)
        self.roomZone = None

        # cleanup players
        for player in self.playerList:
            self.air.sendDeleteMsg(player)
        self.playerList = []

        # cleanup board
        self.air.sendDeleteMsg(self.boardAI.doId)

        DistributedObjectAI.delete(self)

    def getPlayerCount(self):
        return len(self.playerList)

    def getAIPlayerCount(self):
        return len(self.aiPlayerList)

    def addPlayer(self, player):
        # check if the room has place for another player
        if self.isFull():
            print("Room {} already full".format(self.name))
            return False

        # add the player to the list
        self.playerList.append(player)

        # find a start position for the new player
        startField = self.boardAI.getStartField(self.getPlayerCount())
        if startField == None:
            print("Room {} couldn't find start position".format(self.name))
            return False
        player.currentField = startField
        player.startField = startField
        player.piece.setPos(startField.nodepath.getPos())

        # check if other players can join
        self.canJoin = self.getPlayerCount() < self.maxPlayers

        return True

    def endTurn(self):
        """End the current players turn. Can only be called by the player whos
        turn it actually is at the moment."""
        playerId = self.air.getAvatarIdFromSender()
        if playerId != self.activePlayerId:
            return

        # reset the roll so the next player can roll the dice again
        self.currentRoll = -1

        nextPlayer = None
        # find the next player ID
        for player in self.playerList:
            if player.avId != self.activePlayerId: continue
            idx = self.playerList.index(player) + 1
            if idx >= len(self.playerList): idx = 0
            self.activePlayerId = self.playerList[idx].avId
            nextPlayer = self.playerList[idx]
            break

        # send an update to the channel so everyone knows who's next
        self.sendUpdate("nextPlayer", [nextPlayer.getName()])

        # send the end turn to the current player so he knows he can deactivate
        # the relevant gui elements
        self.sendUpdateToAvatarId(playerId, "endTurn", [])

        # send the start turn to the next active player so he can enable the gui
        # and other relevant elements
        self.sendUpdateToAvatarId(nextPlayer.avId, "startTurn", [])

    def isFull(self):
        """Returns wether there are already the maximum amount of players in
        this room or not"""
        return self.getPlayerCount() == self.maxPlayers

    def d_startRoom(self):
        """Tell the players that the room is starting."""
        # we can only start if all players are ready
        if len(self.readyPlayers) != self.maxPlayers: return

        # determine who will be the starting player
        if self.activePlayerId == -1:
            if self.gameType == RoomGlobals.GAMETYPE_RACE:
                # on race mode, choose a random player
                self.activePlayerId = random.choice(self.playerList).avId
            else:
                # the first joint player will be the starting player
                self.activePlayerId = self.playerList[0].avId

        nextPlayer = None
        for player in self.playerList:
            if player.avId != self.activePlayerId: continue
            nextPlayer = player
            break

        # send an update to the channel so everyone knows who's next
        self.sendUpdate("nextPlayer", [nextPlayer.getName()])

        # send the start turn to the next active player so he can enable the gui
        # and other relevant elements
        self.sendUpdateToAvatarId(nextPlayer.avId, "startTurn", [])

        self.sendUpdate("startRoom", [])

    def playerReady(self, playerId):
        if playerId not in self.readyPlayers:
            self.readyPlayers.append(playerId)

        self.d_startRoom()

    def removePlayer(self, playerId):
        """Remove the player with the given ID from the rooms player list"""
        self.air.sendDeleteMsg(playerId)

        for p in self.playerList[:]:
            if p.doId == playerId:
                if self.activePlayerId == p.avId:
                    self.endTurn()
                self.playerList.remove(p)
        return len(self.playerList) == 0

    def getPlayerNames(self):
        """Return a list of all player names in this room"""
        names = []
        for p in self.playerList:
            names.append(p.name)
        return names

    def rollDice(self):
        """Roll the dice and store the value. This can only be called by the
        active player"""
        playerId = self.air.getAvatarIdFromSender()
        if playerId != self.activePlayerId:
            self.sendUpdateToAvatarId(playerId, "rolledDiceFailed", [])
            return

        if self.currentRoll == -1:
            self.currentRoll = self.dice.roll()
            self.sendUpdateToAvatarId(playerId, "rolledDice", [self.currentRoll])
        else:
            self.sendUpdateToAvatarId(playerId, "rolledDiceFailed", [])

    def requestMoveToField(self, fieldName):
        """Request to move the player to the given field. This can onyl be
        called by the active player and will be refused if the players roll is
        not sufficient to move to the given field"""
        playerId = self.air.getAvatarIdFromSender()
        if playerId != self.activePlayerId:
            return

        if self.currentRoll <= 0:
            return

        activePlayer = None
        playerField = None
        for player in self.playerList:
            if player.avId == playerId:
                activePlayer = player
                playerField = player.currentField
                break

        if self.boardAI.canMoveTo(playerField, fieldName, self.currentRoll):
            self.currentRoll -= self.boardAI.minCumulatedCost

            # reset possible other players on last field
            lastField = activePlayer.currentField
            activePlayer.currentField = None
            self.setMultiplePlayersOnField(lastField)

            # move to the new field
            field = self.boardAI.getField(fieldName)
            activePlayer.currentField = field
            # and check if there are other players that have to be moved
            self.setMultiplePlayersOnField(field)

            self.boardAI.processSpecialFields(field)

            # update the roll for the player so he knows how far he can still go
            self.sendUpdateToAvatarId(playerId, "updateRolledDice", [self.currentRoll])

    def setMultiplePlayersOnField(self, field):
        """Move the players a bit to not position them inside each other"""
        playersOnField = []

        for player in self.playerList:
            if player.currentField == field:
                playersOnField.append(player)

        shiftX = shiftY = 0
        positions = [[-0.01,0.01], [0.01,0.01], [-0.01,-0.01], [0.01,-0.01]]
        if len(playersOnField) > 1:
            for player in playersOnField:
                player.moveTo(field, positions[0][0], positions[0][1])
                del positions[0]
        elif len(playersOnField) == 1:
            playersOnField[0].moveTo(field, 0, 0)

    def canInitiateFight(self, field):
        """A player can start a fight on the given field. Tell that to the
        player so he can decide what to do."""
        playerId = self.air.getAvatarIdFromSender()
        self.canBattle = True
        self.currentFightField = field
        self.sendUpdateToAvatarId(playerId, "canInitiateFight", [])

    def initiateDirectFight(self, field):
        """Skip the questioning of players if they want to start a fight and
        directly jump into it."""
        self.canBattle = True
        self.currentFightField = field
        self.initiateFight()

    def initiateFight(self):
        """Start a fight on the previously set fight field if a battle can be
        initiated."""
        if not self.canBattle: return
        self.canBattle = False
        field = self.currentFightField
        playersOnField = []
        spectatorPlayers = []

        playersOnField = self.boardAI.getAttendingPlayers(field, self.playerList)
        for player in self.playerList:
            if player not in playersOnField:
                spectatorPlayers.append(player)


        self.battleAI = DBattleAI(self.air, field, playersOnField, spectatorPlayers, self.difficulty)

        self.air.createDistributedObject(
            distObj = self.battleAI,
            zoneId = self.roomZone)

        for player in playersOnField:
            self.sendUpdateToAvatarId(player.avId, "startBattle", [])
        for player in spectatorPlayers:
            self.sendUpdateToAvatarId(player.avId, "spectateBattle", [])


        self.accept(self.battleAI.uniqueName("endBattle"), self.stopFight)

    def stopFight(self, field, playersWon):
        """Called when the battle is over, given the fight the battle was held
        on and a boolean value wheter the players or the enemies have won."""
        if playersWon:
            self.boardAI.wonFight(field)
        else:
            for player in self.battleAI.playersAttending:
                player.resetToStartField()

        # cleanup the battlefield
        if hasattr(self, "battleAI"):
            self.air.deleteObject(self.battleAI.doId)
            del self.battleAI

    def levelUpAllPlayers(self):
        """Raise the level of all players by 1 if they can level up. Currently
        capped at level 2"""
        for player in self.playerList:
            if player.level == 1:
                player.level += 1
                player.updateInventory()

    def gameOver(self, field):
        """The game is over, tell weveryone who won this round"""
        if self.gameType == RoomGlobals.GAMETYPE_RACE:
            winningPlayerName = ""
            for player in self.playerList:
                if player.currentField == field:
                    winningPlayerName = player.name
            for player in self.playerList:
                self.sendUpdateToAvatarId(player.avId, "gameOver", [winningPlayerName])
        elif self.gameType == RoomGlobals.GAMETYPE_NORMAL:
            for player in self.playerList:
                self.sendUpdateToAvatarId(player.avId, "gameOver", ["ALL"])
