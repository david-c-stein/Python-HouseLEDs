#!/usr/bin/env python

import datetime
import getopt
import inspect
import logging
import logging.config
import os
import platform
import sys
import time
import ephem
import numpy

import Global
import Logger

try:
    import neopixel
    __LEDS__ = True
except ImportError:
    __LEDS__ = False

if Global.__EMULATE_HW__:
    __LEDS__ = False

__TIMER__ = False
__AUDIO__ = True

if Global.__MULTIPROCESSING__:
    import multiprocessing
    from multiprocessing import Queue
    from multiprocessing import RawArray
else:
    if sys.version_info[0] < 3:
        from Queue import Queue
    else:
        from queue import Queue


__version__ = "0.0.1"

appStartTime = datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')


# San Jose International Airport
lat = '37.236373767'  # latitude
lon = '-121.92913348' # longtitude
alt = 12              # altitude (meters)


class Sun(object):
    def __init__(self, lat, long, alt):
        self.location = ephem.Observer()

        # San Jose International Airport
        self.location.lat = lat
        self.location.lon = long
        self.location.elevation = alt

        self.location.date = datetime.datetime.now()
        self.sun = ephem.Sun()

    def nextSunrise(self):
        return ephem.localtime(self.location.next_rising(self.sun))

    def nextSunset(self):
        return ephem.localtime(self.location.next_setting(self.sun))


class displayTime(object):
    def __init__(self, logger, start_hour=15, start_min=0, stop_hour=22, stop_min=0):
        self.logger = logger
        self.start_hour = start_hour
        self.start_minute = start_min
        self.stop_hour = stop_hour
        self.stop_minute = stop_min

        self.starttype = None
        self.stoptype = None

        start = datetime.time(hour=start_hour, minute=start_min)
        self.starttime = datetime.datetime.combine(datetime.datetime.today(), start)
        stop = datetime.time(hour=stop_hour, minute=stop_min)
        self.stoptime = datetime.datetime.combine(datetime.datetime.today(), stop)

        self.sun = Sun(lat, lon, alt)
        self.logger.info("Next sunrise: " + str(self.sun.nextSunrise()))
        self.logger.info("Next sunset: " + str(self.sun.nextSunset()))

    def setStart(self, time):
        self.starttype = 'fixed'
        start = datetime.datetime.strptime(time, '%H:%M:%S.%f').time()
        self.starttime = datetime.datetime.combine(datetime.datetime.today(), start)
        self.logger.debug("display start time: " + str(self.starttime))

    def setStartNow(self):
        self.starttype = 'fixed'
        self.starttime = datetime.datetime.now()
        self.logger.debug("display start time: " + str(self.starttime))

    def setStartBeforeSunset(self, hour, minute=0):
        self.starttype = 'sun'
        self.start_hour = hour
        self.start_minute = minute
        sunrise = self.sun.nextSunrise()
        self.logger.info("Next sunrise: " + str(sunrise))
        self.starttime = sunset - datetime.timedelta(hours=0, minutes=30)
        self.logger.debug("display start time: " + str(self.starttime))

    def getStart(self):
        return self.starttime.strftime('%H:%M:%S.%f')[:-3]

    def setStop(self, time):
        self.starttype = 'fixed'
        stop = datetime.datetime.strptime(time, '%H:%M:%S.%f').time()
        self.stoptime = datetime.datetime.combine(datetime.datetime.today(), stop)
        self.logger.debug("display stop time: " + str(self.stoptime))

    def setStopNow(self):
        self.stoptype = 'fixed'
        self.stoptime = datetime.datetime.now()
        self.logger.debug("display stop time: " + str(self.stoptime))

    def setStopAfterSunset(self, hour, minute=0):
        self.stoptype = 'sun'
        self.stop_hour = hour
        self.stop_minute = minute

        sunset = self.sun.nextSunset()
        self.logger.info("Next sunset: " + str(sunset))
        self.stoptime =  sunset + datetime.timedelta(hours=0, minutes=30)
        self.logger.debug("display stop time: " + str(self.stoptime))

    def getStop(self):
        return self.stoptime.strftime('%H:%M:%S.%f')[:-3]

    def _checkTimeRollover(self):
        now = datetime.datetime.now()
        if self.starttime < now:
            # get next days starttime
            self.starttime += datetime.timedelta(days=1)
            self.logger.info("Next display start time: " + str(self.starttime))
        if self.stoptime < now:
            # get next days stoptime
            self.stoptime += datetime.timedelta(days=1)
            self.logger.info("Next display stop time: " + str(self.stoptime))
            
    def secondsToDisplayOn(self):
        now = datetime.datetime.now()
        self._checkTimeRollover()
        diff = self.starttime - now
        return diff.seconds

    def secondsToDisplayOff(self):
        now = datetime.datetime.now()
        self._checkTimeRollover()
        diff = self.stoptime - now
        return diff.seconds

    def isDisplay(self):
        now = datetime.datetime.now()
        ret = False
        if self.starttime < self.stoptime:
            if self.starttime <= now:
                ret = True
        elif now <= self.stoptime:
                ret = True
        return ret

