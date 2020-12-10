import Global

if Global.__MULTIPROCESSING__:
    import multiprocessing

import os
import socket
import sys
import threading
import tornado
from tornado import gen
import logging
import logging.config

from subprocess import *


class WebServices(multiprocessing.Process if Global.__MULTIPROCESSING__ else threading.Thread):

    def __init__(self, qAud, qHdw, qWeb, config, sharedArrayBase, ledCount):

        if Global.__MULTIPROCESSING__:
            # -- multiprocessing
            multiprocessing.Process.__init__(self)
        else:
            # -- threading
            super(WebServices, self).__init__()

        self.config = config

        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __file__)

        self.sharedArrayBase = sharedArrayBase
        self.ledCount = ledCount

        # message queues
        self.qAud = qAud
        self.qHdw = qHdw
        self.qWeb = qWeb

        if os.name == "nt":
            # windows
            self.config["IPADDRESS"] = socket.gethostbyname(socket.gethostname())
        else:
            # linux
            self.config["IPADDRESS"] = self.get_ip_address("eth0")

    @gen.coroutine
    def run(self):
        # called on start() signal
        try:
            self.logger.info("Running Web process")

            # Identify network information
            self.config["DIRNAME"] = os.path.dirname(__file__)
            self.logger.info("IPAddress: " + str(self.config["IPADDRESS"]))
            self.logger.info("HTTPport: " + str(self.config["HTTPPORT"]))
            self.logger.info("SocketIOport: " + str(self.config["SOCKETIOPORT"]))

            # HTTP Web and WebSocket servers
            import HTTPHandler
            http_server = tornado.httpserver.HTTPServer(
                HTTPHandler.HTTPHandler(self.qAud, self.qHdw, self.qWeb, self.config, self.sharedArrayBase,
                                        self.ledCount))
            http_server.listen(self.config["HTTPPORT"])

            # Error handler
            import ErrorHandler

            # Get it all running
            tornado.ioloop.IOLoop.current().start()

        except(KeyboardInterrupt, SystemExit):
            self.logger.info("Interupted HW process")

        except Exception as e:
            self.logger.exception(e)

        # Web services stopping
        http_server.stop()
        http_server.close_all_connections()
        self.logger.info("tornado http server stopped")

    def stop(self):
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.make_current()
        ioloop.clear_current()

    def get_ip_address(self, ifname):
        # linux
        if sys.version_info[0] < 3:

            # RaspberryPi
            # :o(

            cmd = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
            p = Popen(cmd, shell=True, stdout=PIPE)
            output = p.communicate()[0]
            return output.replace('\n', '').replace('\r', '')

            # python 2
            # import fcntl
            # import struct
            # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # return socket.inet_ntoa( fcntl.ioctl(
            #        s.fileno(),
            #        0x8915, # SIOCGIFADDR
            #        struct.path('256s', ifname[:15])
            #    )[20:24])
        else:
            # python 3
            return socket.gethostbyname(socket.getfqdn())
