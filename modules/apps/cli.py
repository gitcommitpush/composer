from modules.apps import AppManager, AppConfigManager


class App(object):
    def create(self, app_name, repo, branch='master'):
        app = AppManager(app_name)
        app.create(repo, branch)

    def delete(self, app_name):
        app = AppManager(app_name)
        app.delete()

    def update(self, app_name):
        app = AppManager(app_name)
        app.update()

    def __str__(self):
        return 'Apps'
