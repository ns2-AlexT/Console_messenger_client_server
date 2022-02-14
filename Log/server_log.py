import logging
import JIM
from logging.handlers import TimedRotatingFileHandler

server_log = logging.getLogger('server_log')
server_log.setLevel(logging.DEBUG)

server_formatter = logging.Formatter('%(levelname)-10s %(asctime)s %(module)s %(message)s')
server_handler = TimedRotatingFileHandler('./Log/Server_log.log', when='D', interval=1, backupCount=2,
                                          encoding=JIM.default_attrs.get('default_encoding'))
server_handler.suffix = '%Y%m%d'
server_handler.setFormatter(server_formatter)
server_log.addHandler(server_handler)
