#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import (TextNode,
    TextProperties,
    TextPropertiesManager)

from gui.Chat import GUI as Chat

class ChatHandler(DirectObject, Chat):
    def __init__(self, cr):
        base.messenger.send("registerLoadEvent", ["loadChatDone"])

        Chat.__init__(self, base.a2dTopRight)

        self.cr = cr

        self.frmChat.setPos(
            -self.frmChat["frameSize"][1],
            self.frmChat.getY(),
            self.frmChat.getZ())
        self.btnToggleChat.hide()
        self.btnToggleChat.setPos(
            -self.btnToggleChat["frameSize"][1],
            self.btnToggleChat.getY(),
            self.btnToggleChat.getZ())
        self.btnToggleChatOrigTextFG = self.btnToggleChat.component("text1").fg


        self.btnToggleChat["sortOrder"] = 990
        self.frmChat["sortOrder"] = 990

        self.txtMessage["focusInCommand"] = self.focusInCommandFunc
        self.txtMessage["focusOutCommand"] = self.focusOutCommandFunc
        self.txtMessage["command"] = self.sendMessage

        tpMgr = TextPropertiesManager.getGlobalPtr()
        tpBold = TextProperties()
        font = loader.loadFont("assets/fonts/OldaniaADFStd-Bold.otf")
        tpBold.setFont(font)
        tpMgr.setProperties("bold", tpBold)


        self.lblMessages = OnscreenText(
            text="\1bold\1Messages:\2",
            scale = 0.05,
            pos = (self.frmMessages["canvasSize"][0], -0.05),
            align = TextNode.ALeft,
            wordwrap = 14,
            parent = self.frmMessages.getCanvas())

        self.accept("sendMessage", self.sendMessage)
        self.accept("setText", self.addMessage)
        self.accept("toggleChat", self.toggleChat)
        self.hide()

    def start(self, roomZone):
        self.msg = self.cr.createDistributedObject(
            className = "DMessage",
            zoneId = roomZone)

        self.frmChat.show()
        self.btnToggleChat.show()
        base.messenger.send("loadChatDone")

    def destroy(self):
        self.ignoreAll()
        self.frmChat.removeNode()
        self.btnToggleChat.removeNode()

    def toggleChat(self):
        """Toggle the visibility of the chat frame and set the buttons text
        accordingly"""
        base.messenger.send("playSFXSlide")
        if self.frmChat.isHidden():
            self.frmChat.show()
            btnName = self.btnToggleChat["text"]
            if btnName.endswith("*"):
                self.btnToggleChat["text_fg"] = self.btnToggleChatOrigTextFG
                self.btnToggleChat["text"] = btnName[:-1]
        else:
            self.frmChat.hide()

    def focusInCommandFunc(self):
        base.messenger.send("disableOtherKeyboardInput")
        self.clearText()

    def focusOutCommandFunc(self):
        base.messenger.send("enableOtherKeyboardInput")
        self.setDefaultText()

    def clearText(self):
        """ Write an empty string in the textbox """
        self.txtMessage.enterText("")

    def setDefaultText(self):
        """ Write the default message in the textbox """
        self.txtMessage.enterText("Your Message")

    def sendMessage(self, args=None):
        """ Send the text written in the message textbox to the clients """
        txtMsg = self.txtMessage.get()
        if txtMsg.strip() == "": return
        sentText = "\1bold\1{}:\2 {}".format(self.cr.getMyName(), self.txtMessage.get())

        self.msg.b_sendText(sentText)

        self.txtMessage.enterText("")

    def addMessage(self, message):
        """Add the given message to the chat messages frame and add a * to the
        toggle buttons text if the chat is hidden"""
        if self.frmChat.isHidden():
            self.btnToggleChat["text_fg"] = (0.2,0.2,1,1)
            self.btnToggleChat["text"] += "*"

        self.lblMessages["text"] = "{}\n{}".format(
            self.lblMessages["text"],
            message)

        # get the size of the written text
        textbounds = self.lblMessages.getTightBounds()
        # resize the canvas. This will make the scrollbars dis-/appear,
        # dependent on if the canvas is bigger than the frame size.
        self.frmMessages["canvasSize"] = (
            -0.38, textbounds[1].getX(),
            textbounds[0].getZ(), 0)
        self.frmMessages.setCanvasSize()
