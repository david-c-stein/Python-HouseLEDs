
import Global

if Global.__MULTIPROCESSING__:
    import multiprocessing

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import logging.config

import IndexHandler
import WSHandler
import ErrorHandler
       
# HTTP Web Service
class HTTPHandler( tornado.web.Application ):

    def __init__(self, qApp, qAud, qWeb, qPat, config, sharedArrayBase, ledCount):
        
        self.config = config

        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __file__)

        # message queues
        self.qApp = qApp
        self.qAud = qAud
        self.qWeb = qWeb
        self.qPat = qPat

        try:

            self.sharedArrayBase = sharedArrayBase
            self.ledCount = ledCount

            self.static_dir = os.path.join(self.config["DIRNAME"], "static")
            self.static_dir_dict = dict(path=self.static_dir)

            # define handlers
            self.handlers = [
                # public
                (r'/', IndexHandler.IndexHandler, dict(config=self.config, ledCount=self.ledCount)),
                (r'/ws/(.*)', WSHandler.WSHandler, dict(qApp=self.qApp, qAud=self.qAud, qWeb=self.qWeb, qPat=self.qPat, config=self.config, sharedArrayBase=self.sharedArrayBase, ledCount=self.ledCount)),
                (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path" : 'static/favicon.ico'}),
                (r'/(.*.js)', tornado.web.StaticFileHandler, {"path" : 'static/assets/js/.*.js'})
            ]

            self.settings = dict(
                debug=False,                    ### Enable debugging
                autoreload=False,               ### Disable server autoreload
                cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies=False,
            )

            tornado.web.Application.__init__(self, handlers=self.handlers, default_host="", transforms=None, **self.settings)

        except Exception as e:
            self.logger.exception(e)


