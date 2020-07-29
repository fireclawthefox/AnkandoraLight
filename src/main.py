#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

# Python imports

# Panda3D imoprts
from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM
from panda3d.core import CollisionTraverser

import simplepbr

# Game imports
from config import config
from gui.MainMenu import GUI as MainMenu
from gui.RoomListHandler import RoomListHandler
from gui.SinglePlayerCreateGameHandler import SinglePlayerCreateGameHandler
from gui.QuestHandler import QuestHandler
from gui.ChatHandler import ChatHandler
from gui.RollDiceHandler import RollDiceHandler
from gui.TopBarHandler import TopBarHandler
from gui.TurnHandler import TurnHandler
from gui.InventoryHandler import InventoryHandler
from gui.LoadingScreenHandler import LoadingScreenHandler
from gui.GameOverHandler import GameOverHandler
from gui.OptionsHandler import OptionsHandler

# For Multiplayer
from repositories.GameClientRepository import GameClientRepository

# For Singleplayer local server
from repositories.GameServerRepository import GameServerRepository
from repositories.AIRepository import AIRepository

#
# MAIN GAME CLASS
#
class Main(ShowBase, FSM, config.Config):
    """Main function of the application
    initialise the engine (ShowBase)"""

    def __init__(self):
        """initialise the engine"""
        ShowBase.__init__(self)
        base.notify.info("Version {}".format(config.versionstring))
        FSM.__init__(self, "FSM-Game")
        config.Config.__init__(self)

        #
        # PBR SHADING
        #
        pipeline = simplepbr.init()
        pipeline.use_normals_map = True
        pipeline.enable_shadows = True

        #
        # INITIALIZE GAME CONTENT
        #
        self.gameServer = None
        self.gameAIServer = None
        self.cr = None
        # show or hide the game chat
        self.showChat = True

        #
        # EVENT HANDLING
        #
        # By default we accept the escape key
        self.accept("escape", self.__escape)

        #
        # COLLISION DETECTION
        #
        base.cTrav = CollisionTraverser()
        #base.cTrav.showCollisions(base.render)

        #
        # ENTER GAMES INITIAL FSM STATE
        #
        self.request("MainMenu")

    #
    # FSM PART
    #

    def enterMainMenu(self):
        self.cleanupClient()
        self.cleanupSinglePlayerServer()
        self.mainMenu = MainMenu()
        # Menu events
        self.accept("menu_singleplayer", self.request, ["SinglePlayer"])
        self.accept("menu_multiplayer", self.request, ["SetupClient"])
        self.accept("menu_options", self.request, ["Options"])
        self.accept("menu_quit", self.userExit)

    def exitMainMenu(self):
        self.mainMenu.frmMenu.destroy()
        del self.mainMenu
        self.ignore("menu_singleplayer")
        self.ignore("menu_multiplayer")
        self.ignore("menu_options")
        self.ignore("menu_quit")

    def enterOptions(self):
        # Show options
        self.optionsHandler = OptionsHandler()
        self.accept("options_ok", self.request, ["MainMenu"])
        self.accept("options_cancel", self.request, ["MainMenu"])

    def exitOptions(self):
        # Hide options
        self.optionsHandler.destroy()
        del self.optionsHandler
        self.ignore("options_ok")
        self.ignore("options_cancel")

    def enterSinglePlayer(self):
        # Show single player settings
        print("run local server instance")
        # instantiate the server
        self.gameServer = GameServerRepository()
        # Room Manager
        self.air = AIRepository()

        self.setupClient("SinglePlayerCreateGame")

    def enterSinglePlayerCreateGame(self):
        self.spCreateGame = SinglePlayerCreateGameHandler()

        self.accept("singlePlayerCreateGame_back", self.request, ["MainMenu"])
        self.accept("singlePlayerCreateGame_createAndStart", self.startSinglePlayer)

    def exitSinglePlayerCreateGame(self):
        self.spCreateGame.destroy()
        self.ignore("singlePlayerCreateGame_back")
        self.ignore("singlePlayerCreateGame_createAndStart")
        del self.spCreateGame

    def enterSetupClient(self):
        self.setupClient("Longue")

    def enterLongue(self):
        # Show room selection
        self.roomList = RoomListHandler()
        self.showChat = True

        self.accept("roomList_enterRoom", self.enterRoom)
        self.accept("roomList_createRoom", self.cr.requestCreateRoom)
        self.accept("roomList_reload", self.cr.requestRoomList)
        self.accept("roomList_back", self.request, ["MainMenu"])

        self.accept("updateRoomList", self.roomList.update)
        self.cr.requestRoomList()

    def exitLongue(self):
        # Hide room selection
        self.roomList.destroy()
        self.ignore("roomList_enterRoom")
        self.ignore("roomList_createRoom")
        self.ignore("roomList_back")
        self.ignore("updateRoomList")
        del self.roomList

    def disableKeyboardInput(self):
        self.ignore("d")
        self.ignore("space")
    def enableKeyboardInput(self):
        room = self.cr.doId2do[self.cr.roomId]
        self.accept("d", room.d_rollDice)
        self.accept("space", self.endTurn)
    def enterGameRoom(self):
        room = self.cr.doId2do[self.cr.roomId]
        self.accept("leaveRoom", self.leaveRoom)
        self.accept("rollDice", room.d_rollDice)
        self.accept("rolledDice", self.rollDice.updateRoll)
        self.accept("setNextActivePlayerName", self.turnHandler.setActivePlayer)
        self.accept("startTurn", self.turnHandler.setEndTurnActive)
        self.accept("endTurn", self.endTurn)
        self.enableKeyboardInput()
        self.accept("updateHealthPotions", self.inventoryHandler.setHealPotionCount)
        self.accept("disableOtherKeyboardInput", self.disableKeyboardInput)
        self.accept("enableOtherKeyboardInput", self.enableKeyboardInput)
        self.questHandler.show()
        if self.showChat:
            self.chatHandler.start(self.cr.getRoomZone())
            self.chatHandler.show()
        self.turnHandler.show()
        self.topBar.show()
        self.rollDice.show()
        self.inventoryHandler.show()

        self.gameOverScreen = GameOverHandler()
        self.accept("gameOver", self.gameOverScreen.show)

    def exitGameRoom(self):
        # cleanup for game code
        self.ignore("leaveRoom")
        self.ignore("rollDice")
        self.ignore("rolledDice")
        self.ignore("setNextActivePlayerName")
        self.ignore("startTurn")
        self.ignore("endTurn")
        self.ignore("d")
        self.ignore("space")
        self.ignore("updateHealthPotions")

        self.topBar.destroy()
        self.topBar = None
        self.rollDice.destroy()
        self.rollDice = None
        self.turnHandler.destroy()
        self.turnHandler = None
        if self.showChat:
            self.chatHandler.destroy()
            self.chatHandler = None
        self.questHandler.destroy()
        self.questHandler = None
        self.gameOverScreen.destroy()
        self.gameOverScreen = None

    #
    # FSM PART END
    #

    #
    # BASIC FUNCTIONS
    #

    def __escape(self):
        """Handle user escape key klicks"""
        if self.state == "MainMenu":
            # In this state, we will stop the application
            self.userExit()
        elif self.state == "GameRoom":
            #TODO: we need to check what the player actually want to do here, probably open in game menu
            pass
        else:
            # In every other state, we switch back to the Game state
            self.request("MainMenu")

    def setupClient(self, newState):
        self.cr = GameClientRepository(self.request, newState, self.request, "MainMenu")

    def cleanupClient(self):
        if self.cr is None: return

        self.cr.stop()
        self.cr = None

    def cleanupSinglePlayerServer(self):

        if self.gameAIServer is not None:
            self.gameAIServer.sendDisconnect()
            del self.gameAIServer

        if self.gameServer is not None:
            del self.gameServer.cw
            del self.gameServer.qcr
            del self.gameServer.qcl
            del self.gameServer.qcm
            self.gameServer.cw = None
            self.gameServer.qcr = None
            self.gameServer.qcl = None
            self.gameServer.qcm = None

            taskMgr.remove("serverListenerPollTask")
            taskMgr.remove("serverReaderPollTask")
            taskMgr.remove("clientHardDisconnect")
            taskMgr.remove("flushTask")

            del self.gameServer

        self.gameServer = None
        self.gameAIServer = None

    def startSinglePlayer(self, roomInfo, playerClassID):
        self.singleplayerPlayerClassID = playerClassID
        self.accept("updateRoomList", self.joinSinglePlayerRoom)
        self.cr.requestCreateRoom(roomInfo)

    def joinSinglePlayerRoom(self, roomList):
        self.showChat = False
        self.ignore("updateRoomList")
        # in a singleplayer environment we must always only have one room
        self.enterRoom(roomList[0], self.singleplayerPlayerClassID)

    def enterRoom(self, room, playerClassID):
        print("ENTER ROOM")
        if hasattr(self, "roomList"):
            self.roomList.hide()
        elif hasattr(self, ""):
            self.spCreateGame.hide()
        self.loadingScreen = LoadingScreenHandler()
        self.questHandler = QuestHandler()
        if self.showChat:
            self.chatHandler = ChatHandler(self.cr)
        self.turnHandler = TurnHandler(self.cr)
        self.inventoryHandler = InventoryHandler()
        self.topBar = TopBarHandler(self.cr)
        self.rollDice = RollDiceHandler()
        self.accept("roomManager_joinFailed", self.joinRoomFailed)
        self.accept("roomManager_loaded", self.request, ["GameRoom"])
        self.cr.requestEnterRoom(room, playerClassID)

    def joinRoomFailed(self):
        if hasattr(self, "roomList"):
            self.roomList.show()
        elif hasattr(self, ""):
            self.spCreateGame.show()
        self.loadingScreen.delete()
        del self.loadingScreen
        self.loadingScreen = None

    def leaveRoom(self):
        self.cr.requestLeaveRoom()
        print("NOW REQUESTING MAIN MENU")
        self.request("MainMenu")

    def endTurn(self):
        room = self.cr.doId2do[self.cr.roomId]
        room.d_endTurn()
        self.rollDice.clearRoll()

    #
    # BASIC END
    #
# CLASS Main END

#
# START GAME
#
Game = Main()
Game.run()
