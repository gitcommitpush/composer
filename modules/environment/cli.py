from core.cli import BaseCommandLine
from modules.environment.managers import EnvironmentManager
from modules.apps.managers import AppManager, AppConfigManager


class Env(BaseCommandLine):
    def _get_manager(self, app, environment):
        return EnvironmentManager(AppConfigManager(AppManager(app)), env_name=environment)

    def set(self, app, environment='default', **kwargs):
        manager = self._get_manager(app, environment)
        manager.set(**kwargs)

    def ls(self, app, environment='default'):
        manager = self._get_manager(app, environment)
        manager.ls()
