from core.cli import BaseCommandLine
from modules.apps.managers import AppManager


class App(BaseCommandLine):
    def _get_manager(self, app):
        return AppManager(app=app)

    def create(self, app):
        manager = self._get_manager(app)
        manager.create()

    def delete(self, app):
        manager = self._get_manager(app)
        manager.delete()

    def fetch(self, app, repo, branch='master'):
        manager = self._get_manager(app)
        manager.fetch(repo)

    def change_repo(self, app, repo, branch='master'):
        manager = self._get_manager(app)
        manager.change_repo(repo)

    def change_branch(self, app, branch):
        manager = self._get_manager(app)
        manager.change_branch(branch)

    def __str__(self):
        return 'Apps'
