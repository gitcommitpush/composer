from core.managers import BaseManager
from modules.apps.managers import AppConfigManager, AppManager
import os


class EnvironmentManager(BaseManager):
    def __init__(self, config_manager, env_name='default'):
        if not isinstance(config_manager, AppConfigManager):
            raise TypeError('Config manager should be an instance of AppConfigManager.')

        self.config_manager = config_manager
        self.app = config_manager.app  # App instance
        self.env_name = env_name

        if 'env' not in config_manager.config.keys():
            config_manager.config['env'] = dict()

        self.env = config_manager.config['env']
        if 'default' not in self.env.keys():
            # Make sure default environment always exists
            self.env['default'] = dict()

        super().__init__()

    def should_exist(self):
        # Expect an environment to exist
        if self.env_name not in self.env.keys():
            self.logger.fail('Environment "{}" does not exist.'.format(self.env_name))

    def should_not_exist(self):
        # Expect an environment not to exist
        if self.env_name in self.env.keys():
            self.logger.fail('Environment "{}" already exists.'.format(self.env_name))

    def create(self):
        # Create an environment
        self.should_not_exist()

        self.env[self.env_name] = dict()
        self.config_manager.save()

        self.logger.info('Environment "{}" created.'.format(self.env_name))

    def delete(self):
        # Delete an environment
        self.should_exist()

        del self.env[self.env_name]
        self.config_manager.save()

        self.logger.info('Environment "{}" deleted.'.format(self.env_name))

    def set(self, **kwargs):
        # Set environment variable(s)
        self.should_exist()

        for env_key, env_value in kwargs.items():
            self.env[self.env_name][env_key.upper()] = env_value

        self.config_manager.save()

    def unset(self, env_key):
        # Unset environment variable(s)
        self.should_exist()

        del self.env[self.env_name][env_key.upper()]

        self.logger.info('Successfully removed "{}" from environment "{}".'.format(env_key, self.env_name))

    def ls(self):
        # List variables in an environment
        self.should_exist()

        for env_name, env_items in self.env.items():
            print('[{}]'.format(env_name))
            for env_key, env_val in env_items.items():
                print('{}={}'.format(env_key, env_val))

    def setup_environment(self):
        # Load variables into OS environment
        self.should_exist()

        for env_key, env_value in self.env[self.env_name].items():
            os.environ[env_key] = str(env_value)

        self.logger.info('Environment "{}" loaded.'.format(self.env_name))
