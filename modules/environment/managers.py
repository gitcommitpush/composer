from core.managers import BaseManager
from modules.apps.managers import AppConfigManager, AppManager
import os


class EnvironmentManager(BaseManager):
    def __init__(self, config_manager, env_name='default'):
        if not isinstance(config_manager, AppConfigManager):
            raise TypeError('Config manager should be an instance of AppConfigManager.')

        self.config_manager = config_manager
        self.app = self.config_manager.app  # App instance
        self.env = env_name

        if 'env' not in self.config_manager.config.keys():
            self.config_manager.config['env'] = dict()
            if 'default' not in self.config_manager.config['env'].keys():
                # Make sure default environment always exists
                self.config_manager.config['env']['default'] = dict()

        super().__init__()

    def should_exist(self):
        # Expect an environment to exist
        if self.env not in self.config_manager.config['env'].keys():
            self.logger.fail('Environment "{}" does not exist.'.format(self.env))

    def should_not_exist(self):
        # Expect an environment not to exist
        if self.env in self.config_manager.config['env'].keys():
            self.logger.fail('Environment "{}" already exists.'.format(self.env))

    def create(self):
        # Create an environment
        self.should_not_exist()

        self.config_manager.config['env'][self.env] = dict()
        self.config_manager.save()

        self.logger.info('Environment "{}" created.'.format(self.env))

    def delete(self):
        # Delete an environment
        self.should_exist()

        del self.config_manager.config['env'][self.env]
        self.config_manager.save()

        self.logger.info('Environment "{}" deleted.'.format(self.env))

    def set(self, **kwargs):
        # Set environment variable(s)
        self.should_exist()

        for env_key, env_value in kwargs.items():
            self.config_manager.config['env'][self.env][env_key.upper()] = env_value

        self.config_manager.save()

    def unset(self, *args):
        # Unset environment variable(s)
        self.should_exist()

        for env_key in args:
            try:
                del self.config_manager.config['env'][self.env][env_key.upper()]
            except KeyError:
                self.logger.warn('Environment variable "{}" not found in environment "{}"'.format(env_key, self.env))

    def ls(self):
        # List variables in an environment
        self.should_exist()

        for env_key, env_value in self.config_manager.config['env'][self.env].items():
            print('{}={}'.format(env_key, env_value))

    def setup_environment(self):
        # Load variables into OS environment
        self.should_exist()

        for env_key, env_value in self.config_manager.config['env'][self.env].items():
            os.environ[env_key] = env_value

        self.logger.info('Environment "{}" loaded.'.format(self.env))
