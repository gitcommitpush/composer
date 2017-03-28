from core.cli import BaseCommandLine
from modules.environment.managers import EnvironmentManager
from modules.apps.managers import AppManager, AppConfigManager


class Env(BaseCommandLine):
    def _get_manager(self, app, environment):
        return EnvironmentManager(AppConfigManager(AppManager(app)), env_name=environment)

    def create(self, app, environment):
        manager = self._get_manager(app, environment)
        manager.create()

    def delete(self, app, environment):
        manager = self._get_manager(app, environment)
        manager.delete()

    def set(self, app, environment='default', **kwargs):
        manager = self._get_manager(app, environment)
        manager.set(**kwargs)

    def unset(self, app, env_key, environment='default'):
        manager = self._get_manager(app, environment)
        manager.unset(env_key)

    def ls(self, app):
        manager = self._get_manager(app, 'default')
        manager.ls()
