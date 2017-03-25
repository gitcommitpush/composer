from app import settings
from app.logging import Logger
from modules.app.utils import get_path, app_exists
import os
import shutil
import subprocess


class App(object):
    def create(self, name, repo, branch='master'):
        if not app_exists(name):
            path = get_path(name)
            try:
                os.mkdir(path)
                os.chdir(path)
                subprocess.call('git clone {} .'.format(repo), shell=True)
                subprocess.call('git checkout {}'.format(branch), shell=True)
            except:
                shutil.rmtree(path)
                raise Exception('Failed to create app.')

            Logger.info('App "{}" successfully created.'.format(name))
        else:
            raise Exception('App "{}" already exists.'.format(name))

    def delete(self, name):
        if app_exists(name, raise_exception=True):
            path = get_path(name)
            shutil.rmtree(path)
            Logger.info('App "{}" successfully deleted.'.format(name))

    def ls(self):
        Logger.header('Apps')

        dirs = os.listdir(settings.COMPOSER_DATA_DIR)
        for dir in dirs:
            path = get_path(dir)
            if os.path.isdir(path):
                Logger.info(dir)

    def update(self, name, branch=None):
        """
        Update from the associated git repo
        """
        if app_exists(name, raise_exception=True):
            path = get_path(name)
            os.chdir(path)
            if branch:
                subprocess.call('git pull origin {}'.format(branch), shell=True)
            else:
                subprocess.call('git pull', shell=True)
