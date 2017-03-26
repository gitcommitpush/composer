from modules.apps import AppManager, AppConfigManager
from modules.compose import ComposeManager


class Compose(object):
    def up(self, app_name):
        manager = ComposeManager(AppConfigManager(AppManager(app_name)))
        manager.up()

    def down(self, app_name):
        manager = ComposeManager(AppConfigManager(AppManager(app_name)))
        manager.down()
