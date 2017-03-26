from modules.apps import AppConfigManager
from modules.env import EnvironmentManager
import os
import subprocess


class ComposeManager(object):
    def __init__(self, config_manager):
        if not isinstance(config_manager, AppConfigManager):
            raise Exception('ComposeManager requires an AppConfigManager instance.')

        self.manager = config_manager
        self.environment = EnvironmentManager(config_manager)
        self.environment.setup_environment()

    def up(self):
        os.chdir(self.manager.app.get_data_path())
        subprocess.call('docker-compose up -d', shell=True)

    def down(self):
        os.chdir(self.manager.app.get_data_path())
        subprocess.call('docker-compose down', shell=True)
