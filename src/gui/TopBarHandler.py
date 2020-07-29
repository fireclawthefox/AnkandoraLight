from direct.showbase.DirectObject import DirectObject
from gui.TopBar import GUI as TopBar

class TopBarHandler(DirectObject):
    def __init__(self, cr):
        self.cr = cr
        self.bar = TopBar(base.a2dTopLeft)
        self.accept(self.cr.uniqueName("setPlayerName"), self.setPlayerName)

        self.hide()

    def destroy(self):
        self.bar.frmMain.removeNode()
        del self.bar

    def setPlayerName(self, playerName):
        self.bar.lblPlayerName["text"] = playerName

    def show(self):
        self.bar.frmMain.show()

    def hide(self):
        self.bar.frmMain.hide()
