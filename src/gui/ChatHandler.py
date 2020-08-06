from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import (TextNode,
    TextProperties,
    TextPropertiesManager)

from gui.Chat import GUI as Chat

class ChatHandler(DirectObject):
    def __init__(self, cr):
        base.messenger.send("registerLoadEvent", ["loadChatDone"])

        self.cr = cr

        self.chat = Chat(base.a2dTopRight)
        self.chat.frmChat.hide()
        self.chat.frmChat.setPos(
            -self.chat.frmChat["frameSize"][1],
            self.chat.frmChat.getY(),
            self.chat.frmChat.getZ())
        self.chat.btnToggleChat.hide()
        self.chat.btnToggleChat.setPos(
            -self.chat.btnToggleChat["frameSize"][1],
            self.chat.btnToggleChat.getY(),
            self.chat.btnToggleChat.getZ())
        self.btnToggleChatOrigTextFG = self.chat.btnToggleChat.component("text1").fg


        self.chat.btnToggleChat["sortOrder"] = 990
        self.chat.frmChat["sortOrder"] = 990

        self.chat.txtMessage["focusInCommand"] = self.focusInCommandFunc
        self.chat.txtMessage["focusOutCommand"] = self.focusOutCommandFunc
        self.chat.txtMessage["command"] = self.sendMessage

        tpMgr = TextPropertiesManager.getGlobalPtr()
        tpBold = TextProperties()
        font = loader.loadFont("assets/fonts/OldaniaADFStd-Bold.otf")
        tpBold.setFont(font)
        tpMgr.setProperties("bold", tpBold)


        self.lblMessages = OnscreenText(
            text="\1bold\1Messages:\2",
            scale = 0.05,
            pos = (self.chat.frmMessages["canvasSize"][0], -0.05),
            align = TextNode.ALeft,
            wordwrap = 14,
            parent = self.chat.frmMessages.getCanvas())

        self.accept("sendMessage", self.sendMessage)
        self.accept("setText", self.addMessage)
        self.accept("toggleChat", self.toggleChat)
        self.hide()

    def start(self, roomZone):
        self.msg = self.cr.createDistributedObject(
            className = "DMessage",
            zoneId = roomZone)

        self.chat.frmChat.show()
        self.chat.btnToggleChat.show()
        base.messenger.send("loadChatDone")

    def destroy(self):
        self.ignoreAll()
        self.chat.frmChat.removeNode()
        self.chat.btnToggleChat.removeNode()
        del self.chat
        self.chat = None

    def toggleChat(self):
        if self.chat.frmChat.isHidden():
            self.chat.frmChat.show()
            btnName = self.chat.btnToggleChat["text"]
            if btnName.endswith("*"):
                self.chat.btnToggleChat["text_fg"] = self.btnToggleChatOrigTextFG
                self.chat.btnToggleChat["text"] = btnName[:-1]
        else:
            self.chat.frmChat.hide()

    def focusInCommandFunc(self):
        base.messenger.send("disableOtherKeyboardInput")
        self.clearText()

    def focusOutCommandFunc(self):
        base.messenger.send("enableOtherKeyboardInput")
        self.setDefaultText()

    def clearText(self):
        """ Write an empty string in the textbox """
        self.chat.txtMessage.enterText("")

    def setDefaultText(self):
        """ Write the default message in the textbox """
        self.chat.txtMessage.enterText("Your Message")

    def sendMessage(self, args=None):
        """ Send the text written in the message textbox to the clients """
        txtMsg = self.chat.txtMessage.get()
        if txtMsg.strip() == "": return
        sentText = "\1bold\1{}:\2 {}".format(self.cr.getMyName(), self.chat.txtMessage.get())

        self.msg.b_sendText(sentText)

        self.chat.txtMessage.enterText("")

    def addMessage(self, message):
        if self.chat.frmChat.isHidden():
            self.chat.btnToggleChat["text_fg"] = (0.2,0.2,1,1)
            self.chat.btnToggleChat["text"] += "*"

        self.lblMessages["text"] = "{}\n{}".format(
            self.lblMessages["text"],
            message)

        # get the size of the written text
        textbounds = self.lblMessages.getTightBounds()
        # resize the canvas. This will make the scrollbars dis-/appear,
        # dependent on if the canvas is bigger than the frame size.
        self.chat.frmMessages["canvasSize"] = (
            -0.38, textbounds[1].getX(),
            textbounds[0].getZ(), 0)
        self.chat.frmMessages.setCanvasSize()

    def show(self):
        self.chat.frmChat.show()
        self.chat.btnToggleChat.show()

    def hide(self):
        self.chat.frmChat.hide()
        self.chat.btnToggleChat.hide()
