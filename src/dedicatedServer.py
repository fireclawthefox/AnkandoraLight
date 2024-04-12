#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import builtins
import os
import argparse

# all imports needed by the engine itselfe
from direct.showbase.ShowBase import ShowBase

from repositories.GameServerRepository import GameServerRepository
from repositories.AIRepository import AIRepository

from panda3d.core import loadPrcFileData, ConfigVariableString, loadPrcFile, Filename
# the server doesn't need audio. We expect this to run on headless servers
loadPrcFileData("", "audio-library-name null")

#
# PATHS AND CONFIGS
#
# set company and application details
companyName = "Grimfang Studio"
appName = "Ankandora"
versionstring = "20.04"

# build the path from the details we have
home = os.path.expanduser("~")
basedir = os.path.join(
    home,
    companyName,
    appName)
if not os.path.exists(basedir):
    os.makedirs(basedir)

# look for a config file
prcFile = os.path.join(basedir, "{}-server.prc".format(appName))
if os.path.exists(prcFile):
    mainConfig = loadPrcFile(Filename.fromOsSpecific(prcFile))

# pars command-line arguments
parser = argparse.ArgumentParser(description='The game and AI server for {}'.format(appName))
parser.add_argument('--no-ai', dest='noAI', action='store_true',
                    help='Start only the game server')
parser.add_argument('--no-game-server', dest='noGameServer', action='store_true',
                    help='Start only the AI server')
args = parser.parse_args()


if __name__ == "__main__":
    """starting the server"""
    base = ShowBase(windowType="none")

    # we need to set this as it is used in Pandas server logic
    builtins.simbase = base

    #
    # GAME SERVER
    #
    if not args.noGameServer:
        print("Creating Game Server")
        # instantiate the server
        GameServerRepository()

    #
    # AI SERVER
    #
    if not args.noAI:
        print("Creating AI Server")
        # set the serverHost used in the AI Repo
        base.serverHost = ConfigVariableString("server-host", "127.0.0.1:4400")
        # AI repository
        air = AIRepository()
        # store the AI repository for the engine to use
        simbase.air = air

    # give some feedback to the user
    print("server created, waiting for client.")

    # start the application
    base.run()
