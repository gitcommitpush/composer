from modules.env import EnvironmentManager
from modules.apps import AppConfigManager, AppManager


class Env(object):
    def set(self, app_name, key, value):
        manager = EnvironmentManager(AppConfigManager(AppManager(app_name)))
        manager.set(key, value)

    def clear(self, app_name, key):
        manager = EnvironmentManager(AppConfigManager(AppManager(app_name)))
        manager.clear(key)
