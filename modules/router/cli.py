from modules.app.utils import app_exists, get_path
from app.logging import Logger
import os
import socket


class Router(object):
    TEMPLATE = '''
server {{
    server_name {host};

    location / {{
        proxy_pass http://localhost:{port};
    }}
}}
'''

    def set(self, host, port):
        config = self.TEMPLATE.format(
            host=host,
            port=port
        )

        print(config)
