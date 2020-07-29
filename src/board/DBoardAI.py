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

        print("LOADING BOARD MODEL FOR SERVER")
        # need to load the model to get the positions out of it
        self.boardScene = loader.loadModel("assets/models/BoardScene.bam")
        self.setupFieldPositions()

    def getStartField(self, posNr):
        for field in BoardMap.gameMap:
            if field.name == "Start_{}".format(posNr):
                return field

    def setupFieldPositions(self):
        for field in BoardMap.gameMap:
            fieldNP = self.boardScene.find("**/{}".format(field.name))
            field.nodepath = fieldNP

    def setupQuestCards(self, roomZone):
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
        for field in BoardMap.gameMap:
            if field.name == fieldName:
                return field

    def canMoveTo(self, playerField, fieldName, roll):
        self.cumulatedCost = 0
        self.minCumulatedCost = 0
        self.visitedFields = [playerField]
        field = self.getField(fieldName)

        # we may not move back to the start field
        if field.special == "StartField": return False

        if self.findFieldConnection(playerField, fieldName):
            if self.minCumulatedCost <= roll:
                if self.canMoveToSpecialFields(field):
                    return True
        return False

    def findFieldConnection(self, startField, destinationName):
        canMove = False
        for connection in startField.connections:
            if connection in self.visitedFields:
                continue
            self.cumulatedCost += connection.cost
            if connection.name == destinationName:
                canMove = True
                # chec if this is the shortest/most inexpensive path to walk
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
        if field.special == "": return True

        if field.special == "EndField":
            if self.gameType == RoomGlobals.GAMETYPE_RACE:
                return True
            elif self.gameType == RoomGlobals.GAMETYPE_NORMAL:
                if len(self.collectedQuestCards) == len(BoardMap.fightFields):
                    return True
                else:
                    return False

        elif field.special in BoardMap.fightFields:
            return True

        return True

    def processSpecialFields(self, field):
        if field.special == "": return

        if field.special == "EndField":
            if self.gameType == RoomGlobals.GAMETYPE_RACE:
                base.messenger.send(self.uniqueName("PlayerWonRace"), [field])
            elif self.gameType == RoomGlobals.GAMETYPE_NORMAL:
                if len(self.collectedQuestCards) == len(BoardMap.fightFields):
                    base.messenger.send(self.uniqueName("InitiateFight"), [field])

        elif field.special in BoardMap.fightFields:
            if field not in self.collectedQuestCardFields:
                base.messenger.send(self.uniqueName("InitiateFight"), [field])

    def wonFight(self, field):
        self.collectedQuestCardFields.append(field)
        questCard = self.questCards[field]
        questCard.d_collect()
        self.collectedQuestCards.append(questCard)
        if len(self.collectedQuestCards) == 4 and self.gameType == RoomGlobals.GAMETYPE_NORMAL:
            base.messenger.send(self.uniqueName("levelUpAllPlayers"))
