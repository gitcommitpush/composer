from modules.apps import AppConfigManager
import os


class EnvironmentManager(object):
    def __init__(self, config_manager):
        if not isinstance(config_manager, AppConfigManager):
            raise Exception('ComposeManager requires an AppConfigManager instance.')

        self.manager = config_manager

        if 'env' not in self.manager.config.keys():
            self.manager.config['env'] = dict()

    def setup_environment(self):
        config = self.manager.get_config()
        env = config.get('env', {})
        for key, value in env.items():
            os.environ[key] = str(value)

    def set(self, key, value):
        self.manager.config['env'][key] = value
        self.manager.save()
        print('Environment variable "{}" set to "{}"'.format(key, value))

    def clear(self, key):
        if key in self.manager.config['env'].keys():
            del self.manager.config['env'][key]
            self.manager.save()
            print('Environment variable "{}" successfully deleted.'.format(key))
        else:
            raise Exception('Environment variable "{}" does not exist.'.format(key))

    def clearall(self):
        del self.manager.config['env']
        self.manager.save()
        print('Environment variables successfully cleared.')

    def ls(self):
        for key, value in self.manager.config['env'].items():
            print('{}={}'.format(key, value))
