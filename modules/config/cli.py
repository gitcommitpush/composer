from core.cli import BaseCommandLine
from modules.apps.managers import AppManager


class Config(BaseCommandLine):
    def _get_manager(self, app):
        return AppManager(app)

    def set_hostname(self, app, hostname):
        manager = self._get_manager(app)
        manager.config['hostname'] = hostname
        manager.save_config()

    def __str__(self):
        return 'Config'
