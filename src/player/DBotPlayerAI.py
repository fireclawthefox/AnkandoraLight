#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.task import Task

from piece.DPieceAI import DPieceAI
from player.ClassManager import ClassManager

from board import BoardMap
from globalData import RoomGlobals


class DBotPlayerAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.name = ""
        self.avId = -1
        self.botId = 0
        self.currentField = None
        self.startField = None
        self.piece = None
        self.playerClassID = -1
        self.playerClassType = "Unknown"
        self.level = 1
        self.numHealPotions = 3
        self.room = None
        self.needEndTurn = False

        self.cm = ClassManager()

    def delete(self):
        """Cleanup just before the object gets deleted"""
        if self.piece is not None:
            self.air.sendDeleteMsg(self.piece.doId)

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def requestName(self):
        """Roundtrip to set the name of this Player on the client"""
        requesterId = self.air.getAvatarIdFromSender()
        self.sendUpdateToAvatarId(requesterId, "setName", [self.name])

    def startTurn(self):
        """ Start this players turn """
        self.room.botRollDice()
        taskMgr.doMethodLater(1, self.move, "bot-think-time", extraArgs=[])

    def move(self):
        """The bots' movement logic. Will calculate where the bot should move
        to next."""
        self.path = []
        if self.room.gameType == RoomGlobals.GAMETYPE_NORMAL:
            #
            # NORMAL MODE LOGIC
            #
            # The field where we should move to.  If no other field, move to the
            # end field with the number of this bot +1 (e.g. EndField2)
            fieldName = "EndField_{}".format(self.botId+1)

            # in normal mode, we want to move to the fight fields. Simply
            # move to them in the given order of the BoardMap
            for fieldSpecial in BoardMap.fightFields:
                # Skip this field as it's been done
                if self.room.boardAI.collectedQuestCard(fieldSpecial):
                    continue
                # now search for the actual field with that special field set
                for field in BoardMap.gameMap:
                    if field.special == fieldSpecial:
                        # found our destination field
                        fieldName = field.name
                        break
                # we can continue if we found a field which will be anything
                # than the end field
                if fieldName != "EndField_{}".format(self.botId+1):
                    break

            if self.currentField.name == fieldName:
                # we're at our destination. Skip this turn
                self.room.processEndTurn()
                return
            self.path = self.room.boardAI.getCheapestPathToFieldName(self.currentField, fieldName)
        else:
            #
            # RACE MODE LOGIC
            #
            # Simply move to the end field
            #TODO: Should check if there are other fields nearby if the "shortest" way is not always the most easy one
            #      e.g. can move on the shortest route only with a dice roll of 5+ but could move around that with
            #      slightly more turns but lower individual field costs
            #        5
            #  P <       > D
            #      3 - 3
            # P = Player
            # D = Destination
            # # = field costs
            # Bot should check if he can move on the upper path first, if not he
            # may be faster taking the lower one
            self.path = self.room.boardAI.getCheapestPathToFieldName(self.currentField, "EndField_{}".format(self.botId+1))

        taskMgr.doMethodLater(0.5, self.moveNext, "bot-move", extraArgs=[])

    def moveNext(self):
        field = None

        # if we're already at our destination, we can skip this turn
        if len(self.path) == 0:
            self.processAndEndTurn(self.currentField)
            return Task.done

        # get the next field in the path
        field = self.path[0]
        self.path = self.path[1:]
        # check if the dice rolled waypoints are enough to move on
        if field.cost > self.room.currentRoll:
            self.processAndEndTurn(self.currentField)
            return Task.done

        # reduce our roll by the fields waypoint cost
        self.room.currentRoll -= field.cost

        # reset possible other players on last field
        lastField = self.currentField
        self.currentField = None
        self.room.setMultiplePlayersOnField(lastField)

        # move to the new field
        self.currentField = field
        # and check if there are other players that have to be moved
        self.room.setMultiplePlayersOnField(field)

        # we reached a fight field. Stop here.
        if field.special in BoardMap.fightFields:
            self.processAndEndTurn(field)
            return Task.done

        # do this task again until we reached an end condition
        return Task.again

    def processAndEndTurn(self, field):
        """Call the special field processing and end the turn if possible"""
        if self.room.boardAI.processSpecialFields(field, True):
            self.needEndTurn = False
            # We can continue with the next player
            self.room.processEndTurn()
        else:
            self.needEndTurn = True

    def resetToStartField(self):
        """Reset the player to its own start field and set the health potions
        back to the maximum"""
        self.moveTo(self.startField, 0, 0)

        self.numHealPotions = 3

    def moveTo(self, field, shiftX, shiftY):
        """Move the piece to the given location"""
        self.currentField = field
        self.piece.d_setXY(field.nodepath.getX() + shiftX, field.nodepath.getY() + shiftY)

    def startBattle(self, battleAI):
        """Start the battle system for this bot"""
        self.battleAI = battleAI
        self.accept(self.battleAI.uniqueName("endBattle"), self.endBattle)
        self.accept(self.battleAI.uniqueName("startRoundBot-{}".format(self.avId)), self.startBattleRound)
        self.battleAI.rollInitiative(self.avId)

    def startBattleRound(self):
        """It's this bots' turn in a battle"""
        self.battleAI.playerAttack(self.avId)

    def endBattle(self, field, won):
        """Stop the battle for this bot and check if he needs to end his turn"""
        if self.needEndTurn:
            # end this bots turn after battle if it was this bot's turn before
            # which is usually just the case in race mode
            self.room.processEndTurn()
            self.needEndTurn = False

    def updateInventory(self):
        """Just a required implementation, won't do anything."""
        # nothing to do here
        pass

    def getAttack(self):
        """Returns the attack strength of the players class"""
        return self.cm.getAttack(self.playerClassType, self.level)

    def getDefense(self):
        """Returns the defensive strength of the players class"""
        return self.cm.getDefense(self.playerClassType, self.level)
