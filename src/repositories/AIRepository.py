from direct.distributed.ClientRepository import ClientRepository
from panda3d.core import URLSpec, ConfigVariableInt, ConfigVariableString
from globalData import ZonesGlobals

class AIRepository(ClientRepository):
    def __init__(self):
        print("SETUP AI REPOSITORY")
        dcFileNames = ["interfaces/direct.dc", "interfaces/gameRoom.dc", "interfaces/chat.dc"]

        ClientRepository.__init__(
            self,
            dcFileNames = dcFileNames,
            dcSuffix = 'AI',
            threadedNet = True)

        hostname = base.serverHost.getValue()
        print("CONNECT TO:", hostname)
        url = URLSpec('http://{}'.format(hostname))
        self.connect([url],
                     successCallback = self.connectSuccess,
                     failureCallback = self.connectFailure)

    def connectFailure(self, statusCode, statusString):
        raise Exception(statusString)

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """
        self.accept('createReady', self.gotCreateReady)

    def lostConnection(self):
        """ This should be overridden by a derived class to handle an
        unexpectedly lost connection to the gameserver. """
        exit()

    def gotCreateReady(self):
        """ Now we're ready to go! """

        # This method checks whether we actually have a valid doID range
        # to create distributed objects yet
        if not self.haveCreateAuthority():
            # Not ready yet.
            return

        # we are ready now, so ignore further createReady events
        self.ignore('createReady')

        # Create a Distributed Object by name.  This will look up the object in
        # the dc files passed to the repository earlier
        self.timeManager = self.createDistributedObject(
            className = 'TimeManagerAI',
            zoneId = ZonesGlobals.SERVER_MANAGERS)

        self.roomManager = self.createDistributedObject(
            className = 'DRoomManagerAI',
            zoneId = ZonesGlobals.ROOM_MANAGER_ZONE)

        print("AI Repository Ready")
        print("SETUP AI REPOSITORY DONE")

    def deallocateChannel(self, doID):
        """ This method will be called whenever a client disconnects from the
        server.  The given doID is the ID of the client who left us. """
        print("Client left us: ", doID)
