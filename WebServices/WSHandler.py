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

   
    def initialize(self, queAud, queHdw, queWeb, config, sharedArrayBase, ledCount):

        self.config = config

        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __file__)

        self.ledCount = ledCount
        sharedArray = numpy.ctypeslib.as_array(sharedArrayBase)
        self.ledArray = sharedArray.reshape((self.ledCount, 3))

        # message queues
        self.getMsg = queWeb
        self.putMsgAud = queAud.put
        self.putMsgHwd = queHdw.put

        # setup message handler
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(milliseconds=100),self.msgHandler)


    #=============================================================

    def msgHandler(self):

        try:
            if not self.getMsg.empty():
                msg = self.getMsg.get()
                if not Global.__MULTIPROCESSING__:
                    self.getMsg.task_done()

                self.logger.debug( 'Web : ' + str(self.msg) )

                event = self.msg['event']
                data = self.msg['data']
                
                # parse msg



            # ledinfo to webpage
            self.sendAllData( ["ledData", self.ledArray.tolist()] )        
                
            # continue message handler
            tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(milliseconds=100), self.msgHandler)
            
        except Exception as e:
            self.logger.exception(str(e))
            raise


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

        #self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        WSHandler.clients[self.id] = {"id": self.id, "object": self}
        self.logger.info("Client added: id " + self.id + " IP addr: " + self.ipAddr)


    def on_close(self):
        if self.id in WSHandler.clients:
            del WSHandler.clients[self.id]
        self.logger.info("Client closed: id " + self.id + " IP address " + self.ipAddr)


    def on_message(self, message):
        self.logger.debug("Client : " + self.id + " msg: " + message)
        self.msg = json_decode(message)

        # login message
        if (self.msg['event'] == 'login'):
            if(self.verifyLogin(self.msg)):
                self.logger.info('logined in ' + self.id + " IP address " + self.ipAddr)

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

                
    #---------------------------------------------------

    def verifyLogin(self, msg):
        if((msg['data'][0] == Global.__USERNAME__) and (msg['data'][1] == Global.__PASSWORD__)):
            return True
        else:
            return False

