#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import random
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from panda3d.core import UniqueIdAllocator
from room.DRoomAI import DRoomAI
from globalData import ZonesGlobals, RoomGlobals

class DRoomManagerAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.air.roomZoneAllocator = UniqueIdAllocator(
            ZonesGlobals.ROOM_MIN_ID_ZONE,
            ZonesGlobals.ROOM_MAX_ID_ZONE)

        self.roomList = []

        self.accept("Client-disconnect", self.handleClientDisconnect)

    def delete(self):
        self.roomList = []
        DistributedObjectAI.delete(self)

    def getRoomInfoList(self):
        roomInfoList = []
        for room in self.roomList:
            roomInfo = (
                room.name,
                room.maxPlayers,
                room.getPlayerCount(),
                room.getBotPlayerCount(),
                room.difficulty,
                room.gameType,
                room.roomZone)
            roomInfoList.append(roomInfo)
        return roomInfoList

    def requestRoomList(self):
        requesterId = self.air.getAvatarIdFromSender()
        roomInfoList = self.getRoomInfoList()
        self.sendUpdateToAvatarId(requesterId, "setServerRoomList", [roomInfoList])

    def requestCreateRoom(self, roomInfo):
        requesterId = self.air.getAvatarIdFromSender()

        if len(roomInfo) != 7:
            print("room creation failed, unknown info length: {}".format(len(roomInfo)))
            return

        if (roomInfo[RoomGlobals.ROOM_NAME] is None or len(roomInfo[RoomGlobals.ROOM_NAME]) < 1):
            print("room creation failed, bad room name. Room name must not be none or empty.")
            return

        if (roomInfo[RoomGlobals.ROOM_MAX_PLAYER_COUNT] < 1 or roomInfo[RoomGlobals.ROOM_MAX_PLAYER_COUNT] > 4):
            print("room creation failed, wrong player count: {} (Min: 1 | Max: 4)".format(roomInfo[RoomGlobals.ROOM_MAX_PLAYER_COUNT] + roomInfo[RoomGlobals.ROOM_AI_PLAYER_COUNT]))
            return

        if (roomInfo[RoomGlobals.ROOM_DIFFICULTY] not in RoomGlobals.DIFFICULTIES):
            print("room creation failed, unknonwn difficulty: {}".format(roomInfo[RoomGlobals.ROOM_DIFFICULTY]))
            return

        if (roomInfo[RoomGlobals.ROOM_TYPE] not in RoomGlobals.ALL_GAMETYPES):
            print("room creation failed, unknonwn game type")
            return

        newRoom = DRoomAI(
            self.air,
            roomInfo[RoomGlobals.ROOM_NAME],
            roomInfo[RoomGlobals.ROOM_MAX_PLAYER_COUNT],
            roomInfo[RoomGlobals.ROOM_DIFFICULTY],
            roomInfo[RoomGlobals.ROOM_TYPE],
            self.air.roomZoneAllocator.allocate())
        self.air.createDistributedObject(
            distObj = newRoom,
            zoneId = ZonesGlobals.ROOM_MANAGER_ZONE)

        for i in range(roomInfo[RoomGlobals.ROOM_AI_PLAYER_COUNT]):
            # create the bots
            botPlayer = self.air.createDistributedObject(
                className="DBotPlayerAI",
                zoneId=newRoom.roomZone)
            botPlayer.playerClassID = random.choice(RoomGlobals.ALL_PLAYERCLASSES)
            botPlayer.playerClassType = RoomGlobals.PlayerClassID2Name[botPlayer.playerClassID]
            botPlayer.botId = i+1
            botPlayer.avId = -(i+1)
            botPlayer.room = newRoom

            piece = self.air.createDistributedObject(
                className="DPieceAI",
                zoneId=newRoom.roomZone)

            botPlayer.piece = piece
            piece.player = botPlayer
            modelName = botPlayer.cm.getModel(botPlayer.playerClassType)
            piece.setModel(modelName)

            # give the new player a unique name
            playerNameList = newRoom.getPlayerNames()
            playerName = self.getRandomPlayerName()
            while playerName in playerNameList:
                playerName = self.getRandomPlayerName()
            botPlayer.setName(playerName)

            # try add the player to the room
            if not newRoom.addPlayer(botPlayer):
                # can't add more bots
                self.air.sendDeleteMsg(botPlayer.doId)
                self.air.sendDeleteMsg(piece.doId)
            else:
                newRoom.numBotPlayers += 1

            newRoom.playerReady(botPlayer.doId)

            self.accept(newRoom.uniqueName("startBotTurn-{}".format(botPlayer.botId)), botPlayer.startTurn)

        self.roomList.append(newRoom)

        roomInfoList = self.getRoomInfoList()
        self.sendUpdateToAvatarId(requesterId, "setServerRoomList", [roomInfoList])

    def getServerRoomList(self):
        return self.roomList

    def getRandomPlayerName(self):
        """Create a random name for a player made up of an adjective and
        an animal"""
        namePartA = random.choice([
            "Adorable", "Adventurous", "Angry", "Arrogant",
            "Brave", "Bright", "Busy", "Blushing",
            "Calm", "Clumsy", "Confused", "Cute",
            "Dangerous", "Determained", "Dizzy", "Dull",
            "Eager", "Elegant", "Embarrassed", "Excited",
            "Fancy", "Foolish", "Funny", "Frantic",
            "Gentle", "Good", "Graceful", "Glamorous",
            "Handsome", "Happy", "Hilarious", "Hungry",
            "Important", "Innocent", "Impossible", "Itchy",
            "Jealous", "Jittery", "Jolly", "Joyous",
            "Kind", "Kin", "Knotty", "Keen",
            "Lazy", "Light", "Long", "Lovely",
            "Magnificent", "Marvelous", "Muddy", "Mysterious",
            "Naughty", "Nutty", "Nice", "Nervous",
            "Odd", "Open", "Outstanding", "Obedient",
            "Pleasant", "Proud", "Powerful", "Precious",
            "Quaint", "Quarterly", "Queer", "Quantal",
            "Real", "Relieved", "Repulsive", "Rich",
            "Shiny", "Shy", "Sparkling", "Sleepy",
            "Talented", "Tame", "Tasty", "Tired",
            "Unusual", "Upset", "Urgent", "Used",
            "Vast", "Valued", "Vanilla", "Very",
            "Wild", "Witty", "Worried", "Wicked",
            "Xenial", "Xeric", "Xyloid", "Xanthous",
            "Yawning", "Young", "Yummy", "Yonder",
            "Zany", "Zippy", "Zesty", "Zonal"])
        namePartB = random.choice([
            "Aardvark", "Albatross", "Alligator", "Armadillo",
            "Bobcat", "Butterfly", "Bear", "Bat",
            "Caracal", "Cheetah", "Catterpilar", "Crane",
            "Deer", "Duck", "Donkey", "Dingo",
            "Eagle", "Elephant", "Emu", "Echidna",
            "Fox", "Falcon", "Frog", "Ferret",
            "Gecko", "Goat", "Giraffe", "Gibbon",
            "Hare", "Horse", "Hyena", "Heron",
            "Ibis", "Iguana", "Impala", "Indri",
            "Jackal", "Jaguar", "Jellyfish",
            "Kiwi", "Koala", "Kudu", "Kangaroo",
            "Lemur", "Leopard", "Lion", "Lynx",
            "Meerkat", "Moth", "Mouse", "Manatee",
            "Newt", "Nightingale", "Newfoundland", "Numbat",
            "Ocelot", "Okapi", "Otter", "Octopus",
            "Penguin", "Platypus", "Prawn", "Parrot",
            "Quail", "Quetzal", "Quokka", "Quoll",
            "Raccoon", "Rabbit", "Robin", "Reindeer",
            "Scorpion", "Sheep", "Sloth", "Seal",
            "Tapir", "Tiger", "Tortoise", "Toucan",
            "Uakari", "Uguisu", "Umbrellabird", "Uromastix",
            "Vulture", "Vanga", "Vaquita", "Viper",
            "Wallaby", "Wolf", "Wombat", "Weasel",
            "Xenops", "Xerus", "Xenarthra", "Xenopus",
            "Yak", "Yabby", "Yellowjacket", "Yellowhammer",
            "Zebra", "Zebu", "Zebrafish", "Zorilla"])
        return "{} {}".format(namePartA, namePartB)

    def requestJoin(self, roomZone, playerClassID):
        """Client requesting to join a room. Given the rooms zone and the
        players chosen class ID"""
        requesterId = self.air.getAvatarIdFromSender()

        # search for the room the client requests to join
        roomsMatchingId = filter(lambda room: room.roomZone == roomZone, self.roomList)
        foundRoom = next(roomsMatchingId, None)
        if foundRoom is None:
            print("No room found in zone", roomZone)
            self.sendUpdateToAvatarId(requesterId, "joinFailed", [])
            return

        # check if we can join the room
        if not foundRoom.canJoin:
            self.sendUpdateToAvatarId(requesterId, "joinFailed", [])
            return

        # create a new player instance for the joining client
        player = self.air.createDistributedObject(
            className="DPlayerAI",
            zoneId=roomZone)
        player.avId = requesterId
        player.playerClassID = playerClassID
        player.playerClassType = RoomGlobals.PlayerClassID2Name[playerClassID]

        piece = self.air.createDistributedObject(
            className="DPieceAI",
            zoneId=roomZone)

        player.piece = piece
        piece.player = player
        modelName = player.cm.getModel(player.playerClassType)
        piece.setModel(modelName)

        # give the new player a unique name
        playerNameList = foundRoom.getPlayerNames()
        playerName = self.getRandomPlayerName()
        while playerName in playerNameList:
            playerName = self.getRandomPlayerName()
        player.setName(playerName)

        # try add the player to the room
        if not foundRoom.addPlayer(player):
            self.air.sendDeleteMsg(player.doId)
            self.sendUpdateToAvatarId(requesterId, "joinFailed", [])
            return

        parameters = (
            roomZone,
            foundRoom.doId,
            player.doId,
            piece.doId)

        # send the room zone and created player doID back to the requesting client
        self.sendUpdateToAvatarId(requesterId, "joinSuccess", [parameters])

    def requestLeave(self, roomZone, playerId):
        """Player requests to leave the room. We'll look him up and remove him
        if we find him on the room, otherwise we simple ignore it. If this
        player was the last in the room, the room gets removed."""
        roomsMatchingId = filter(lambda room: room.roomZone == roomZone, self.roomList)
        foundRoom = next(roomsMatchingId, None)
        if foundRoom.removePlayer(playerId):
            # all players have left the room
            self.roomList.remove(foundRoom)
            self.air.sendDeleteMsg(foundRoom.doId)

    def handleClientDisconnect(self, doId):
        for room in self.roomList:
            for player in room.playerList:
                if player.doId == doId:
                    room.removePlayer(player.doId)
                    print("FOUND PLAYER THAT LEFT")
