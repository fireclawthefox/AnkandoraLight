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

from globalData import RoomGlobals

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
        # Client and Server
        self.gameServer = None
        self.air = None
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

        self.exitFunc = self.cleanExit

        #
        # ENTER GAMES INITIAL FSM STATE
        #
        self.request("MainMenu")

    #
    # FSM PART
    #

    ## MAIN MENU
    def enterMainMenu(self):
        self.cleanupClient()
        self.cleanupSinglePlayerServer()
        self.mainMenu = MainMenu()
        # Menu events
        self.mainMenuEvents = {
            "menu_singleplayer": [self.request, ["SinglePlayer"]],
            "menu_multiplayer": [self.request, ["SetupClient"]],
            "menu_options": [self.request, ["Options"]],
            "menu_quit": self.userExit
        }
        self.acceptDict(self.mainMenuEvents)

    def exitMainMenu(self):
        self.mainMenu.frmMenu.destroy()
        del self.mainMenu
        self.ignoreDict(self.mainMenuEvents)


    ## OPTIONS
    def enterOptions(self):
        # Show options
        self.optionsHandler = OptionsHandler()
        self.optionsEvents = {
            "options_back": [self.request, ["MainMenu"]]
        }
        self.acceptDict(self.optionsEvents)

    def exitOptions(self):
        # Hide options
        self.optionsHandler.destroy()
        del self.optionsHandler
        self.ignoreDict(self.optionsEvents)


    ## SETUP STATES
    def enterSinglePlayer(self):
        # Show single player settings
        print("run local server instance")
        # instantiate the server
        self.gameServer = GameServerRepository()
        # Room Manager
        self.air = AIRepository()

        self.setupClient("SinglePlayerCreateGame")

    def enterSetupClient(self):
        self.setupClient("Longue")


    ## SINGLE PLAYER CREATE ROOM
    def enterSinglePlayerCreateGame(self):
        self.spCreateGame = SinglePlayerCreateGameHandler()

        self.singlePlayerCreateGameEvents = {
            "singlePlayerCreateGame_back": [self.request, ["MainMenu"]],
            "singlePlayerCreateGame_createAndStart": self.startSinglePlayer
        }
        self.acceptDict(self.singlePlayerCreateGameEvents)

    def exitSinglePlayerCreateGame(self):
        self.spCreateGame.destroy()
        self.ignoreDict(self.singlePlayerCreateGameEvents)
        del self.spCreateGame


    ## LONGUE
    def enterLongue(self):
        # Show room selection
        self.roomList = RoomListHandler()
        self.showChat = True

        self.longueEvents = {
            "roomList_enterRoom": self.enterRoom,
            "roomList_createRoom": self.cr.requestCreateRoom,
            "roomList_reload": self.cr.requestRoomList,
            "roomList_back": [self.request, ["MainMenu"]],
            "updateRoomList": self.roomList.update
        }
        self.acceptDict(self.longueEvents)
        self.cr.requestRoomList()

    def exitLongue(self):
        # Hide room selection
        self.roomList.destroy()
        self.ignoreDict(self.longueEvents)
        del self.roomList


    ## GAME ROOM
    def enterGameRoom(self):
        """Starts the game room"""
        # Get our DRoom instance
        room = self.cr.doId2do[self.cr.roomId]
        self.gameOverScreen = GameOverHandler()

        # This can be used to check if the in-game gui should be shown
        self.canShowGUI = False

        # event handling
        self.gameRoomEvents = {
            "leaveRoom": self.leaveRoom,
            "rollDice": room.d_rollDice,
            "rolledDice": self.rollDice.updateRoll,
            "setNextActivePlayerName": self.turnHandler.setActivePlayer,
            "startTurn": self.turnHandler.setEndTurnActive,
            "endTurn": self.endTurn,
            "updateHealthPotions": self.inventoryHandler.setHealPotionCount,
            "disableOtherKeyboardInput": self.disableKeyboardInput,
            "enableOtherKeyboardInput": self.enableKeyboardInput,
            "gameOver": self.gameOverScreen.show,
            "startRoom": self.showTurnGui,
            "quitRoom": self.leaveRoom
        }
        self.acceptDict(self.gameRoomEvents)

        # we just need to accept this once to show up the quest related
        # information as soon as the board animation is done
        self.acceptOnce("BoardAnimationDone", self.showQuest)

        # If we are in a multiplayer game, initiate the chat system
        if self.showChat:
            self.chatHandler.start(self.cr.getRoomZone())
            self.chatHandler.hide()

    def exitGameRoom(self):
        # cleanup for game code
        # disable events
        self.ignoreDict(self.gameRoomEvents)
        self.disableKeyboardInput()

        # remove the GUI
        self.topBar.destroy()
        self.topBar = None
        self.rollDice.destroy()
        self.rollDice = None
        self.turnHandler.destroy()
        self.turnHandler = None
        if self.showChat:
            self.chatHandler.destroy()
            self.chatHandler = None
        self.inventoryHandler.destroy()
        self.inventoryHandler = None
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

    def cleanExit(self):
        """Called on exiting the application to make a clean quit from the
        server"""
        if self.cr is not None:
            self.leaveRoom()
        self.cleanupSinglePlayerServer()

    def acceptDict(self, eventDict):
        """Helper function to accept a dictionary of events.
        Key: event name
        Value: function or list [function, extra args]"""
        for event, func in eventDict.items():
            if type(func) is list:
                # func[0] = function
                # func[1] = extra args
                self.accept(event, func[0], func[1])
            else:
                self.accept(event, func)

    def ignoreDict(self, eventDict):
        for event in eventDict.keys():
            self.ignore(event)

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
        """Set up our client repository to connect to any server"""
        self.cr = GameClientRepository(self.request, newState, self.request, "MainMenu")

    def cleanupClient(self):
        # check if we even have a client repo
        if self.cr is None: return
        self.cr.stop()
        self.cr = None

    def cleanupSinglePlayerServer(self):
        """Stop and remove the local server created for a singleplayer session"""
        if self.air is not None:
            self.air.sendDisconnect()
            self.air = None

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
        """Request to create a room. This should only be called for a local
        single player instance"""
        self.singleplayerPlayerClassID = playerClassID
        self.acceptOnce("updateRoomList", self.joinSinglePlayerRoom)
        self.cr.requestCreateRoom(roomInfo)

    def joinSinglePlayerRoom(self, roomList):
        """Join the single player room that has just been created. As we
        expect to be there only one room in the room list of our local server,
        we just take the first room in the list"""
        if len(roomList) > 1:
            print("ERROR: More than one room created on local server!")
            # move back to the main menu
            self.request("MainMenu")
            return
        self.showChat = False
        # in a singleplayer environment we must always only have one room
        self.enterRoom(roomList[0], self.singleplayerPlayerClassID)

    def enterRoom(self, room, playerClassID):
        """Try to enter the given room as a player with the class of the given ID"""
        if hasattr(self, "roomList"):
            # hide the roomList if we started from the longue
            self.roomList.hide()
        elif hasattr(self, ""):
            self.spCreateGame.hide()
        self.loadingScreen = LoadingScreenHandler()
        self.questHandler = QuestHandler(room[RoomGlobals.ROOM_TYPE])
        if self.showChat:
            self.chatHandler = ChatHandler(self.cr)
        self.turnHandler = TurnHandler(self.cr)
        self.inventoryHandler = InventoryHandler()
        self.topBar = TopBarHandler(self.cr)
        self.rollDice = RollDiceHandler()
        self.acceptOnce("roomManager_joinFailed", self.joinRoomFailed)
        self.acceptOnce("roomManager_loaded", self.request, ["GameRoom"])
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
        self.request("MainMenu")

    def endTurn(self):
        room = self.cr.doId2do[self.cr.roomId]
        room.d_endTurn()
        self.rollDice.clearRoll()

    #
    # BASIC END
    #

    #
    # GameRoom state related functions
    #
    def disableKeyboardInput(self):
        """Disable the in-game events for keyboard mapping"""
        self.ignore("d")
        self.ignore("space")

    def enableKeyboardInput(self):
        """Enable the in-game events for keyboard mapping"""
        room = self.cr.doId2do[self.cr.roomId]
        self.accept("d", room.d_rollDice)
        self.accept("space", self.endTurn)

    def showQuest(self):
        """Show the quest related information"""
        self.questHandler.show(self.showGUI)

    def showGUI(self):
        """Show the main in-game GUI"""
        self.canShowGUI = True
        self.questHandler.hide()
        if self.showChat:
            # only show the chat in multiplayer games
            self.chatHandler.show()
        self.topBar.show()
        self.inventoryHandler.show()

    def showTurnGui(self):
        """Show the turn related GUI elements.  This should be called as soon as
        the room is ready (all players are in).  It will check itself if the GUI
        should actually be shown or if the quest display is still up"""
        if self.canShowGUI:
            self.turnHandler.show()
            self.rollDice.show()
        else:
            taskMgr.doMethodLater(0.5, self.showTurnGui, "delayedShowTurnGui", extraArgs=[])

        # accept keyboard events for the turn handling
        self.enableKeyboardInput()
# CLASS Main END

#
# START GAME
#
Game = Main()
Game.run()
