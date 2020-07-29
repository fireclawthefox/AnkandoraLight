from direct.showbase.DirectObject import DirectObject
from gui.SinglePlayerCreateGame import GUI as SinglePlayerCreateGame

from globalData import RoomGlobals

class SinglePlayerCreateGameHandler(DirectObject):
    def __init__(self):
        self.spCreateGame = SinglePlayerCreateGame()
        self.spCreateGame.optionPlayerClass["items"] = RoomGlobals.ALL_PLAYERCLASSES_AS_NAMES
        self.spCreateGame.optionNumNPCs["items"] = ["0", "1","2","3"]
        self.spCreateGame.optionGameType["items"] = RoomGlobals.ALL_GAMETYPES_AS_NAMES

        self.accept("singlePlayerCreateGame_start", self.create)

    def create(self):
        name = "SingleplayerGame"
        numPlayers = 1
        aiPlayerCount = int(self.spCreateGame.optionNumNPCs.get())
        gameTypeStr = self.spCreateGame.optionGameType.get()
        playerClassID = RoomGlobals.Name2PlayerClassID[self.spCreateGame.optionPlayerClass.get()]
        gameType = 0
        if gameTypeStr == "Normal":
            gameType = RoomGlobals.GAMETYPE_NORMAL
        elif gameTypeStr == "Race":
            gameType = RoomGlobals.GAMETYPE_RACE
        room = (name, numPlayers, 0, aiPlayerCount, gameType, 0)
        base.messenger.send("singlePlayerCreateGame_createAndStart", [room, playerClassID])

    def destroy(self):
        self.spCreateGame.destroy()
        del self.spCreateGame

    def show(self):
        self.spCreateGame.show()

    def hide(self):
        self.spCreateGame.hide()
