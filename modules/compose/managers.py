from core.managers import BaseManager
from modules.router.managers import RouterManager
import os
import sh
import socket
import subprocess


class ComposeManager(BaseManager):
    def __init__(self, app):
        self.router = RouterManager(app)
        self.app = app

        super().__init__()

    def up(self, force_build=True):
        os.chdir(self.app.get_data_path())
        port = self.router.get_available_port()
        os.environ['COMPOSER_PORT'] = str(port)

        self.logger.info('Composing app...')

        try:
            try:
                cmd = ['docker-compose', 'up', '-d']
                if force_build:
                    cmd.append('--build')
                subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as error:
                self.logger.fail('Problem composing app', extra=error.output)
            self.logger.info('Started successfully.')
        except sh.ErrorReturnCode as e:
            self.logger.fail('There was a problem starting the container: \n\n{}'.format(e))

        self.router.define_route(port)

    def down(self):
        os.chdir(self.app.get_data_path())

        try:
            self.logger.info('Stopping app...')
            sh.docker_compose('down')
            self.logger.info('Stopped successfully.')
        except sh.ErrorReturnCode as e:
            self.logger.fail('There was a problem stopping the container: \n\n{}'.format(e))
