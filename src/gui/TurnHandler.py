from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG
from gui.Turn import GUI as Turn

class TurnHandler(DirectObject):
    def __init__(self, cr):
        self.cr = cr
        self.turn = Turn(base.a2dBottomCenter)
        self.turn.hide()

        self.hide()

    def destroy(self):
        self.turn.destroy()
        del self.turn

    def setActivePlayer(self, playerName):
        self.turn.btnEndTurn["text"] = playerName
        self.turn.btnEndTurn["image"] = "./assets/Turn/EndTurn_disabled.png"
        self.turn.btnEndTurn["state"] = DGG.DISABLED
        self.turn.show()

    def setEndTurnActive(self):
        self.turn.btnEndTurn["text"] = "End Turn"
        self.turn.btnEndTurn["image"] = "./assets/Turn/EndTurn.png"
        self.turn.btnEndTurn["state"] = DGG.NORMAL
        self.turn.show()

    def show(self):
        self.turn.btnEndTurn.show()

    def hide(self):
        self.turn.btnEndTurn.hide()
