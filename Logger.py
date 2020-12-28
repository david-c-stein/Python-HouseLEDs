import sys
import traceback
import threading
import multiprocessing
import gzip
import itertools
import os
import shutil
import logging


class MultiProcessingLog(logging.Handler):
    def __init__(self, filename, mode, maxBytes, backupCount):
        logging.Handler.__init__(self)

        self._handler = logging.handlers.RotatingFileHandler(filename, mode, maxBytes, backupCount)
        self.queue = multiprocessing.Queue(-1)

        thrd = threading.Thread(target=self.receive)
        thrd.daemon = True
        thrd.start()

    def setFormatter(self, fmt):
        logging.Handler.setFormatter(self, fmt)
        self._handler.setFormatter(fmt)

    def receive(self):
        while True:
            try:
                record = self.queue.get()
                self._handler.emit(record)
                #print('received on pid {}'.format(os.getpid()))
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)

    def send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            dummy = self.format(record)
            record.exc_info = None

        return record

    def emit(self, record):
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        for i in itertools.count(1):
            nextName = "%s.%d.gz" % (self.baseFilename, i)
            if not os.path.exists(nextName):
                with open(self.baseFilename, 'rb') as original_log:
                    with gzip.open(nextName, 'wb') as gzipped_log:
                        shutil.copyfileobj(original_log, gzipped_log)
                os.remove(self.baseFilename)
                break

        if not self.delay:
            self.stream = self._open()
    
    def close(self):
        self._handler.close()
        logging.Handler.close(self)



logConfig = {
    'version': 1,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '[%(levelname)-4s][%(asctime)-15s][%(filename)-14s][%(funcName)-10s][%(lineno)-3s] : %(message)s'
        },
        'simple': {
            'class': 'logging.Formatter',
            'format': '[%(levelname)-4s] : %(message)s'
        }       
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'stream' : 'ext://sys.stdout'
        },
        'file': {
            'class': 'Logger.MultiProcessingLog',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'appLogger.log',
            'mode': 'w',
            'maxBytes': 0,   #1024*1024,  # megabyte file
            'backupCount': 0 #3
        },
        'errors': {
            'class': 'Logger.MultiProcessingLog',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': 'appError.log',
            'mode': 'w',
            'maxBytes': 0,   #1024*1024,  # megabyte file
            'backupCount': 0 #3
        },
    },
    'filter': {
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file', 'errors']
    }   
}

# logging.config.dictConfig(logConfig)
