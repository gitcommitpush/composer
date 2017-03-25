from modules.app.utils import app_exists, get_path
from app.logging import Logger
import subprocess
import os
import socket


class Compose(object):
    """
    Compose projects using docker-compose.
    """
    def configure_env(self):
        os.environ['COMPOSER_PORT'] = self.obtain_available_port()

    def _get_to_app(self, app):
        if not app_exists(app):
            raise ValueError('App "{}" does not exist.'.format(app))

        os.chdir(get_path(app))
        self.configure_env()

    def obtain_available_port(self):
        sock = socket.socket()
        sock.bind(('', 0))
        open_port = sock.getsockname()[1]
        sock.close()
        return str(open_port)

    def up(self, app):
        self._get_to_app(app)
        subprocess.call('docker-compose up -d', shell=True)

    def down(self, app):
        self._get_to_app(app)
        subprocess.call('docker-compose down', shell=True)
