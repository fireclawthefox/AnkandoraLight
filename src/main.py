#!/usr/bin/python
# -*- coding: utf-8 -*-
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
from audio.AudioManager import AudioManager
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

# Global Data
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

        self.setBackgroundColor(0,0,0)

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
        self.canStartClient = True
        self.gameServer = None
        self.air = None
        self.cr = None

        # Audio
        self.audioMgr = AudioManager()

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
        """Build up the main menu GUI"""
        base.messenger.send("playAudioMenu")

        # make sure we're clean when we go back to the main menu
        self.cleanupClient()
        self.cleanupSinglePlayerServer()

        # create the menu GUI
        self.mainMenu = MainMenu()

        # Menu events
        self.mainMenuEvents = {
            "menu_singleplayer": [self.request, ["SinglePlayer"]],
            "menu_multiplayer": [self.request, ["SetupClient"]],
            "menu_options": [self.request, ["Options"]],
            "menu_quit": self.__quitApplication
        }
        self.acceptDict(self.mainMenuEvents)

    def exitMainMenu(self):
        """Cleanup the main menu GUI"""
        self.mainMenu.destroy()
        del self.mainMenu
        self.ignoreDict(self.mainMenuEvents)


    ## OPTIONS
    def enterOptions(self):
        """Build up the options GUI"""
        # Show options
        self.optionsHandler = OptionsHandler()
        self.optionsEvents = {
            "options_back": [self.request, ["MainMenu"]]
        }
        self.acceptDict(self.optionsEvents)

    def exitOptions(self):
        """Clean up the options GUI"""
        # Hide options
        self.optionsHandler.destroy()
        del self.optionsHandler
        self.ignoreDict(self.optionsEvents)


    ## SETUP STATES
    def enterSinglePlayer(self):
        """Setup the local server for single player usage"""
        # instantiate the server
        self.gameServer = GameServerRepository()
        # Room Manager
        self.air = AIRepository()

        # set up the client related things. This is the same for single- and
        # multiplayer, we just pass in the next state we want to go to
        self.setupClient("SinglePlayerCreateGame")

    def enterSetupClient(self):
        """Setup the client for multiplayer usage"""
        # after setting up the client we want to go to the longue
        self.setupClient("Longue")

    ## SINGLE PLAYER CREATE ROOM
    def enterSinglePlayerCreateGame(self):
        """Setup the single player setup GUI"""
        # Create the GUI for setting up a single player game
        self.spCreateGame = SinglePlayerCreateGameHandler()

        # accept the GUI events
        self.singlePlayerCreateGameEvents = {
            "singlePlayerCreateGame_back": [self.request, ["MainMenu"]],
            "singlePlayerCreateGame_createAndStart": self.startSinglePlayer
        }
        self.acceptDict(self.singlePlayerCreateGameEvents)

    def exitSinglePlayerCreateGame(self):
        """Clean up the single player setup GUI"""
        self.spCreateGame.destroy()
        self.ignoreDict(self.singlePlayerCreateGameEvents)
        del self.spCreateGame


    ## MULTIPLAYER LONGUE
    def enterLongue(self):
        """Setup the multiplayer longue GUI"""
        # Show longue aka roomlist
        self.roomList = RoomListHandler()

        # In a multiplayer game we want to see the chat frame
        self.showChat = True

        # accept the GUI events
        self.longueEvents = {
            "roomList_enterRoom": self.enterRoom,
            "roomList_createRoom": self.cr.requestCreateRoom,
            "roomList_reload": self.cr.requestRoomList,
            "roomList_back": [self.request, ["MainMenu"]],
            "updateRoomList": self.roomList.update
        }
        self.acceptDict(self.longueEvents)

        # send initial request to the server so we see already created rooms
        # after opening the longue
        self.cr.requestRoomList()

    def exitLongue(self):
        """Cleanu up multiplayer longue GUI"""
        # Hide room selection
        self.roomList.destroy()
        # ignore any further events from that GUI
        self.ignoreDict(self.longueEvents)
        del self.roomList


    ## GAME ROOM
    def enterGameRoom(self):
        """Starts the game room"""
        base.messenger.send("playAudioGame")
        # Get our DRoom instance
        room = self.cr.doId2do[self.cr.roomId]

        # The screen which will be shown once the game has ended
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
        """Clean the room and all the GUI elements that come with it"""
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

    def __quitApplication(self):
        base.exitFunc = self.writeConfig
        self.userExit()

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
        """Ignore a given set of events. Can be called with the same
        dicts given to the acceptDict function"""
        for event in eventDict.keys():
            self.ignore(event)

    def __escape(self):
        """Handle user escape key klicks"""
        if self.state == "MainMenu":
            # In this state, we will stop the application
            self.userExit()
        elif self.state == "GameRoom":
            # Nothing to do here yet
            pass
        else:
            # In every other state, we switch back to the Game state
            self.request("MainMenu")

    #
    # BASIC END
    #

    #
    # CLIENT/SERVER RELATED FUNCTIONS
    #

    def cleanExit(self):
        """Called on exiting the application to make a clean quit from the
        server"""
        if self.cr is not None:
            self.leaveRoom()
        self.cleanupSinglePlayerServer()

    def setupClient(self, newState):
        """Set up our client repository to connect to any server"""
        print(self.canStartClient)
        if not self.canStartClient:
            self.request("MainMenu")
            return
        self.cr = GameClientRepository(
            self.request, newState, self.request, "MainMenu")

    def cleanupClient(self):
        """Stop the client and remove it"""
        self.canStartClient = False
        # check if we even have a client repo
        if self.cr is None:
            self.canStartClient = True
            return

        for obj in self.cr.doId2do.values():
            obj.sendDeleteMsg()

        for doId, do in self.cr.doId2do.copy().items():
            # hard delete of all objects as we're going to kill the client
            # anyway
            self.cr.deleteObject(doId)
        self.cr.stop()
        del self.cr
        self.cr = None
        self.canStartClient = True

    def cleanupSinglePlayerServer(self):
        """Stop and remove the local server created for a singleplayer
        session"""
        # clean the AI Repository
        if self.air is not None:
            self.air.sendDisconnect()
            self.air = None

        # clean the Game server
        if self.gameServer is not None:
            # as there is no easy way to clean up a server yet, we have to do
            # this manually...

            # remove all created connection handling variables
            del self.gameServer.cw
            del self.gameServer.qcr
            del self.gameServer.qcl
            del self.gameServer.qcm
            # not sure if this has to be done but better save than sorry
            self.gameServer.cw = None
            self.gameServer.qcr = None
            self.gameServer.qcl = None
            self.gameServer.qcm = None

            # remove the tasks, the server has spawned
            taskMgr.remove("serverListenerPollTask")
            taskMgr.remove("serverReaderPollTask")
            taskMgr.remove("clientHardDisconnect")
            taskMgr.remove("flushTask")

            # finally delete the game server
            del self.gameServer

        # make sure everything is set to None for later checks and usage
        self.gameServer = None
        self.gameAIServer = None

    def startSinglePlayer(self, roomInfo, playerClassID):
        """Request to create a room. This should only be called for a local
        single player instance"""
        # store the Players selected Class (e.g. Warrior, Archer, etc.)
        self.singleplayerPlayerClassID = playerClassID
        self.acceptOnce("updateRoomList", self.joinSinglePlayerRoom)
        # create our room for this single player match. This should be the only
        # room to be created on this server.
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
        """Try to enter the given room as a player with the class of
        the given ID"""
        if hasattr(self, "roomList"):
            # hide the roomList if we started from the longue
            self.roomList.hide()
        elif hasattr(self, ""):
            self.spCreateGame.hide()

        # setup the loading screen
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
        """If something went wrong joining the room, we should land here"""
        # check if we were in the longue
        if hasattr(self, "roomList"):
            # if so, show the longue again
            self.roomList.show()
        # if this was a single player try
        elif hasattr(self, "spCreateGame"):
            # show the create game window again
            self.spCreateGame.show()

        # clean up the loading screen
        self.loadingScreen.destroy()
        del self.loadingScreen
        self.loadingScreen = None

    #
    # CLIENT/SERVER RELATED FUNCTIONS END
    #

    #
    # GAMEROOM STATE RELATED FUNCTIONS
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

        self.cr.roomManager.setPlayerReady()

    def showTurnGui(self):
        """Show the turn related GUI elements.  This should be called as soon as
        the room is ready (all players are in).  It will check itself if the GUI
        should actually be shown or if the quest display is still up"""
        if self.canShowGUI:
            # we can show the GUI so, do so.
            self.turnHandler.show()
            self.rollDice.show()
        else:
            # We have to wait until we can so the GUI. Check every 0.5 seconds
            # we we can show the GUI then.
            taskMgr.doMethodLater(
                0.5, self.showTurnGui, "delayedShowTurnGui", extraArgs=[])

        # accept keyboard events for the turn handling
        self.enableKeyboardInput()

    def endTurn(self):
        """Request ending the turn for this player"""
        base.messenger.send("playSFXEndTurn")
        room = self.cr.doId2do[self.cr.roomId]
        room.d_endTurn()
        self.rollDice.clearRoll()

    def leaveRoom(self):
        """Request leaving the room and go back to the main menu"""
        self.cr.requestLeaveRoom()
        self.request("MainMenu")
    #
    # GAMEROOM STATE RELATED FUNCTIONS END
    #
# CLASS Main END

#
# START GAME
#
Game = Main()
Game.run()
