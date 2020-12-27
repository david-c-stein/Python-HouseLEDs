import Global

import json
import time
import datetime
import os.path
import tornado.web
import tornado.websocket
from tornado.escape import json_encode, json_decode
from tornado.options import options
import logging
import logging.config
import uuid
import base64
import numpy
import pickle


def getClientID():
    return ('ID_' + str(uuid.uuid1()).replace('-',''))


class WSHandler(tornado.websocket.WebSocketHandler):

    clients = {}
    patterns = []
    selected_pattern = None
    selected_forceon = None
    selected_startTimePicker = None
    selected_stopTimePicker = None

    def initialize(self, qApp, qAud, qWeb, qPat, config, sharedArrayBase, ledCount):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __file__)

        self.ledCount = ledCount
        sharedArray = numpy.ctypeslib.as_array(sharedArrayBase)
        self.ledArray = sharedArray.reshape((self.ledCount, 3))

        # message queues
        self.getMsg = qWeb
        self.putMsgApp = qApp.put
        self.putMsgAud = qAud.put
        self.putMsgPat = qPat.put

        # setup message handler
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(milliseconds=100),self.msgHandler)

    def putApp(self, data):
        # send data to app
        self.putMsgApp({'src': 'Web', 'data': data})

    def putWeb(self, data):
        # send data to aud
        self.putMsgAud({'src': 'Web', 'data': data})

    def putPat(self, data):
        # send data to patternengine
        self.putMsgPat({'src': 'Web', 'data': data})

    def putAll(self, data):
        # send data back to all
        self.putMsgApp({'src': 'Web', 'data': data})
        self.putMsgAud({'src': 'Web', 'data': data})
        self.putMsgPat({'src': 'Web', 'data': data})

    #=============================================================
    # Message handler for backend

    def msgHandler(self):
        try:
            if not self.getMsg.empty():
                msg = self.getMsg.get()
                if not Global.__MULTIPROCESSING__:
                    self.getMsg.task_done()

                if (msg != None):
                    src = msg['src']
                    data = msg['data']

                    self.logger.debug("WS msg: " + str(msg))

                    if 'Pat' == src:
                        if 'addPattern' in data:
                            # patterns for web clients
                            for pattern in data['addPattern']:
                                self.sendAllData(['addPattern', pattern])
                                WSHandler.patterns.append(pattern)

                    if 'App' == src:
                        if 'startTime' in data:
                            self.sendAllData(['startTimePicker', startTime])
                            WSHandler.selected_startTimePicker = startTime

                        elif 'stopTime' in data:
                            self.sendAllData(['stopTimePicker', stopTime])
                            WSHandler.selected_stopTimePicker = stopTime

            # ledinfo to webpage
            self.sendAllData(['ledData', self.ledArray.tolist()])

            # continue message handler
            tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(milliseconds=100), self.msgHandler)

        except Exception as e:
            self.logger.exception(str(e))
            raise

    #=============================================================
    # Message handler for web clients

    def webMsgHandler(self, msg):

        self.logger.info('Client Id: ' + self.id + " IP address: " + self.ipAddr + " : " + str(msg))

        # pattern message
        if (msg['event'] == 'pattern'):
            pattern = msg['data']
            WSHandler.selected_pattern = pattern
            WSHandler.sendOthersData(self.id, ['selectPattern', pattern])
            self.putPat({'selectPattern': pattern})

        elif (msg['event'] == 'forceOn'):
            forceOn = msg['data']
            WSHandler.selected_forceon = forceOn
            WSHandler.sendOthersData(self.id, ['forceOn', forceOn])
            self.putAll({'forceOn': forceOn})

        elif (msg['event'] == 'startTimePicker'):
            startTimePicker = msg['data']
            WSHandler.selected_startTimePicker = startTimePicker
            WSHandler.sendOthersData(self.id, ['startTimePicker', WSHandler.selected_startTimePicker])
            self.putApp({'startTimePicker': WSHandler.selected_startTimePicker})

        elif (msg['event'] == 'stopTimePicker'):
            stopTimePicker = msg['data']
            WSHandler.selected_stopTimePicker = stopTimePicker
            WSHandler.sendOthersData(self.id, ['stopTimePicker', WSHandler.selected_stopTimePicker])
            self.putApp({'stopTimePicker': WSHandler.selected_stopTimePicker})

    #=============================================================

    def check_origin(self, origin):
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self, *args):
        # get client ip address
        x_real_ip = self.request.headers.get("X-Real-IP")
        self.ipAddr = x_real_ip or self.request.remote_ip

        # Get unique client ID
        self.id = getClientID()
        self.stream.set_nodelay(True)
        WSHandler.clients[self.id] = {"id": self.id, "object": self}
        self.logger.info("Client added: id " + self.id + " IP addr: " + self.ipAddr)

        # initialize pattern list in client
        for pattern in WSHandler.patterns:
            self.sendData(['addPattern', pattern])

        self.sendData(['selectPattern', WSHandler.selected_pattern])
        self.sendData(['startTimePicker', WSHandler.selected_startTimePicker])
        self.sendData(['stopTimePicker', WSHandler.selected_stopTimePicker])

    def on_close(self):
        if self.id in WSHandler.clients:
            del WSHandler.clients[self.id]
        self.logger.info("Client closed: id " + self.id + " IP address " + self.ipAddr)

    def on_message(self, message):
        self.logger.debug("Client : " + self.id + " msg: " + message)
        msg = json_decode(message)
        self.webMsgHandler(msg)

    def sendData(self, a):
        self.write_message( json_encode(a) )

    @classmethod
    def sendAllData(cls, a):
        for c in cls.clients:
            cls.clients[c]['object'].sendData(a);

    @classmethod
    def sendOthersData(cls, id, a):
        for c in cls.clients:
            if cls.clients[c]['id'] != id:
                cls.clients[c]['object'].sendData(a);

    @classmethod
    def sendOneData(cls, id, a):
        for c in cls.clients:
            if cls.clients[c]['id'] == id:
                cls.clients[c]['object'].sendData(a);
