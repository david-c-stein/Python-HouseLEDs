#!/usr/bin/env python

import logging
import logging.config
import threading
import time

import numpy
import pygame

import Global

if Global.__MULTIPROCESSING__:
    import multiprocessing


class Player(object):

    def __init__(self):

        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 2048  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)

        self.clock = pygame.time.Clock()

        self.musicFileName = None
        self.eventFileName = None
        self.paused = False
        self.labelTrack = None
        self.currPos = None
        self.isPlaying = False
        
        self.InternalOffsetTime = 0

    def setVolume(self, value):
        pygame.mixer.music.set_volume(value)

    def loadMusic(self, musicFileName, eventFileName=None):
        try:
            pygame.mixer.music.load(musicFileName)
        except pygame.error:
            return

        try:
            if self.labelTrack:
                # read eventFile
                data = numpy.genfromtext(eventFileName, dtype=[('start', 'f',), ('start', 'S20')], delimiter='\t',
                                         autostrip=True)
                # get labels
                self.labelTrack = set([x[2] for x in data])
        except error:
            return

    def playMusic(self):
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
        self.paused = False

    def pauseMusic(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True

    def stopMusic(self):
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        self.paused = False

    def monitorPlay(self):
        if pygame.mixer.music.get_busy():
            msTime = pygame.mixer.music.get_pos()

            self.currPos = self.InternalOffsetTime + msTime
            print str(self.currPos)

            # minutes = int(mstime / 60000)
            # seconds = int(mstime / 1000 - minutes * 60)

            # check for event
            # -- send event msg to PatternEngine
            # self.labelTrack


class Audio(multiprocessing.Process if Global.__MULTIPROCESSING__ else threading.Thread):

    def __init__(self, qAud, qHdw, qWeb, config):
        if Global.__MULTIPROCESSING__:
            # -- multiprocessing
            multiprocessing.Process.__init__(self)
        else:
            # -- threading
            super(Audio, self).__init__()

        self.config = config

        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __file__)

        # message queues
        self.getMsg = qAud
        self.putMsgWeb = qWeb.put
        self.putMsgHdw = qHdw.put


        
        #music = pygame.mixer_music
        
        #freq = 44100  # audio CD quality
        #bitsize = -16  # unsigned 16 bit
        #channels = 2  # 1 is mono, 2 is stereo
        #buffer = 2048  # number of samples
        #pygame.mixer.init(freq, bitsize, channels, buffer)
        
        #music = music.load('./Media/Audio/DS9.mp3')
        
        
        # another audio idea
        # https://github.com/MegaDoot/Music-Player/blob/master/App.py
        # self.player = pyglet.media.Player()
        
        # initialize audio
        self.player = Player()
        
        self.player.loadMusic('./Media/Audio/DS9.mp3')
        self.player.playMusic()
        self.player.monitorPlay()
        
        
        self.msg = None

        self.done = False

    def run(self):
        # called on start() signal
        try:
            self.logger.info("Running Audio process")

            while not self.done:
                try:
                    # --------------------------------
                    # check for messages from the WebService
                    if not self.getMsg.empty():
                        self.msg = self.getMsg.get()
                        if not Global.__MULTIPROCESSING__:
                            self.getMsg.task_done()

                        if self.msg is not None:

                            print(self.msg)

                            # playMusic
                            if self.msg['event'] == 'play':
                                self.player.playMusic()

                            # pauseMusic
                            elif self.msg['event'] == 'pause':
                                self.player.pauseMusic()

                            # stopMusic
                            elif self.msg['event'] == 'stop':
                                self.player.stopMusic()

                            # loadMusic
                            elif self.msg['event'] == 'load':
                                self.player.loadMusic(self.msg['data'])


                            else:
                                self.logger.error('Unknown message type')

                    # actively playing audio
                    if self.player.isPlaying:
                        self.monitorPlay()

                    else:
                        time.sleep(.05)

                except(KeyboardInterrupt, SystemExit):
                    self.logger.info("Interrupted HW process")
                    self.stop()
                    exit()

                except Exception as e:
                    self.logger.exception(e)

        except Exception as e:
            self.logger.exception(e)

    def stop(self):
        # do cleanup
        self.done = True
        return
