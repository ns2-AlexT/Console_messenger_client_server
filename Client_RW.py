import threading
from socket import *
import JIM
from Log.client_log import client_log
from common_def import parser, get_json, send_json


def client_msg(client_socket, client_name):
    while True:
        user_input = input('enter command ')
        if user_input == 'q':
            break
        elif user_input == 'l':
            JIM.body_of_msg['from'], JIM.body_of_msg['msg'], JIM.body_of_msg['action'] = client_name, \
                                                                                         'list of an active users', \
                                                                                         'REQUEST'
            client_socket.send(send_json(JIM.body_of_msg, is_server=False))
        elif user_input == 'm':
            msg_to = input('message to client: ')
            msg = input('enter a text: ')
            JIM.body_of_msg['from'], JIM.body_of_msg['to'], JIM.body_of_msg['msg'], JIM.body_of_msg[
                'action'] = client_name, msg_to, msg, 'MESSAGE'
            client_socket.send(send_json(JIM.body_of_msg, is_server=False))
        else:
            pass


def server_msg(client_socket, client_name):
    while True:
        msg = get_json(client_socket.recv(JIM.default_attrs.get(
            'default_file_size')).decode(
            JIM.default_attrs.get('default_encoding')), is_server=True)
        if msg['to'] == client_name:
            print(f'\nReceived a message from {msg["from"]}\n{msg["msg"]}')


def main():
    # parsing args of CLI
    attr_from_parser = parser(is_server=False)
    try:
        if attr_from_parser.address is None:
            raise AttributeError('Client stopped. Argument -address of CLI is missing.')
        elif attr_from_parser.port is None:
            raise AttributeError('Client stopped. Argument -port of CLI is missing.')
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((attr_from_parser.address, attr_from_parser.port))
    except AttributeError as ae:
        client_log.error(ae)
    else:
        print('Connection is ready')
        client_name = input('what is your nick:  ')
        server = threading.Thread(target=server_msg, args=(client_socket, client_name))
        server.start()
        user = threading.Thread(target=client_msg, args=(client_socket, client_name))
        user.start()


if __name__ == "__main__":
    main()
