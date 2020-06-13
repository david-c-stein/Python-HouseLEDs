#!/usr/bin/env python

import logging
import logging.config
import threading
import time

from mpg123 import Mpg123, Out123

import numpy
import Queue

try:
    import Global
    if Global.__MULTIPROCESSING__:
        import multiprocessing
except ImportError:
    class Global:
        __MULTIPROCESSING__ = False


'''
    Audio on Raspberry PI
    learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi?view=all

    pypi.org/project/mpg123
    github/20tab/mpg123-python/blob/master/examples

    Audacity to labelTrack eventing
    https://manual.audacityteam.org/man/creating_and_selecting_labels.html
'''

class _mpg123_player_thread (threading.Thread):
    def __init__(self, toQueueu, returnQueue):
        threading.Thread.__init__(self)
        self.getMsg = toQueueu
        self.putMsg = returnQueue.put

        self.mp3 = None
        self.out = None
        self.rate = None
        self.samples_per_sec = 0
        self.channels = None
        self.encoding = None
        self.frame_iter = None
        self.frame_count = 0
        self.pause = True
        self.done = False
        self.labelTrack = None
        self.labelIndex = None

    def load(self, mp3Filename, eventFilename=None):
        self.mp3 = Mpg123(mp3Filename)
        self.rate, self.channels, self.encoding = self.mp3.get_format()
        self.samples_per_sec = self.rate * self.channels

        self.out = Out123()
        self.out.start(self.rate, self.channels, self.encoding)
        self.frame_iter = self.mp3.iter_frames(self.out.start(self.rate, self.channels, self.encoding))
        self.frame_count = 0

        if eventFilename:
            # open label file created with Audacity and get labels  'start' flaot, 'stop' float
            self.labelTrack = numpy.genfromtxt(eventFilename, dtype=[('start','f8',),('stop','f8'),('label','S20')], delimiter='\t', autostrip=True)
            self.labelIndex = 0

    def _time_of_frame(self, frame_length, frame_count):
        # division my 2 asmumes 16-bit encoding
        samples_per_frame = frame_length / 2
        frames_per_second = float(self.samples_per_sec / samples_per_frame)
        time_sec = float(frame_count / frames_per_second)
        return time_sec

    def _elapsed(self, time_sec):
        return "{:02.0f}:{:06.3f}".format(time_sec // 60, time_sec % 60)

    def _label_event_check(self, time):
        try:
            labeldata = self.labelTrack[self.labelIndex]

            if labeldata[0] == labeldata[1]:
                if labeldata[0] <= time:
                    self.putMsg(str(labeldata[0]) + ' : ' + labeldata[2])
                    self.labelIndex += 1    
            else:
                if labeldata[0] < time and labeldata[1] > time:
                    self.putMsg(labeldata[2])
                elif labeldata[1] < time:
                    self.labelIndex += 1
                    
        except IndexError:
            self.labelTrack = None
    
    def _play_mp3(self):
        try:
            self.frame_count += 1
            frame = next(self.frame_iter)
            time = self._time_of_frame(len(frame), self.frame_count)

            if self.labelTrack is not None:
                self._label_event_check(time)
                
            self.putMsg(self._elapsed(time))
            #self.putMsg(str(time))
            self.out.play(frame)
            
        except StopIteration:
            self.putMsg('DONE')
            self.pause = True
            self.done = True

    def run(self):
        while(not self.done):
            try:
                if (not self.getMsg.empty()):
                    msg = self.getMsg.get(timeout=0.02)
                    self.getMsg.task_done()

                    #if msg is not None:
                    self.putMsg('ECHO ' + str(msg))

                    if msg['event'] == 'load':
                        self.load(msg['data']['mp3'], msg['data']['label'])
                        self.pause = True

                    elif msg['event'] == 'play':
                        self.pause = False
                        
                    elif msg['event'] == 'pause':
                        self.pause = True
                        
                    elif msg['event'] == 'stop':
                        self.done = True
                        
                    elif msg['event'] == 'done':
                        self.done = True

                if self.mp3 is not None:
                    if not self.pause:
                        self._play_mp3()

                time.sleep(0.001)

            except(KeyboardInterrupt, SystemExit):
                return
                
            except Exception, err:
                return

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
       
        self.qToPlayer = Queue.Queue()
        self.qFromPlayer = Queue.Queue()

        self.player = None
        
        # initialize audio
        self.player = _mpg123_player_thread(self.qToPlayer, self.qFromPlayer)
        self.player.start()

        self.msg = None
        self.done = False

    def __del__(self):
        self.qToPlayer.put({'event':'stop'})
        self.player.join()
        self.done = True

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
                                self.qToPlayer.put({'event': 'play'})

                            # pauseMusic
                            elif self.msg['event'] == 'pause':
                                self.qToPlayer.put({'event':'pause'})
                                self.qToPlayer.join()

                            # stopMusic
                            elif self.msg['event'] == 'stop':
                                self.qToPlayer.put({'event':'stop'})
                                self.qToPlayer.join()
                                self.done = True

                            # loadMusic
                            elif self.msg['event'] == 'load':
                                #self.qToPlayer.put({'event': 'load', 'data': msg['data']})
                                self.qToPlayer.put({'event': 'load', 'data': {
                                    'mp3':'../Media/Music/This_Is_Halloween.mp3',
                                    'label':'../Media/Music/This_Is_Halloween.labels'}
                                })

                            else:
                                self.logger.error('Unknown message type')
                                self.done = True

                    # --------------------------------
                    # check for messages from _mpg123_player_thread
                    if (not self.qFromPlayer.empty()):
                        msg = self.qFromPlayer.get(timeout=0.2)
                        self.qFromPlayer.task_done()
                        print str(msg)


                    else:
                        time.sleep(.05)

                except(KeyboardInterrupt, SystemExit):
                    self.logger.info("Interrupted HW process")
                    self.stop()

                except Exception as e:
                    self.logger.exception(e)

        except Exception as e:
            self.logger.exception(e)

    def stop(self):
        # do cleanup
        self.qToPlayer.put({'event':'stop'})
        self.player.join()
        self.done = True


# test stuffs are here
if __name__ == '__main__':

    '''
    # --- basic mpg123 test ---

    def time_of_frame(rate, channels, frame_length, frame_count):
        samples_per_sec = rate * channels
        # division my 2 asmumes 16-bit encoding
        samples_per_frame = frame_length / 2
        frames_per_second = float(samples_per_sec / samples_per_frame)
        time_sec = float(frame_count / frames_per_second)
        return "{:02.0f}:{:06.3f}".format(time_sec // 60, time_sec % 60)

    mp3 = Mpg123('../Media/Music/This_Is_Halloween.mp3')
    rate, channels, encoding = mp3.get_format()
   
    frame_count = 0
    out = Out123()

    frame_iter = mp3.iter_frames(out.start(rate, channels, encoding))
    playing = True

    while (playing):
        try:
            frame = next(frame_iter)
            frame_count += 1
            time = time_of_frame(rate, channels, len(frame), frame_count)
            print time
            out.play(frame)
        except StopIteration:
            playing = False
    
    print "DONE"
    '''

    '''
    # --- threaded player class test ---
    qToPlayer = Queue.Queue()
    qFromPlayer = Queue.Queue()

    step = 0
    running = True
    player = None

    while(running):
        try:
            if (not qFromPlayer.empty()):
                msg = qFromPlayer.get(timeout=0.2)
                qFromPlayer.task_done()
            
                print str(msg)

            if step == 0:
                # initialize audio
                print 'initializing player'
                player = _mpg123_player_thread(qToPlayer, qFromPlayer)
                player.start()
                step += 1

            elif step == 1:
                print 'load'
                qToPlayer.put({'event': 'load', 'data': {
                                    'mp3':'../Media/Music/This_Is_Halloween.mp3',
                                    'label':'../Media/Music/This_Is_Halloween.labels'}
                             })
                step += 1

            elif step == 2:
                print 'play'
                qToPlayer.put({'event': 'play'})
                step += 1

            elif step == 3:
                if msg == 'DONE':
                    step += 1

            else:
                qToPlayer.put({'event':'stop'})
                qToPlayer.join()
                running = False

            time.sleep(0.01)

        except(KeyboardInterrupt, SystemExit):
            qToPlayer.put({'event':'stop'})
            qToPlayer.join()
            exit()
    '''
    pass
