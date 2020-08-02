import random
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from panda3d.core import UniqueIdAllocator
from room.DRoomAI import DRoomAI
from player.DPlayerAI import DPlayerAI
from globalData import ZonesGlobals, RoomGlobals

class DRoomManagerAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.air.roomZoneAllocator = UniqueIdAllocator(
            ZonesGlobals.ROOM_MIN_ID_ZONE,
            ZonesGlobals.ROOM_MAX_ID_ZONE)

        self.roomList = []

        self.accept("Client-disconnect", self.handleClientDisconnect)

    def getRoomInfoList(self):
        roomInfoList = []
        for room in self.roomList:
            roomInfo = (
                room.name,
                room.maxPlayers,
                room.getPlayerCount(),
                room.getAIPlayerCount(),
                room.difficulty,
                room.gameType,
                room.roomZone)
            roomInfoList.append(roomInfo)
        return roomInfoList

    def requestRoomList(self):
        print("CLIENT REQUESTED ROOM LIST")
        requesterId = self.air.getAvatarIdFromSender()
        print("request rooms by ID:", requesterId)
        roomInfoList = self.getRoomInfoList()
        self.sendUpdateToAvatarId(requesterId, "setServerRoomList", [roomInfoList])

    def requestCreateRoom(self, roomInfo):
        print("CLIENT REQUESTED CREATE ROOM")
        requesterId = self.air.getAvatarIdFromSender()
        print("request create room by ID:", requesterId)
        print("ROOM INFO:", roomInfo)

        if len(roomInfo) != 7:
            print("room creation failed, unknown info length")
            return

        if (roomInfo[RoomGlobals.ROOM_NAME] is None or len(roomInfo[RoomGlobals.ROOM_NAME]) < 1):
            print("room creation failed, bad room name")
            return

        if (roomInfo[RoomGlobals.ROOM_MAX_PLAYER_COUNT] < 1 or roomInfo[RoomGlobals.ROOM_MAX_PLAYER_COUNT] + roomInfo[RoomGlobals.ROOM_AI_PLAYER_COUNT] > 4):
            print("room creation failed, wrong player count (Min: 1 | Max: 4)")
            return

        if (roomInfo[RoomGlobals.ROOM_DIFFICULTY] not in RoomGlobals.DIFFICULTIES):
            print("room creation failed, unknonwn difficulty")
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
            #TODO: Create AI Players here and add them to the room
            # aiPlayer = DAIPlayerAI(self.air)
            # newRoom.addAIPlayer(aiPlayer)
            pass

        self.roomList.append(newRoom)

        roomInfoList = self.getRoomInfoList()
        self.sendUpdateToAvatarId(requesterId, "setServerRoomList", [roomInfoList])

    def getServerRoomList(self):
        return self.roomList

    def getRandomPlayerName(self):
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
        roomsMatchingId = filter(lambda room: room.roomZone == roomZone, self.roomList)
        foundRoom = next(roomsMatchingId, None)
        if foundRoom.removePlayer(playerId):
            print("ALL PLAYERS LEFT")
            # all players have left the room
            self.roomList.remove(foundRoom)
            self.air.sendDeleteMsg(foundRoom.doId)

    def handleClientDisconnect(self, doId):
        print("HANDLE DISCONNECT")
        for room in self.roomList:
            print("players in room: {}".format(len(room.playerList)))
            for player in room.playerList:
                print("CHECK DISCONNECTION")
                if player.doId == doId: print("FOUND PLAYER THAT LEFT")
