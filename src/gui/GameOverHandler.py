from gui.GameOver import GUI as GameOver
from direct.gui import DirectGuiGlobals as DGG

class GameOverHandler():
    def __init__(self):

        self.gameOver = GameOver()
        self.gameOver.frmMain["text_scale"] = 0.07
        self.gameOver.frmMain["frameSize"] = [base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop]
        self.gameOver.frmMain["state"] = DGG.NORMAL
        self.gameOver.frmMain.setState()
        self.hide()

    def setEndMessage(self, msg):
        self.gameOver.lblMessage["text"] = msg

    def show(self, msg):
        self.setEndMessage(msg)
        self.gameOver.show()

    def hide(self):
        self.gameOver.hide()

    def destroy(self):
        self.gameOver.destroy()
