#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import random
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence, Parallel, LerpFunctionInterval, Func

MENU_TRACKS = ["menu.ogg"]
GAME_TRACKS = ["track1.ogg", "track2.ogg", "track3.ogg"]
WIN_TRACKS = ["win.ogg"]
LOOSE_TRACKS = ["loose.ogg"]

SFX_DICE = ["dice1.ogg", "dice2.ogg", "dice3.ogg", "dice4.ogg"]
SFX_SLIDE = ["slide.ogg"]
SFX_END_TURN = ["endTurn.ogg"]

class AudioManager(DirectObject):
    def __init__(self):
        self.accept("playAudioMenu", self.playMusic, extraArgs=[MENU_TRACKS])
        self.accept("playAudioGame", self.playMusic, extraArgs=[GAME_TRACKS])
        self.accept("playAudioWin", self.playMusic, extraArgs=[WIN_TRACKS])
        self.accept("playAudioLoose", self.playMusic, extraArgs=[LOOSE_TRACKS])
        self.accept("playAudioNext", self.playNext)

        self.accept("playSFXDice", self.playSfx, extraArgs=[SFX_DICE])
        self.accept("playSFXSlide", self.playSfx, extraArgs=[SFX_SLIDE])
        self.accept("playSFXEndTurn", self.playSfx, extraArgs=[SFX_END_TURN])

        self.currentTrack = None
        self.currentSongList = None
        self.playNextSong = False

        base.musicManager.setConcurrentSoundLimit(2)

    def playSfx(self, sfxList):
        loader.loadSfx("assets/audio/sfx/" + random.choice(sfxList)).play()

    def playMusic(self, songList):
        if self.currentSongList == songList and not self.playNextSong:
            return
        self.playNextSong = False

        self.currentSongList = songList
        newSound = loader.loadMusic("assets/audio/music/" + random.choice(songList))

        dur = 2.0

        newSound.setFinishedEvent("playAudioNext")
        newSound.play()

        if self.currentTrack is not None:
            oldTrack = self.currentTrack
            oldTrack.setFinishedEvent("")
            Sequence(
                Parallel(
                    LerpFunctionInterval(newSound.setVolume, dur, 0, 1),
                    LerpFunctionInterval(oldTrack.setVolume, dur, 1, 0)
                ),
                Func(oldTrack.stop)
            ).start()

        self.currentTrack = newSound

    def playNext(self):
        self.playNextSong = True
        self.playMusic(self.currentSongList)
