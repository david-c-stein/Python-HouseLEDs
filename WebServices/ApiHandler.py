import Global

import json
import time
import datetime
import os.path
import tornado.web
from tornado.escape import json_encode, json_decode
from tornado.options import options
import uuid
import base6


class ApiHandler(tornado.web.RequestHandler):

    def initialize(self, queCam, queHdw, queWeb, config):

        self.config = config
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __file__)

        # message queues
        self.getMsg = queWeb
        self.putMsgSer = queSer.put
        self.putMsgCam = queCam.put
        self.putMsgHwd = queHdw.put

    #=============================================================

    @web.asynchronous
    def get(self, *args):
        self.finish()
        id = self.get_argument("id")
        value = self.get_argument("value")
        data = {"id": id, "value" : value}
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)

    @web.asynchronous
    def post(self):
        pass
