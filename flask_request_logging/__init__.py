"""Flask Logging Request

"""

import logging
from logging import getLogger, StreamHandler, Formatter, getLoggerClass, DEBUG, ERROR
from uuid import uuid4
from flask import g, request


REQUEST_LOG_FORMAT = '[%(request_id)s] %(levelname)s in %(module)s: %(message)s'


class FlaskRequestLogFilter(logging.Filter):

    def filter(self, record):
        record.request_id = g.request_id
        return True


# class FlaskRequestLogFormatter(logging.Formatter):

#     def __init__(self, *args, **kwargs):
#         super(FlaskRequestLogFormatter, self).__init__(*args, **kwargs)

#     def format(self, record):
#         return super(FlaskRequestLogFormatter, self).format(record)


def create_logger(app):
    Logger = getLoggerClass()
    logger = getLogger(app.logger_name)

    class DebugLogger(Logger):
        def getEffectiveLevel(self):
            if self.level == 0 and app.debug:
                return DEBUG
            return Logger.getEffectiveLevel(self)

    class RequestHandler(StreamHandler):
        def emit(self, record):
            StreamHandler.emit(self, record)

    debug_handler = DebugHandler()
    debug_handler.setLevel(DEBUG)
    debug_handler.setFormatter(Formatter(REQUEST_LOG_FORMAT))

    # just in case that was not a new logger, get rid of all the handlers
    # already attached to it.
    del logger.handlers[:]
    logger.__class__ = DebugLogger
    logger.addHandler(debug_handler)

    # Disable propagation by default
    logger.propagate = False

    return logger







def update_factory():
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.request_id = 'rrrrrrrrrrrr'
        return record

    logging.setLogRecordFactory(record_factory)


def init_app(app):

    @app.before_request
    def request_log():
        g.request_id = request.headers.get(app.config['LOGGING_HEADER_ID_NAME'], uuid4().hex)
    
    update_factory()

    ftr = FlaskRequestLogFilter()
    app.logger.addFilter(ftr)
    
