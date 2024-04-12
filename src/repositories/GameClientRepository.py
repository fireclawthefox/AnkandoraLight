#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.ClientRepository import ClientRepository
from panda3d.core import URLSpec, ConfigVariableInt, ConfigVariableString
from globalData import RoomGlobals, ZonesGlobals

class GameClientRepository(ClientRepository):

    def __init__(self, readyCommand, readyCommandArgs, failedCommand, failedCommandArgs):
        dcFileNames = ["interfaces/direct.dc", "interfaces/gameRoom.dc", "interfaces/chat.dc"]
        ClientRepository.__init__(
            self,
            dcFileNames = dcFileNames,
            threadedNet = True)

        self.roomManager = None
        self.readyCommand = readyCommand
        self.readyCommandArgs = readyCommandArgs
        self.failedCommand = failedCommand
        self.failedCommandArgs = failedCommandArgs

        hostname = base.serverHost.getValue()
        self.url = URLSpec('http://{}'.format(hostname))
        self.connect([self.url],
                     successCallback = self.connectSuccess,
                     failureCallback = self.connectFailure)

    def lostConnection(self):
        base.messenger.send("client_lost_connection")

    def connectFailure(self, statusCode, statusString):
        """ some error occured while try to connect to the server """
        print("Failed to connect to %s: %s."
                % (self.url, statusString))
        base.messenger.send("client_lost_connection")
        self.failedCommand(self.failedCommandArgs)

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """
        print("Connection established, waiting for timesync.")
        self.acceptOnce(self.uniqueName("gotTimeSync"), self.syncReady)
        self.setInterestZones([ZonesGlobals.SERVER_MANAGERS])

    def syncReady(self):
        """ Now we've got the TimeManager manifested, and we're in
        sync with the server time.  Now we can enter the world.  Check
        to see if we've received our doIdBase yet. """

        # This method checks whether we actually have a valid doID range
        # to create distributed objects yet
        if self.haveCreateAuthority():
            # we already have one
            self.gotCreateReady()
        else:
            # Not yet, keep waiting a bit longer.
            self.accept(self.uniqueName('createReady'), self.gotCreateReady)

    def gotCreateReady(self):
        """ Ready to enter the world.  Expand our interest to include
        any other zones """

        # This method checks whether we actually have a valid doID range
        # to create distributed objects yet
        if not self.haveCreateAuthority():
            # Not ready yet.
            return

        # we are ready now, so ignore further createReady events
        self.ignore(self.uniqueName('createReady'))

        self.acceptOnce(self.uniqueName("roomManager_ready"), self.roomManagerReady)
        self.setInterestZones([ZonesGlobals.SERVER_MANAGERS, ZonesGlobals.ROOM_MANAGER_ZONE])

    def getMyName(self):
        return self.doId2do[self.localPlayerId].name

    def roomManagerReady(self):
        self.readyCommand(self.readyCommandArgs)

    def stop(self):
        self.sendDisconnect()

    def requestEnterRoom(self, room, playerClassID):
        roomID = room[RoomGlobals.ROOM_ID]
        self.roomManager.d_requestJoin(roomID, playerClassID)

    def requestLeaveRoom(self):
        self.roomManager.d_requestLeave()

    def requestCreateRoom(self, roomInfo):
        self.roomManager.d_requestCreateRoom(roomInfo)

    def requestRoomList(self):
        self.roomManager.d_requestRoomList()

    def getRoomZone(self):
        return self.roomManager.roomZone
