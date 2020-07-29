
from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG

from gui.RollDice import GUI as RollDice

class RollDiceHandler(DirectObject):
    def __init__(self):
        self.rollDice = RollDice(base.a2dBottomLeft)
        self.hide()

    def destroy(self):
        self.rollDice.destroy()

    def updateRoll(self, roll):
        self.rollDice.btnRollDice["text"] = str(roll)

    def clearRoll(self):
        self.rollDice.btnRollDice["text"] = ""

    def show(self):
        self.rollDice.btnRollDice.show()

    def hide(self):
        self.rollDice.btnRollDice.hide()
