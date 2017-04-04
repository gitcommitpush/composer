from core.managers import BaseManager
from core import settings
from modules.apps.managers import AppManager
import os
import subprocess
import socket
import time


class RouterManager(BaseManager):
    def __init__(self, app):
        self.app = app
        self.config = app.config

        super().__init__()

    def get_hostname(self):
        return self.config.get('hostname', '{}.{}'.format(self.app.get_name(), settings.BASE_DOMAIN))

    def get_config_template(self):
        return self.app.get_proxy_template()

    def get_available_port(self):
        sock = socket.socket()
        sock.bind(('', 0))
        available_port = sock.getsockname()[1]
        sock.close()
        return available_port

    def run_pre_check(self, port):
        self.logger.info('Running pre-checks...')
        try:
            subprocess.check_output(['nc', '-z', '127.0.0.1', port])
        except subprocess.CalledProcessError:
            self.logger.fail('Container is not listening on port {}'.format(port))

        self.logger.info('Pre-checks successful.')

    def define_route(self, port):
        self.logger.info('Routing hostname to container...')
        content = self.get_config_template().format(hostname=self.get_hostname(), port=port)

        try:
            with open(self.app.get_proxy_config_path(), 'w+') as f:
                f.write(content)
                f.close()
        except IOError:
            self.logger.fail('Routing failed: could not write proxy config file')

        try:
            process = subprocess.check_output(['service', 'nginx', 'restart'], stderr=subprocess.STDOUT)
        except FileNotFoundError:
            self.logger.fail('Routing failed: command "service" not found. Possibly an unsupported operating system?')
        except subprocess.CalledProcessError as error:
            self.logger.warn('Routing failed: could not restart proxy service', extra=error.output)

        self.logger.info('Routing successful.')

        self.run_pre_check(port)

        self.logger.info('Map [ {} => 127.0.0.1:{} ]'.format(self.get_hostname(), port))
        self.logger.info('You can also access this application via port {}'.format(port))
