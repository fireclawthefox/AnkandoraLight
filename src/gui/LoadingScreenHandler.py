
from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG

from gui.LoadingScreen import GUI as LoadingScreen

class LoadingScreenHandler(DirectObject):
    def __init__(self):
        self.loadingScreen = LoadingScreen()
        self.loadingScreen.frmMain["frameSize"] = [base.a2dLeft, base.a2dRight, base.a2dBottom, base.a2dTop]
        self.loadingScreen.frmMain["sortOrder"] = 1000
        self.loadingScreen.frmMain["state"] = DGG.NORMAL
        self.loadingScreen.frmMain.setState()
        self.wb = self.loadingScreen.waitbar
        self.reset()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

        self.accept("registerLoadEvent", self.registerLoadEvent)

    def delete(self):
        self.ignoreAll()
        self.loadingScreen.frmMain.hide()
        self.loadingScreen.frmMain.removeNode()

    def reset(self):
        self.wb["value"] = 0
        self.numLoadEvents = 0
        self.step = self.wb["range"]
        self.waitBarLocked = False

    def registerLoadEvent(self, loadDoneEvent):
        if self.waitBarLocked: return False
        self.acceptOnce(loadDoneEvent, self.updateWaitbar)

        self.numLoadEvents += 1

        self.step = self.wb["range"] / self.numLoadEvents
        return True

    def updateWaitbar(self):
        self.waitBarLocked = True
        self.wb["value"] += self.step

        if self.wb["value"] == self.wb["range"]:
            self.loadingScreen.frmMain.hide()
