#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from board import BoardMap
from globalData import RoomGlobals
from questCard.DQuestCardAI import DQuestCardAI

class DBoardAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.gameType = None
        self.collectedQuestCards = []
        self.collectedQuestCardFields = []

        self.questCards = {}

        # need to load the model to get the positions out of it
        self.boardScene = loader.loadModel("assets/models/board/BoardScene.bam")
        self.setupFieldPositions()

    def getStartField(self, posNr):
        """Returns the start field with the given number"""
        for field in BoardMap.gameMap:
            if field.name == "Start_{}".format(posNr):
                return field

    def setupFieldPositions(self):
        """Fills the nodepath variable of all fields"""
        for field in BoardMap.gameMap:
            fieldNP = self.boardScene.find("**/{}".format(field.name))
            field.nodepath = fieldNP

    def setupQuestCards(self, roomZone):
        """Create all quest cards on the map and places them correctly"""
        endQuestCard = DQuestCardAI(self.cr, "Crown")
        self.air.createDistributedObject(
            distObj = endQuestCard,
            zoneId = roomZone)
        endCardNP = self.boardScene.find("**/QuestChip_Crown")
        endQuestCard.setPos(endCardNP.getPos())

        for field in BoardMap.gameMap:
            if field.special in BoardMap.fightFields:
                questCard = DQuestCardAI(self.cr, field.special)

                self.air.createDistributedObject(
                    distObj = questCard,
                    zoneId = roomZone)

                questCardNP = self.boardScene.find("**/QuestChip_{}".format(field.special))
                questCard.setPos(questCardNP.getPos())
                self.questCards[field] = questCard

            if field.special == "EndField":
                self.questCards[field] = endQuestCard

    def getField(self, fieldName):
        """Returns the field with the given name"""
        for field in BoardMap.gameMap:
            if field.name == fieldName:
                return field

    def getMinCostOfPathToFieldName(self, startField, destinationName):
        self.cumulatedCost = 0
        self.minCumulatedCost = 0
        self.visitedFields = [startField]
        self.cheapestPathFields = []
        self.pathFields = []
        self.findCheapestPathToFieldName(startField, destinationName)
        return self.minCumulatedCost

    def getCheapestPathToFieldName(self, startField, destinationName):
        self.cumulatedCost = 0
        self.minCumulatedCost = 0
        self.visitedFields = [startField]
        self.cheapestPathFields = []
        self.pathFields = []
        self.findCheapestPathToFieldName(startField, destinationName)
        return self.cheapestPathFields

    def getAllPathsToFieldName(self, startField, destinationName):
        self.visitedFields = [startField]
        self.paths = []
        self.findAllPathsToFieldName(startField, destinationName)
        return self.paths

    def findAllPathsToFieldName(self, startField, destinationName):
        for connection in startField.connections:
            if connection in self.visitedFields:
                continue
            self.pathFields.append(connection)
            if connection.name == destinationName:
                # we found a path from start to destination, add it to the list
                self.paths.append(self.pathFields.copy())
            else:
                # add the field to the current journey and continue down the path
                self.visitedFields.append(connection)
                self.findAllPathsToFieldName(connection, destinationName)

            if connection in self.visitedFields:
                self.visitedFields.remove(connection)
            self.pathFields.remove(connection)

    def findCheapestPathToFieldName(self, startField, destinationName):
        for connection in startField.connections:
            if connection in self.visitedFields:
                continue
            self.cumulatedCost += connection.cost
            self.pathFields.append(connection)
            if connection.name == destinationName:
                # check if this is the shortest/most inexpensive path to walk
                if self.minCumulatedCost == 0:
                    self.minCumulatedCost = self.cumulatedCost
                    self.cheapestPathFields = self.pathFields.copy()

                if self.cumulatedCost < self.minCumulatedCost:
                    # found a new cheaper path
                    self.cheapestPathFields = self.pathFields.copy()

                self.minCumulatedCost = min(self.minCumulatedCost, self.cumulatedCost)
            else:
                # as we may find multiple ways to the destination, we don't want
                # to add the destination itself to the found fields.  So we add
                # it here.
                self.visitedFields.append(connection)
                self.findCheapestPathToFieldName(connection, destinationName)

            if connection in self.visitedFields:
                self.visitedFields.remove(connection)
            # this field may not belong to the sum of the path to walk on. If it
            # does, we already have it added to the minimum walk cost
            self.cumulatedCost -= connection.cost
            self.pathFields.remove(connection)

    def canMoveTo(self, playerField, fieldName, roll):
        """Check if the player can move from it's given field to the requested
        other field with the given dice roll"""
        self.cumulatedCost = 0
        self.minCumulatedCost = 0
        self.visitedFields = [playerField]
        field = self.getField(fieldName)

        # we may not move back to the start field
        if field.special == "StartField": return False

        # check if the fields are actually connected
        if self.findFieldConnection(playerField, fieldName):
            # check if the cumulated costs for the fastest track are less then
            # the amount the player rolled with the dice
            if self.minCumulatedCost <= roll:
                # we could theoretically move to the new field, now check if it
                # is a special field that may require specific things to be done
                # prior to moving to it.
                if self.canMoveToSpecialFields(field):
                    return True
        return False

    def findFieldConnection(self, startField, destinationName):
        """This function will search for all connections of the two given fields.
        The cost for the shortest way of moving to the destination field will be
        stored in the cumulatedCost variable."""
        canMove = False
        for connection in startField.connections:
            if connection in self.visitedFields:
                continue
            self.cumulatedCost += connection.cost
            if connection.name == destinationName:
                canMove = True
                # check if this is the shortest/most inexpensive path to walk
                if self.minCumulatedCost == 0: self.minCumulatedCost = self.cumulatedCost
                self.minCumulatedCost = min(self.minCumulatedCost, self.cumulatedCost)
            else:
                # as we may find multiple ways to the destination, we don't want
                # to add the destination itself to the found fields.  So we add
                # it here.
                self.visitedFields.append(connection)
                if self.findFieldConnection(connection, destinationName):
                    canMove = True

            if connection in self.visitedFields:
                self.visitedFields.remove(connection)
            # this field may not belong to the sum of the path to walk on. If it
            # does, we already have it added to the minimum walk cost
            self.cumulatedCost -= connection.cost
        return canMove

    def canMoveToSpecialFields(self, field):
        """Check function to see if it is possible to move to the desired field
        by checking the special field property of it."""
        if field.special == "": return True

        if field.special == "EndField":
            if self.gameType == RoomGlobals.GAMETYPE_RACE:
                # in race mode, we can always move to the end field
                return True
            elif self.gameType == RoomGlobals.GAMETYPE_NORMAL:
                # in normal mode, we first need to gather all other quest cards
                if len(self.collectedQuestCards) == len(BoardMap.fightFields):
                    return True
                else:
                    # the players haven't collected all other quest cards yet
                    return False

        # This special field doesn't hold us back from moving there
        return True

    def processSpecialFields(self, field, ignoreFight=False):
        """This function will initiate the feature of the given field if it is
        a special field."""
        # not a special field, nothing to do here.
        if field.special == "": return True

        # check if a player moved to the end field
        if field.special == "EndField":
            if self.gameType == RoomGlobals.GAMETYPE_RACE:
                base.messenger.send(self.uniqueName("initiateDirectFight"), [field])
                #base.messenger.send(self.uniqueName("gameOver"), [field])
            elif self.gameType == RoomGlobals.GAMETYPE_NORMAL:
                if len(self.collectedQuestCards) == len(BoardMap.fightFields):
                    if not ignoreFight:
                        base.messenger.send(self.uniqueName("canInitiateFight"), [field])
                    return True

        # check if a player moved to any of the fight fields
        elif field.special in BoardMap.fightFields:
            if field not in self.collectedQuestCardFields:
                if self.gameType == RoomGlobals.GAMETYPE_RACE:
                    # in race mode, directly start the fight
                    base.messenger.send(self.uniqueName("initiateDirectFight"), [field])
                    return False
                else:
                    # in normal mode, give the players time to gather on a field
                    # to let them fight together
                    if not ignoreFight:
                        base.messenger.send(self.uniqueName("canInitiateFight"), [field])
                    return True

        # check if a player moved to a level up field special to the race mode
        elif field.special in BoardMap.raceLevelUp and self.gameType == RoomGlobals.GAMETYPE_RACE:
            base.messenger.send(self.uniqueName("levelUpAllPlayers"))
        return True

    def getAttendingPlayers(self, field, playerList):
        """Returns a list of all players of the given player list, that are
        attending the fight going on on the given field."""
        searchFields = []
        attendingPlayers = []
        if field.special == "EndField":
            # if we are on an end field, we have to gather all players from all
            # end fields.
            for field in BoardMap.gameMap:
                if field.special == "EndField":
                    searchFields.append(field)
        else:
            searchFields.append(field)

        for player in playerList:
            if player.currentField in searchFields:
                attendingPlayers.append(player)
        return attendingPlayers

    def wonFight(self, field):
        """The players won the fight on the given field. Collect the quest card
        and check for a level up"""
        self.collectedQuestCardFields.append(field)
        questCard = self.questCards[field]
        questCard.d_collect()
        self.collectedQuestCards.append(questCard)

        # check for the level up.
        # We might want to move that out to a dedicated function and check for
        # a more sophisticated ruleset on level ups to make this more broadly
        # usable
        if len(self.collectedQuestCards) == 4:
            base.messenger.send(self.uniqueName("levelUpAllPlayers"))

        if field.special == "EndField":
            base.messenger.send(self.uniqueName("gameOver"), [field])

    def collectedQuestCard(self, fieldSpecialName):
        for card in self.collectedQuestCards:
            if card.fieldName == fieldSpecialName:
                return True
        return False
