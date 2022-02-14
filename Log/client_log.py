import logging
import JIM

client_log = logging.getLogger('client_log')
client_log.setLevel(logging.DEBUG)

client_formatter = logging.Formatter('%(levelname)-10s %(asctime)s %(module)s %(message)s')
client_handler = logging.FileHandler('./Log/Client.log', mode='a', encoding=JIM.default_attrs.get(
    'default_encoding'))
client_handler.setFormatter(client_formatter)
client_log.addHandler(client_handler)
