import builtins
import os

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


if __name__ == "__main__":
    """starting the server"""
    base = ShowBase(windowType="none")
    builtins.simbase = base


    # instantiate the server
    GameServerRepository()


    # set the serverHost used in the AI Repo
    base.serverHost = ConfigVariableString("server-host", "127.0.0.1:4400")
    # AI repository
    air = AIRepository()
    simbase.air = air

    # give some feedback to the user
    print("server created, waiting for client.")

    # start the application
    base.run()
