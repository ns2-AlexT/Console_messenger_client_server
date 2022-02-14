import select
from socket import *
import JIM
from Log.server_log import server_log
from common_def import send_json, get_json, parser, check_status


def from_users(from_user, clients, dict_msg_from_users, to_users_msg):
    for user in from_user:
        try:
            msg_from_user = get_json(user.recv(JIM.default_attrs.get('default_file_size')).decode(
                JIM.default_attrs.get('default_encoding')), is_server=True)
            dict_msg_from_users[user] = msg_from_user
        except Exception as e:
            clients.remove(user)
    return dict_msg_from_users


def w_user(r, w_clients, clients):
    for str_from_r in r:
        for w_client in w_clients:
            # preparing for sending to client a list of an active users
            # print(r[str_from_r]['action'])
            # print(r[str_from_r]['from'])
            # if ((r[str_from_r]['action'] == 'REQUEST') & (r[str_from_r]['from'] == w_client)) :
            #     val = 'list of an active users'
            # else:
            val = r[str_from_r]
            try:
                w_client.send(send_json(val, is_server=True))
            except Exception as e:
                w_client.close()
                clients.remove(w_client)


def main():
    attr_from_parser = parser(is_server=True)
    clients = []
    try:
        if attr_from_parser.address is None:
            raise AttributeError('Server stopped. Argument -address of CLI is missing.')
        elif attr_from_parser.port is None:
            raise AttributeError('Server stopped. Argument -port of CLI is missing.')
        try:
            sock_server = socket(AF_INET, SOCK_STREAM)
            sock_server.bind((attr_from_parser.address, attr_from_parser.port))
            sock_server.listen(JIM.default_attrs.get('default_max_connections'))
            sock_server.settimeout(0.2)
            server_log.info('Server has started.')
        except Exception as e:
            server_log.error(e)

        while True:
            try:
                connect, addr = sock_server.accept()
            except OSError as e:
                pass
            else:
                print(f'Add client ==>> {addr}')
                clients.append(connect)
            from_users_msg = []
            to_users_msg = []
            dict_msg_from_users = {}
            try:
                from_users_msg, to_users_msg, err_user = select.select(clients, clients, [], 0)
            except Exception as e:
                print(f'Something went wrong {e}')
            list_msg_from_user = from_users(from_users_msg, clients, dict_msg_from_users, to_users_msg)
            if list_msg_from_user:
                print(f'We have msg from users: {list_msg_from_user}')
                w_user(list_msg_from_user, to_users_msg, clients)
    except AttributeError as ae:
        server_log.error(ae)


if __name__ == "__main__":
    main()
