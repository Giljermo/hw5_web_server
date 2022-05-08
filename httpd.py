import argparse

from response_handler import handle_client_connection
from config import Config as cfg
from socket import AF_INET, SOCK_STREAM
import socket
import threading
import logging


class OtuServer:
    _socket = None

    def __init__(self,
                 host=cfg.host,
                 port=cfg.port,
                 socket_timeout=cfg.socket_timeout,
                 reconnect_delay=cfg.reconnect_delay,
                 reconnect_max_attempts=cfg.reconnect_max_attempts,
                 allow_reuse_address=cfg.allow_reuse_address,
                 worker_count=cfg.worker_count,
                 document_root=cfg.root_dir):
        self.host = host
        self.port = port
        self.socket_timeout = socket_timeout
        self.reconnect_delay = reconnect_delay
        self.reconnect_max_attempts = reconnect_max_attempts
        self.allow_reuse_address = allow_reuse_address
        self.worker_count = worker_count
        self.document_root = document_root
        self.server = None

    def server_bind(self):
        if self.allow_reuse_address:
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self.host, self.port))
        self.server = self._socket.getsockname()
        logging.info(f'Привязка к серверу "{self.host}" и порту "{self.port}" задана')

    def server_activate(self):
        self._socket = socket.socket(AF_INET, SOCK_STREAM)
        logging.info('Сокет создан')
        self.server_bind()
        self._socket.listen(self.worker_count)
        logging.info(f'Прослушиваю до "{self.worker_count}" клиентов.')

    def server_run(self):
        self.server_activate()

        while True:
            client_sock, address = self._socket.accept()
            logging.info('Получено входящее соединение от {}:{}'.format(address[0], address[1]))
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(self.server, client_sock, self.document_root)
            )
            client_handler.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--worker", help="количество обработчиков запросов", default=cfg.worker_count)
    parser.add_argument("-r", "--root", help="корневой каталог файлов", default=cfg.root_dir)
    args = parser.parse_args()

    # logging.basicConfig(filename="Client.log",
    logging.basicConfig(format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S')

    server = OtuServer(worker_count=args.worker, document_root=args.root)
    server.server_run()
