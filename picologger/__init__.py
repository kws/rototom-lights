import adafruit_logging 
from adafruit_logging import LEVELS, Handler, StreamHandler

for __value, __name in LEVELS:
    globals()[__name] = __value

_old_logger = adafruit_logging.getLogger
def getLogger(name):
    return _old_logger()
adafruit_logging.getLogger = getLogger

def getRootLogger():
    return getLogger("")


__root_logger = getRootLogger()
def __exception(message, *args, exception=None, **kwargs):
    if exception:
        import traceback
        message = "\n".join([message] + traceback.format_exception(exception.__class__, exception))

    __root_logger.error(message, *args, **kwargs)
    
__root_logger.exception = __exception
