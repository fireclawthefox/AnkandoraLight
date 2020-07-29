from panda3d.core import ConfigVariableString
from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG

from gui.Options import GUI as Options

class OptionsHandler(DirectObject, Options):
    def __init__(self):
        Options.__init__(self)

        self.accept("options_ok", self.ok)
        self.accept("options_cancel", self.cancel)

        self.txtServer.enterText(base.serverHost.getValue())

    def ok(self):
        serverUrl = self.txtServer.get()
        base.serverHost.setValue(serverUrl)

    def cancel(self):
        pass
