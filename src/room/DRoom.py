from direct.distributed.DistributedObject import DistributedObject
from direct.gui.DirectDialog import YesNoDialog

class DRoom(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        print("OPENED UP ROOM")

    def announceGenerate(self):
        self.cr.localRoomId = self.doId
        DistributedObject.announceGenerate(self)

        self.accept("requestMoveToField", self.d_requestMoveToField)

    def startRoom(self):
        print("SEND START ROOM")
        base.messenger.send("startRoom")

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

    def canInitiateFight(self):
        print("CAN INITIATE ROOM")
        base.messenger.send("canInitiateFight")

        self.dlgStartFight = YesNoDialog(
            state='normal',
            text='Start Fight?',
            fadeScreen=True,
            command=self.doInitiateFight
        )

    def doInitiateFight(self, yes):
        if yes:
            self.d_initiateFight()
        self.dlgStartFight.cleanup()
        self.dlgStartFight = None

    def d_initiateFight(self):
        self.sendUpdate("initiateFight")

    def startBattle(self):
        print("START BATTLE")

    def endBattle(self, won):
        print("END BATTLE")
        print("Player won:", won)

    def spectateBattle(self):
        print("SPECtATE BATTLE")

    def endSpectateBattle(self):
        print("END SPECTATE BATTLE")
