from direct.distributed.DistributedObject import DistributedObject

class DRoom(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        print("OPENED UP ROOM")

    def announceGenerate(self):
        self.cr.localRoomId = self.doId
        DistributedObject.announceGenerate(self)

        self.accept("requestMoveToField", self.d_requestMoveToField)

    def d_rollDice(self):
        self.sendUpdate("rollDice")

    def nextPlayer(self, playerName):
        base.messenger.send("setNextActivePlayerName", [playerName])

    def d_endTurn(self):
        self.sendUpdate("endTurn")

    def endTurn(self):
        """ End this players turn """
        base.messenger.send("endThisPlayerTurn", [])

    def startTurn(self):
        """ Start this players turn """
        print("START THIS PLAYERS TURN")
        base.messenger.send("startTurn", [])

    def rolledDice(self, roll):
        base.messenger.send("rolledDice", [roll])

    def updateRolledDice(self, remainingRoll):
        print("HERE?! RE_DICE", remainingRoll)
        base.messenger.send("rolledDice", [remainingRoll])

    def rolledDiceFailed(self):
        print("can't roll dice now")

    def d_requestMoveToField(self, fieldName):
        self.sendUpdate("requestMoveToField", [fieldName])

    def gameOver(self, winningPlayerName):
        msg = ""
        if winningPlayerName == "ALL":
            msg = "You Won!"
        else:
            msg = "Player\n{}\nwon!".format(winningPlayerName)
        base.messenger.send("gameOver", [msg])

    def startBattle(self):
        print("START BATTLE")
        # TODO: Make sure the players can't do anything than looking for the batle

    def endBattle(self, won):
        print("END BATTLE")
        print("Player won:", won)

    def spectateBattle(self):
        print("SPECtATE BATTLE")
        # TODO: Make sure the players can't do anything than looking for the batle

    def endSpectateBattle(self):
        print("END SPECTATE BATTLE")
