#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.distributed.DistributedObject import DistributedObject
from direct.showbase.MessengerGlobal import messenger

class DMessage(DistributedObject):
    def __init__(self, clientRepo):
        DistributedObject.__init__(self, clientRepo)

    def sendText(self, messageText):
        """Function which is caled for local changes only"""
        # send an event, which will set the text on the
        #print "got a message"
        messenger.send("setText", [messageText])

    def d_sendText(self, messageText):
        """Function which is caled to send the message over the network
        therfore the d_ suffix stands for distributed"""
        #print "send message %s" % messageText
        self.sendUpdate("sendText", [messageText])

    def b_sendText(self, messageText):
        """Function which combines the local and distributed functionality,
        so the sendText and d_sendText functions are called.
        The b_ suffix stands for both"""
        self.sendText(messageText)
        self.d_sendText(messageText)
