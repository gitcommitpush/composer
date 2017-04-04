from core.cli import BaseCommandLine
from modules.apps.managers import AppManager
from modules.compose.managers import ComposeManager


class Compose(BaseCommandLine):
    def _get_manager(self, app):
        return ComposeManager(AppManager(app))

    def up(self, app, environment='default'):
        manager = self._get_manager(app)
        manager.up()

    def down(self, app, environment='default'):
        manager = self._get_manager(app)
        manager.down()
