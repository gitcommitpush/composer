from modules.environment import EnvironmentManager
from modules.apps import AppConfigManager, AppManager


class Env(object):
    def _get_manager(self, app_name):
        return EnvironmentManager(AppConfigManager(AppManager(app_name)))

    def set(self, app_name, key, value):
        manager = self._get_manager(app_name)
        manager.set(key, value)

    def clear(self, app_name, key):
        manager = self._get_manager(app_name)
        manager.clear(key)

    def clear_all(self, app_name):
        manager = self._get_manager(app_name)
        manager.clearall()

    def ls(self, app_name):
        manager = self._get_manager(app_name)
        manager.ls()
