from core.managers import BaseManager
from modules.apps.managers import AppConfigManager
from modules.environment.managers import EnvironmentManager
from modules.router.managers import RouterManager
import os
import sh
import socket


class ComposeManager(BaseManager):
    def __init__(self, environment_manager):
        if not isinstance(environment_manager, EnvironmentManager):
            raise TypeError('Environment manager should be an instance of EnvironmentManager.')

        self.environment_manager = environment_manager
        self.config_manager = environment_manager.config_manager
        self.router_manager = RouterManager(environment_manager.config_manager)
        self.app = self.config_manager.app

        self.environment_manager.setup_environment()

        super().__init__()

    def get_available_port(self):
        sock = socket.socket()
        sock.bind(('', 0))
        available_port = sock.getsockname()[1]
        sock.close()
        return available_port

    def up(self):
        os.chdir(self.config_manager.app.get_data_path())
        port = self.get_available_port()
        os.environ['COMPOSER_PORT'] = str(port)

        try:
            self.logger.info('Starting app...')
            sh.docker_compose('up', '-d')
            self.logger.info('Started successfully.')
            self.logger.info('Routing hostname to container...')
            self.router_manager.define_route(port)
            self.logger.info('Successfully routed hostname to container and should be accessible at: {}'.format(
                self.router_manager.get_hostname())
            )
        except sh.ErrorReturnCode as e:
            self.logger.fail('There was a problem starting the container: \n\n{}'.format(e))

    def down(self):
        os.chdir(self.config_manager.app.get_data_path())

        try:
            self.logger.info('Stopping app...')
            sh.docker_compose('down')
            self.logger.info('Stopped successfully.')
        except sh.ErrorReturnCode as e:
            self.logger.fail('There was a problem stopping the container: \n\n{}'.format(e))
