from core.cli import BaseCommandLine
from modules.environment.managers import EnvironmentManager
from modules.apps.managers import AppConfigManager, AppManager
from modules.compose.managers import ComposeManager


class Compose(BaseCommandLine):
    def _get_manager(self, app, environment):
        environment_manager = EnvironmentManager(AppConfigManager(AppManager(app)), environment)
        return ComposeManager(environment_manager)

    def up(self, app, environment='default'):
        manager = self._get_manager(app, environment)
        manager.up()

    def down(self, app, environment='default'):
        manager = self._get_manager(app, environment)
        manager.down()
