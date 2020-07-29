from direct.distributed.ServerRepository import ServerRepository
from panda3d.core import ConfigVariableInt

class GameServerRepository(ServerRepository):
    """The server repository class"""
    def __init__(self):
        """initialise the server class"""
        print("SETUP SERVER")
        tcpPort = ConfigVariableInt("server-port", 4400)
        dcFileNames = ["interfaces/direct.dc", "interfaces/gameRoom.dc", "interfaces/chat.dc"]
        ServerRepository.__init__(self, tcpPort, dcFileNames = dcFileNames)
        print("SETUP SERVER DONE")
