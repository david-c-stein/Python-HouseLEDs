#!/usr/bin/env python

import logging
import logging.config
import threading
import time

from mpg123 import Mpg123, Out123

import numpy

try:
    import Global
    if Global.__MULTIPROCESSING__:
        import multiprocessing
except ImportError:
    class Global:
        __MULTIPROCESSING__ = False

"""
class Player(object):
    '''
        Audio on Raspberry PI

        learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi?view=all

        pypi.org/project/mpg123

        github/20tab/mpg123-python/blob/master/examples
    '''
    def __init__(self):
        self.mp3 = None
        self.rate = None
        self.samples_per_sec = 0
        self.channels = None
        self.encoding = None
        self.frame_count = 0
        self.paused = False
        self.time = None

    def elapsed(self, frame_length, frame_count):
        # division my 2 asmumes 16-bit encoding
        samples_per_frame = frame_length / 2

        frames_per_second = float(self.samples_per_sec / samples_per_frame)
        time_sec = float(frame_count / frames_per_second)

        return time_sec

    def load(self, filename):
        self.mp3 = Mpg123('../Media/Music/This_Is_Halloween.mp3')
        self.rate, self.channels, self.encoding = mp3.get_format()

        self.samples_per_sec = self.rate * self.channels

        self.out = Out123()
        self.out.start(self.rate, self.channels, self.encoding)

        self.frame_count = 0
        self.paused = False
        self.time = None

    def pause(self):
        self.paused = not self.paused

    def play(self):
        if not self.paused:

        # need to loop cont here
             for frame in mp3.iter_frames(out.start):
                self.frame_count += 1
                self.time_sec = time_of_frame(len(frame), self.frame_count)
                out.play(frame)

                print "{:02.0f}:{:06.3f}".format(
                    self.time_sec // 60,
                    self.time_sec % 60)

    def stop(self):
        pass
"""




class Player():
    '''
        Audio on Raspberry PI

        learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi?view=all

        pypi.org/project/mpg123

        github/20tab/mpg123-python/blob/master/examples

        # ==================================================

        Audacity to labelTrack eventing

        https://manual.audacityteam.org/man/creating_and_selecting_labels.html

    '''
    def __init__(self):
        self.mp3 = None
        self.out = None
        self.labelTrack = None

        self.rate = None
        self.samples_per_sec = 0
        self.channels = None
        self.encoding = None
        self.paused = False
        self.time = None
        self.labelTrack = None

        self.mp3FileName = None
        self.eventFileName = None

        self.send_q = Queue.Queue()
        self.alive = True

        try:
            self.player_thread = threading.Thread(target.self._player)
            self.player_thread.setDeamon(True)
            self.player_thread.start()
        except thread.error:
            raise

    def _player(self):
        try:
            frame_count = 0
            frame = None
            
            while self.alive:
                
                cmd = self.send_q.get()

                if self.stopped:
                    frame_count = 0

                if not self.paused:
                    # play stuffs
                    for frame in self.mp3.iter_frames(self.out.start):
                        frame_count += 1
                        self.time_sec = _time_of_frame(len(frame), frame_count)
                        out.play(frame)

                        # send out even data
                        if labelTrack:
                            pass

                self.send_q.task_done()
        except(KeyboardInterrupt, SystemExit):
            self.alive = False
            raise
            
        except Exception, err:
            self.alive = False
            raise        

    def _time_of_frame(self, frame_length, frame_count):
        # division my 2 asmumes 16-bit encoding
        samples_per_frame = frame_length / 2
        frames_per_second = float(self.samples_per_sec / samples_per_frame)
        time_sec = float(frame_count / frames_per_second)
        return time_sec

    def elapsed(self):
         return "{:02.0f}:{:06.3f}".format( self.time_sec // 60, self.time_sec % 60)

    def load(self, mp3filename, evenfilename=None):
        if mp3filename:
            self.mp3FileName = filename
        else:
            self.mp3FileName = '../Media/Music/This_Is_Halloween.mp3'

        if eventFileName:
            self.eventFileName = eventFileName
        else:
            self.eventFileName = '../Media/Music/This_is_Halloween.event'
            
        self.mp3 = Mpg123(self.mp3FileName)
        self.rate, self.channels, self.encoding = mp3.get_format()
        self.samples_per_sec = self.rate * self.channels
        self.out = Out123()
        self.out.start(self.rate, self.channels, self.encoding)

        if self.eventFileName:
            # open label file generated by Audacity
            data = numpy.genfromtext(self.eventFileName, dtype=[('start','f',),('start','S20')], delimiter='\t', autostrip=True)
            # get labels
            self.labelTrack = set([x[2] for x in data])

    def pause(self):
        self.paused = not self.paused

    def play(self):
        if not self.paused:

    def stop(self):
        pass



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
       
        # initialize audio
        self.player = Player()
        self.player.start()


        ##### test code 
        self.player.load('./Media/Audio/DS9.mp3')
        self.player.play()
        self.player.elapsed()


        
        
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
                                self.player.play()

                            # pauseMusic
                            elif self.msg['event'] == 'pause':
                                self.player.pause()

                            # stopMusic
                            elif self.msg['event'] == 'stop':
                                self.player.stop()

                            # loadMusic
                            elif self.msg['event'] == 'load':
                                self.player.load(self.msg['data'])

                            else:
                                self.logger.error('Unknown message type')

                    # actively playing audio
                    if self.player.isPlaying:
                        self.elapsed()

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


# ==============================================================================


def time_of_frame(rate, channels, frame_length, frame_count):
    samples_per_sec = rate * channels
    # division my 2 asmumes 16-bit encoding
    samples_per_frame = frame_length / 2

    frames_per_second = float(samples_per_sec / samples_per_frame)
    time_sec = float(frame_count / frames_per_second)

    return "{:02.0f}:{:06.3f}".format(
        time_sec // 60,
        time_sec % 60)
        

# test stuffs are here
if __name__ == '__main__':

    '''
    import Queue
    
    qPat = Queue.Queue()
    qAud = Queue.Queue()
    qWeb = Queue.Queue()
    config = {}

    testAudio = Audio(qAud, qWeb, qPat, config)
    testAudio.run()
    '''

    
    mp3 = Mpg123('../Media/Music/This_Is_Halloween.mp3')
    rate, channels, encoding = mp3.get_format()

    out = Out123()
    
    frame_count = 0

    #for frame in mp3.iter_frames(out.start):
    for frame in mp3.iter_frames(out.start(rate, channels, encoding)):
        frame_count += 1


        time = time_of_frame(rate, channels, len(frame), frame_count)
        ##print time
               
        out.play(frame)

    print "DONE"
    

    





    