class myApp(object):
    def __init__(self):

        self.pAU = None  # Audio thread/process
        self.pWS = None  # WebServices thread/process
        self.pPE = None  # Pattern Engine thread/process

        self.logConfig = Logger.logConfig

        self.FRAMES_PER_SECOND = 30
        self.msLoopDelta = round(1.0/self.FRAMES_PER_SECOND, 4)
        self.msPrev = 0

        self.strip = None
        self.run = False

    def main(self, argv):
        logging.config.dictConfig(self.logConfig)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Start time: " + appStartTime)

        # parse command line arguments
        try:
            opts, args = getopt.getopt(argv, "h", ["help"])
        except getopt.GetoptError as e:
            self.logger.exception(str(e))
            self.usage()
            return
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.usage()
                return
            else:
                self.usage()
                return

        self.running = True
        run = True

        while(run):
            try:
                self.initialize()
                self.start()
                self.stop()

            except(KeyboardInterrupt, SystemExit):
                self.logger.info("Interrupted Main process")

            except Exception as e:
                self.logger.exception(e)

            finally:
                self.stop()
                run = False

    def initialize(self):
        try:
            # identify platform
            self.logger.info("------------------------------")
            self.logger.info("  machine: " + platform.machine())
            self.logger.info("  version: " + platform.version())
            self.logger.info(" platform: " + platform.platform())
            self.logger.info("   system: " + platform.system())
            self.logger.info("processor: " + platform.processor())
            if Global.__MULTIPROCESSING__:
                self.logger.info("    cores: " + str(multiprocessing.cpu_count()))
            self.logger.info("    nodes: " + platform.node())
            self.logger.info("PythonImp: " + platform.python_implementation())
            self.logger.info("PythonVer: " + platform.python_version())
            self.logger.info("starttime: " + appStartTime)
            self.logger.info("scriptver: " + __version__)
            self.logger.info("------------------------------")

            # include paths
            dirs = ['pythonLibs', 'WebServices', 'Audio', 'PatternEngine']
            self.initPaths(dirs)

            # initialize queues
            self.qApp = None
            self.qPat = None
            self.qAud = None
            self.qWeb = None

            if Global.__MULTIPROCESSING__:
                self.qApp = multiprocessing.Queue()
                self.qPat = multiprocessing.Queue()
                self.qAud = multiprocessing.Queue()
                self.qWeb = multiprocessing.Queue()
            else:
                self.qApp = Queue()
                self.qPat = Queue()
                self.qAud = Queue()
                self.qWeb = Queue()

            # message queues
            self.getMsg = self.qApp
            self.putMsgAud = self.qAud.put
            self.putMsgPat = self.qPat.put
            self.putMsgWeb = self.qWeb.put

            self.initializeLEDs()

            # hardware configuration
            self.configHW = {
                #dcsdcs "HTTPPORT" : 8888,
                #dcsdcs "SOCKETIOPORT" : 8888,
                "HTTPPORT" : 8800,
                "SOCKETIOPORT" : 8800,
            }

            # initialize patten engine process
            try:
                from PatternEngine import PatternEngine
                self.pPE = PatternEngine(self.qApp, self.qAud, self.qWeb, self.qPat, self.configHW, self.sharedArrayBase, self.ledCount)
            except Exception as e:
                self.logger.error( "PatternEngine Initialization Error: " + str(e) )
                raise(e)

            # initialize web services process
            try:
                from WebServices import WebServices
                self.pWS = WebServices(self.qApp, self.qAud, self.qWeb, self.qPat, self.configHW, self.sharedArrayBase, self.ledCount)
            except Exception as e:
                self.logger.error( "Web Initialization Error: " + str(e) )
                raise(e)

            # initialize audio process
            if __AUDIO__:
                try:
                    from Audio import Audio
                    self.pAU = Audio(self.qApp, self.qAud, self.qWeb, self.qPat, self.configHW)
                except Exception as e:
                    self.logger.error( "Audio Initialization Error: " + str(e) )
                    raise(e)

            self.displayTime = displayTime(self.logger)

        except Exception as e:
            self.logger.exception( "Initialization Error: " + str(e) )
            raise(e)
        return

    def putAud(self, data):
        # send data to audio
        self.putMsgAud({'src': 'App', 'data': data})

    def putPat(self, data):
        # send data to pat
        self.putMsgApp({'src': 'App', 'data': data})

    def putWeb(self, data):
        # send data to web
        self.putMsgWeb({'src': 'App', 'data': data})

    def putAll(self, data):
        # send data back to audio and web
        self.putMsgAud({'src': 'App', 'data': data})
        self.putMsgPat({'src': 'App', 'data': data})
        self.putMsgWeb({'src': 'App', 'data': data})

    def _frame_delay(self):
        msCurr = time.time()
        msDelta = msCurr - self.msPrev
        if 0 < msDelta < self.msLoopDelta:
            time.sleep(self.msLoopDelta - msDelta)
        self.msPrev = msCurr

    def initializeLEDs(self):

        try:
            # LED strip configuration:
            LED_COUNT      = 482     # Number of LED pixels.
            LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
            LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
            LED_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
            LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
            LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
            LED_CHANNEL    = 0       # 0 or 1

            self.ledCount = LED_COUNT
            self.sharedArrayBase = RawArray('B', numpy.prod((self.ledCount, 3)))
            self.sharedArray = numpy.ctypeslib.as_array(self.sharedArrayBase)

            if not __LEDS__:
                self.logger.info("---- Running without real LEDS ----")

            else:
                LED_STRIP = neopixel.ws.WS2811_STRIP_RGB
                self.strip = neopixel.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
                self.strip.begin()

                self.leds = self.strip.getPixels()
                self.strip.setBrightness(LED_BRIGHTNESS)

                # quick led check
                for i in range(self.ledCount):
                    self.strip.setPixelColorRGB(i,0,0,0,0)
                print("ALL: off")
                self.strip.show()
                time.sleep(0.25)
                self.strip.show()
                time.sleep(0.25)
                self.strip.show()
                time.sleep(0.25)
                self.strip.show()
                time.sleep(5)

                for i in range(self.ledCount):
                    self.strip.setPixelColorRGB(i,255,0,0,0)
                print("ALL: red")
                self.strip.show()
                time.sleep(2)

                for i in range(self.ledCount):
                    self.strip.setPixelColorRGB(i,0,255,0,0)
                print("ALL: green")
                self.strip.show()
                time.sleep(2)

                for i in range(self.ledCount):
                    self.strip.setPixelColorRGB(i,0,0,255,0)
                print("ALL: blue")
                self.strip.show()
                time.sleep(2)

                # turn off all the leds
                for i in range(self.ledCount):
                    self.strip.setPixelColorRGB(i,0,0,0,0)
                print("ALL: off")
                self.strip.show()

        except Exception as e:
            self.logger.exception(e)

    def start(self):
        try:
            self.logger.info("Main starting")

            # start pattern engine process
            self.pPE.start()

            # start audio
            if __AUDIO__:
                self.pAU.start()

            # start webservices process
            self.pWS.start()

            # shared led array memory
            ledArray = self.sharedArray.reshape((self.ledCount, 3))

            self.running = True;

            #--------------
            # https://learn.adafruit.com/led-tricks-gamma-correction
            #
            # Gamma8  This table remaps linear input values (e.g. 127 = half brightness)
            # to nonlinear gamma-corrected output values (numbers producing the desired
            # effect on the LED; e.g. 36 = half brightness)

            self.gamma8 = [
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
                1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
                2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
                5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
               10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
               17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
               25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
               37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
               51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
               69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
               90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
              115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
              144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
              177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
              215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ]

            displayActive = False
            forceOn = False
            timeCheck = 0

            self.putWeb({'startTime': self.displayTime.getStart()})
            self.putWeb({'stopTime': self.displayTime.getStop()})
            
            try:
                while self.running:
                    if not self.getMsg.empty():
                        msg = self.getMsg.get()
                        if not Global.__MULTIPROCESSING__:
                            self.getMsg.task_done()

                        if (msg != None):
                            src = msg['src']
                            data = msg['data']

                            self.logger.debug("Main : " + str(msg))

                            if 'Web' == src:
                                if 'startTimePicker' in data:
                                    self.displayTime.setStart(data['startTimePicker'])
                                    timeCheck = 0

                                elif 'stopTimePicker' in data:
                                    self.displayTime.setStop(data['stopTimePicker'])
                                    timeCheck = 0

                                elif 'forceOn' in data:
                                    forceOn = data['forceOn']

                    if forceOn:
                        displayActive = True
                    else:
                        # to help minimize cpu expensive continous time checks
                        if timeCheck <= 0:

                            self.logger.debug(".....TIMECHECK.....")

                            if self.displayTime.isDisplay():
                                self.putAll({'displayOn': True})
                                displayActive = True
                                diff = self.displayTime.secondsToDisplayOff()
                                self.logger.info( "Display on for : " + str(diff) + " seconds")

                            else:
                                self.putAll({'displayOn': False})
                                displayActive = False
                                diff = self.displayTime.secondsToDisplayOn()
                                self.logger.info( "Display off for : " + str(diff) + " seconds")

                                # leds off
                                if __LEDS__:
                                    for i in range(self.ledCount):
                                        self.strip.setPixelColorRGB(i,0,0,0,0)
                                    self.strip.show()
                                    self.strip.show()

                            timeCheck = diff
                        else:
                            timeCheck -= 1

                    if __LEDS__ and displayActive:
                        for i in range(self.ledCount):
                            # gamma correct brighness with rgb leds
                            self.strip.setPixelColorRGB(i, self.gamma8[ledArray[i][0]], self.gamma8[ledArray[i][1]], self.gamma8[ledArray[i][2]])
                            #self.strip.setPixelColorRGB(i, ledArray[i][0], ledArray[i][1], ledArray[i][2])

                        self.strip.show()
                        self._frame_delay()

                    else:
                        time.sleep(1)

            except(KeyboardInterrupt, SystemExit):
                self.logger.info("Interupted PatternEngine process")

            except Exception as e:
                self.logger.exception(str(e))

            finally:
                if self.strip is not None:
                    # turn off all the leds
                    for i in range(self.ledCount):
                        self.strip.setPixelColorRGB(i,0,0,0,0)
                    self.strip.show()
                    self.strip.show()
                    self.strip.show()

                self.stop()
                self.running = False

        except Exception as e:
            self.logger.exception(str(e))

        finally:
            if self.strip is not None:
                # turn off all the leds
                for i in range(self.ledCount):
                    self.strip.setPixelColorRGB(i,0,0,0,0)
                self.strip.show()
                self.strip.show()
                self.strip.show()

            self.stop()
            self.running = False

    def stop(self):
        # stop processes
        if(self.pPE != None):
            self.pPE.stop()
        if(self.pAU != None):
            self.pAU.stop()
        if(self.pWS != None):
            self.pWS.stop()
        self.pPE = None
        self.pAU = None
        self.pWS = None
        self.running = False

    def usage(self):
        print("\n\n sudo python " + __file__ + "\n")
        self.stop()
        exit(1)

    def initPaths(self, dirs):

        try:
            # include <local> paths   NOTE: realpath() works with simlinks
            cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
            if cmd_folder not in sys.path:
                sys.path.insert(0, cmd_folder)
                self.logger.debug("Path Added : " + cmd_folder)

            # include dirs passed
            for dir in dirs:
                cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], dir)))
                if cmd_subfolder not in sys.path:
                    sys.path.insert(0, cmd_subfolder)
                    self.logger.debug("Path Added : " + cmd_subfolder)

        except Exception as e:
            self.logger.exception(str(e))
            raise

if __name__== '__main__':

    if __LEDS__:
        if not os.geteuid() == 0:
            sys.exit('This script must be run as root')

    myApp().main(sys.argv[1:])

