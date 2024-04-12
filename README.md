# Ankandora
An adventure board game for 1-4 players.

This implementation is the light/travel version that was dedicated for ease of use, shorter play times and quicker learning curve.

The game can be played alone in singleplayer mode or by creating a server and opening rooms for others to join. As it is currently WIP there are a lot of features missing and remaining issues.

Current features:
- Singleplayer mode
- Play with or against up to 3 Bots in Singleplayer mode
- Dedicated server
- 4 types of pieces with dedicated stats
- Basic game features (moving on the board, fighting)
- 2 different game modes
- simple text chat

## Screenshots

![Main menu](/screenshots/MainMenu.png?raw=true "The main menu")
![Singleplayer](/screenshots/Singleplayer.png?raw=true "Singleplayer session")
![Multiplayer](/screenshots/Multiplayer.png?raw=true "Multiplayer session")
![Battle](/screenshots/Battle.png?raw=true "A battle sceen from the Multiplayer session")

## Server
### Configure
The configuration file of the server can be created if it doesn't exist as:<br />
<code>~/Grimfang Studio/Ankandora/Ankandora-server.prc</code>

In it, you should configure these two values:
- server-port - Used for the port that the Server will utilize to listen for connections. Defaults to <code>4400</code>
- server-host - Used by the AI Server to connect to the main server. This will usually be localhost with the port set for server-port. Defaults to <code>127.0.0.1:4400</code>

### Start
To start the server, navigate to the src directory and run<br />
<code>python3 dedicatedServer.py</code>


## Client
### Configure
The configuration file is stored in<br />
<code>~/Grimfang Studio/Ankandora/Ankandora.prc</code><br />
which will be created the first time the game is launched.

The in game options menu currently only features the setting for the server connection URL.

### Start
To start the client, navigate to the src directory and run<br />
<code>python3 main.py</code>


## Notes
License notes for the Oldania ADF Std Fonts:<br />
Copyright Arkandis Digital Foundry, under the GNU General Public License V2 and later, with font exception.

License notes for used audio files:<br />
track1 (A Medieval Tale) by Invadable Harmony CC-BY-ND https://www.jamendo.com/track/1701042/a-medieval-tale
track2 (Ancient Fairy) by Invadable Harmony CC-BY-ND https://www.jamendo.com/track/1705645/ancient-fairy
track3 (Jane Ray - Lullaby of Rain) by Tunguska Electronic Music Society CC-BY-ND https://www.jamendo.com/track/1118119/jane-ray-lullaby-of-rain
menu (Medieval banners) by Nito Ferri CC-BY-SA https://www.jamendo.com/track/1077187/medieval-banners
win (Ya salio de la mar) by Ofri Eliaz CC-BY-SA https://www.jamendo.com/track/316630/ya-salio-de-la-mar
loose (The past ages of glory) by zero-project CC-BY https://www.jamendo.com/track/703954/the-past-ages-of-glory
