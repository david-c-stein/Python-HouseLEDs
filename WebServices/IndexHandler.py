
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
                <link href="static/assets/css/bootstrap.min.css" rel="stylesheet">
                <link href="static/assets/css/ledstrip.css" rel="stylesheet" >
                <link href="static/assets/css/mdtimepicker.css" rel="stylesheet">

                <script src="static/assets/js/jquery-3.5.1.min.js"></script>
                <script src="static/assets/js/bootstrap.min.js"></script>
                <script src="static/assets/js/rAF.js"></script>
                <script src="static/assets/js/ledstrip.js"></script>
                <script src="static/assets/js/ws2812.js"></script>
                <script src="static/assets/js/arduino_funcs.js"></script>
                <script src="static/assets/js/generator.js"></script>
                <script src="static/assets/js/mdtimepicker.js"></script>
            </head>
            <body id="body">
                <noscript>
                    <div class='enableJS'>You need to enable javascript</div>
                </noscript>

                <div class="container-fluid">
                    <div class="row">
                        <div class="col-md-12">
                            <center>
                            <div class="page-header">
                                <h1>House Holiday Lights</h1>
                                <h3>A work in progress</h3>
                            </div>
                            </center>
                        </div>
                    </div>
                    <hr/>
                    <div class="row">
                        <div class="col-md-2">
                            <select id="animselect">
                                 <option value="pattern">Pattern</option>
                                 <option value="stop">Stop</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <input type="checkbox" id="forceon" value="0" /> <label for="forceon">Force ON</label>
                        </div>
                        <div class="col-md-3">
                            <input type="text" id="startTimePicker"/> <label for="startTimePicker">Start time</label>
                        </div>
                        <div class="col-md-3">
                            <input type="text" id="stopTimePicker"/> <label for="stopTimePicker">Stop time</label>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="ledstrip"></div>
                        </div>
                    </div>
                </div>

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
                                return this;      // chainable
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
                                    return;  // no callbacks for this event
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

                            socket.bind('forceOn', function(data) {
                                selectForceOn(data);
                            })

                            socket.bind('pattern', function(data) {
                                changeAnimation(data);
                            })

                            socket.bind('selectPattern', function(data) {
                                selectPattern(data);
                            })

                            socket.bind('addPattern', function(data) {
                                addPattern(data);
                            })

                            socket.bind('ledData', function(data) {
                                if (typeof driver.setLEDs === "function") {
                                    driver.setLEDs(data, data.length);
                                }
                            })

                            socket.bind('startTimePicker', function(data) {
                                console.log('startTimePicker from BO : ' + data)
                                $('#startTimePicker').mdtimepicker('setValue', data);
                            })

                            socket.bind('stopTimePicker', function(data) {
                                console.log('stopTimePicker from BO : ' + data)
                                $('#stopTimePicker').mdtimepicker('setValue', data);
                            })
                        };
                    }

                    //===========================================================================

                    var strip, animation;
                    var container = $('.ledstrip')[0];
                    var light_count = """ + str(self.ledCount) + """;
                    strip = LEDstrip(container, light_count);
                    driver = new Generator(strip);
                    driver.init();
                    animation = driver.animate.bind(driver)();

                    $('#forceon').change(function(e) {
                        var forceOn = $(e.target).val();
                        console.log('force on ' + forceon.checked);
                        sendMsg('forceOn', forceon.checked);
                    });

                    $('#animselect').change(function(e) {
                        var newanim = $(e.target).val();
                        console.log('change to ' + newanim);
                        sendMsg('pattern', newanim);
                    });

                    $('#startTimePicker').mdtimepicker({theme: 'green'}).on('timechanged', function(e){
                        console.log('startTimePicker ' + e.time);
                        sendMsg('startTimePicker', e.time);   // data-time value
                    });

                    $('#stopTimePicker').mdtimepicker().on('timechanged', function(e){
                        console.log('stopTimePicker ' + e.time);
                        sendMsg('stopTimePicker', e.time);   // data-time value
                    });


                    function changeAnimation(newanim){
                        animation = cancelAnimationFrame(animation);
                        switch(newanim) {
                            case 'stop':
                                animation = cancelAnimationFrame(animation);
                                return;
                                break;
                            default:
                                driver = new Generator(strip);
                                break;
                        }
                        driver.init();
                        animation = driver.animate();
                    }

                    function addPattern(pattern){
                        var option = document.createElement('option');
                        option.text = pattern;
                        option.value = pattern;
                        var select = document.getElementById('animselect');
                        select.appendChild(option);
                    }

                    function selectPattern(pattern){
                        var element = document.getElementById('animselect');
                        element.value = pattern;
                    }

                    function selectFOrceOn(forceOn){
                        console.log('force on: ' + forceOn)
                        document.getElementById('forceon').checked = forceOn;

                    }

                </script>
            </body>
        </html>
        """)

        self.finish()

    def write_error(self, status_code, **kwargs):
        self.write("Opps a %d error." % status_code)

