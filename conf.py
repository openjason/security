import logging
from logging.handlers import RotatingFileHandler

DBhost='1.1.1.177'
DBhost='192.168.18.101'
DBuser='jcc'
DBpassword='pwd123456'
DBname='stock'

def set_logging():
    global logger
    logger = logging.getLogger('balance_logger')
    handler = logging.handlers.RotatingFileHandler('日志记录.log', maxBytes=5000000, backupCount=6)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    formatter = logging.Formatter('%(asctime)-12s %(filename)s %(lineno)d %(message)s')
    handler.setFormatter(formatter)