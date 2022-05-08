import os
import logging
from datetime import datetime as dt
from urllib.parse import unquote


DELIMETR = '\r\n'
DOUBLE_DELIMETR = DELIMETR * 2
OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
INVALID_REQUEST = 422
INTERNAL_ERROR = 500
DESCRIPTIONS = {
    OK: 'OK',
    BAD_REQUEST: "Bad Request",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    INVALID_REQUEST: "Invalid Request",
    INTERNAL_ERROR: "Internal Server Error",
}


class Response:
    allowed_method = ['GET', 'HEAD']
    max_size = 2048

    def __init__(self, server, root):
        self.root = root
        self.server = server
        self.method = ''
        self.http_version = ''
        self.path = ''
        self.args = ''
        self.file_path = ''  # путь до запрашиваемого файла
        self.file_content = ''
        self.response_content = ''

    def parse_request(self, request):
        """определить следующие объекты: метод, версию http, путь, """
        client_content = self._get_client_content(request)

        if not client_content:
            logging.info('Данные отстусвуют, завршаю парсинг данных')
            return

        service_content, *other = client_content.split(DELIMETR)
        self.method, self.path, self.http_version = service_content.split()
        self.path = unquote(self.path.lstrip('/'))

        if '?' in self.path:
            self.path, self.args = self.path.split('?')

    def create_content(self):
        """сформировать ответную строку для клиента"""
        try:
            self._prepare_content()
        except FileNotFoundError as err:
            logging.error(err)
            self.do_HEAD(NOT_FOUND)
            return

        if self.method not in self.allowed_method:
            logging.error(f'Не разрешенный метод "{self.method}"')
            self.do_HEAD(BAD_REQUEST)
            return

        self.do_HEAD(OK) if self.method == 'HEAD' else self.do_GET(OK)

    def do_HEAD(self, code):
        self.response_content = f'{self.http_version} {code} {DESCRIPTIONS[code]}{DELIMETR}'.encode()
        self.set_headers()

    def do_GET(self, code):
        self.do_HEAD(code)
        self.response_content += self.file_content

    def set_headers(self):
        """задать заголовки ответа"""
        headers = [
            f'Server: {self.server}',
            f'Date: {dt.now().strftime("%Y.%m.%d %H:%M:%S")}',
            f'Content-Type: {self.get_content_type(self.file_path)}',
            f'Content-Length: {len(self.file_content)}',
            f'Connection: keep-alive'
        ]

        self.response_content += f'{DELIMETR}'.join(headers).encode() + DOUBLE_DELIMETR.encode()

    def _get_client_content(self, request):
        """получить все содержимое от клиента"""
        fragments = []
        while True:
            chunk = request.recv(self.max_size).decode('utf-8')
            fragments.append(chunk)
            if not chunk or DOUBLE_DELIMETR in chunk:
                break

        messages = "".join(fragments)
        logging.info(f'Считаны данные "{messages}"')
        return messages.strip(DOUBLE_DELIMETR)

    def _prepare_content(self):
        """получаем путь до возвращаемого файла"""
        if os.path.isfile(self.path):
            self.file_path = os.path.join(self.root, self.path)
        else:
            self.file_path = os.path.join(self.path, 'index.html')

        with open(self.file_path, 'rb') as f:
            self.file_content = f.read()

    def get_content_type(self, content: str):
        """определить тип документа"""
        if content.endswith('.html') or content.endswith('.txt'):
            return 'text/html'
        elif content.endswith('.css'):
            return "text/css"
        elif content.endswith('.js'):
            return "text/javascript"
        elif content.endswith('.jpeg') or content.endswith('.jpg'):
            return "image/jpeg"
        elif content.endswith('.gif'):
            return "image/gif"
        elif content.endswith('.png'):
            return "image/png"
        elif content.endswith('.swf'):
            return "application/x-shockwave-flash"

        return ''


def handle_client_connection(server, client_request, document_root):
    logging.info('Начинаю обработку запроса:')
    response = Response(server, document_root)
    response.parse_request(client_request)
    response.create_content()
    client_request.send(response.response_content)
    client_request.close()
