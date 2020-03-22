
import tornado.web
import logging
import logging.config
import uuid


class IndexHandler(tornado.web.RequestHandler):

    def initialize(self, config, ledCount):
        
        self.config = config

        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing " + __file__)
       
        self.address = self.config["IPADDRESS"]
        self.port = self.config["SOCKETIOPORT"]

        self.ledCount = ledCount
        
    @tornado.web.asynchronous
    def get(self):

        title = 'House Lights'

        self.write( """
        <!DOCTYPE html>
        <html>
            <head id="head">
                <title>""" + title + """</title>
                <meta charset="utf-8" />
                <link rel="stylesheet" href="static/assets/css/ledstrip.css" />
                
                <script src="static/assets/js/jquery.js"></script>
                <script src="static/assets/js/rAF.js"></script>
                <script src="static/assets/js/ledstrip.js"></script>
                <script src="static/assets/js/ws2812.js"></script>
                <script src="static/assets/js/arduino_funcs.js"></script>
                <script src="static/assets/js/generator.js"></script>
            </head>
            <body id="body">
                <noscript>
                    <div class='enableJS'>You need to enable javascript</div>
                </noscript>

            <!-- Main -->
                <!-- Main content -->
                <div id="main" class="container">


         <div class="ledstrip"></div>
         
         
         <br />
         <br />
         <br />
         <br />
         <br />
         <br />
         
         <form>
           <select id="animselect">
             <option value="generator">Generator</option>
             <option value="stop">Stop</option>
           </select>
           <input type="checkbox" id="diffuser" value="0" /> <label for="diffuser">Diffuser</label>
         </form>
         <p id="output"></p>
         <p>For more information:</p>


                </div>

            <!-- Footer -->
                <footer id="footer">
                    <div class="copyright">
                        David Stein : 2019
                    </div>
                </footer>

                <!-- Start of websocket yummy goodness -->

                <script type="text/javascript" id="wsScript">

                    var socket;

                    function sendMsg(event_name, event_data) {
                        if(socket) {
                            socket.send(event_name, event_data);
                        }
                    }

                    window.onload = function() {

                        var websocket = false;

                        if("WebSocket" in window) {
                            websocket = true;
                        } else {
                            console.log("WebSocket are not supported by this browser");
                        }

                        var mySocket = function() {
                            var ws;
                            var callbacks = {};

                            try {
                                // ensure only one connection is open
                                if(ws !== undefined && ws.readyState !== ws.CLOSED) {
                                    console.log("WebSocket is already open");
                                    return;
                                }
                                // c an instance of the websocket
                                ws = new WebSocket("ws://""" + self.address + """:""" + str(self.port) + """/ws/");
                            }
                            catch(e) {
                                console.log(e.message);
                            };

                            this.bind = function(event_name, callback) {
                                callbacks[event_name] = callbacks[event_name] || [];
                                callbacks[event_name].push(callback);
                                return this;                       // chainable
                            };

                            this.unbind = function(event_name) {
                                delete callbacks[event_name];
                            };

                            this.send = function(event_name, event_data) {
                                var payload = JSON.stringify({event: event_name, data:event_data});
                                waitForSocket(ws, function(){
                                    ws.send(payload);
                                });
                                return this;
                            };

                            function waitForSocket(socket, callback) {
                                setTimeout(
                                    function () {
                                        if (socket.readyState === socket.OPEN) {
                                            // connection is ready
                                            if(callback != null)
                                                callback();
                                            return;
                                        } else {
                                            // connection is not ready yet
                                            waitForSocket(socket, callback)
                                        }
                                   }, 5);  // wait 5 milliseconds for connection
                            };

                            ws.onmessage = function(env) {
                                var j = JSON.parse(env.data);
                                dispatch(j[0], j[1]);
                            };

                            ws.onclose = function() {
                                dispatch('closed', null);
                                disableAll();
                            }

                            ws.onopen = function() {
                                dispatch('opened', null);
                            }

                            ws.onerror = function(evt) {
                                var err = evt.data;
                                console.log("Error occured");
                                dispatch('error', err);
                                disableAll();
                            };

                            var dispatch = function(event_name, message) {
                                var chain = callbacks[event_name];
                                if (typeof chain == 'undefined')
                                    // no callbacks for this event
                                    return;             
                                for(var i = 0; i < chain.length; i++)
                                    chain[i](message);
                            }
                        };

                        //-------------------------------------------------

                        if (websocket == true) {

                            socket = new mySocket();

                            socket.bind('opened', function(env) {
                                ;
                            })

                            socket.bind('closed', function(env) {
                                ;
                            })

                            socket.bind('error', function(env) {
                                ;
                            })

                            socket.bind('ledData', function(data) {
                                //console.log(data)
                                if (typeof driver.setLEDs === "function") {
                                    var i
                                    var size = data.length

                                    driver.setLEDs(data, size)
                                }
                            })

                        };
                    }


                    //===========================================================================


                    var strip, animation;  // Global

                    var container = $('.ledstrip')[0];
                    var light_count = """ + str(self.ledCount) + """;
                    strip = LEDstrip(container, light_count);
                    driver = new Generator(strip);
                    driver.init();
                    animation = driver.animate.bind(driver)();

                    $('#diffuser').change(function(e) {
                        $('.ledstrip').toggleClass('diffuse');
                    });

                    $('#animselect').change(function(e) {
                        var newanim = $(e.target).val();
                        console.log('change to ' + newanim); 
                        animation = cancelAnimationFrame(animation);
                        switch(newanim) {
                            case 'generator':
                                driver = new Generator(strip);
                                break;
                            case 'stop':
                                animation = cancelAnimationFrame(animation);
                                return;
                                break;
                            } // /switch
                        
                        driver.init();
                        animation = driver.animate();
                    });
                   

                </script>
            </body>
        </html>
        """)

        self.finish()

    def write_error(self, status_code, **kwargs):
        self.write("Opps a %d error." % status_code)

