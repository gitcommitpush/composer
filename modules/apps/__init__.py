from core import settings
import configparser
import subprocess
import shutil
import os
import json


class AppManager(object):
    CONFIG_NAME = 'app.json'

    def __init__(self, app, expect_exists=False):
        self.app = app

    def expect_not_exists(self):
        """
        Assert that an app doesn't exist.
        """
        if self.app_exists():
            raise Exception('App "{}" already exists.'.format(self.app))

    def expect_exists(self):
        """
        Assert that an app does exist.
        """
        if not self.app_exists():
            raise Exception('App "{}" does not exist.'.format(self.app))

    def delete(self):
        """
        Delete an app.
        """
        self.expect_exists()
        shutil.rmtree(self.get_path())
        print('App "{}" successfully deleted.'.format(self.app))

    def create(self, repo=None, branch='master'):
        """
        Create an app.
        """
        self.expect_not_exists()

        os.mkdir(self.get_path())
        if repo:
            self.clone_from_repo(repo, branch)
            print('App "{}" successfully created from Git repo {}'.format(self.app, repo))
        else:
            print('Empty app "{}" successfully created.')

        open(os.path.join(self.get_path(), self.CONFIG_NAME), 'w+').write(json.dumps({}))  # Create empty config file

    def clone_from_repo(self, repo, branch='master'):
        """
        Get the repo from the git repository
        """
        self.expect_exists()

        os.chdir(self.get_path())
        subprocess.call('git clone {} ./app-data'.format(repo), shell=True)
        subprocess.call('git checkout {}'.format(branch), shell=True)

    def get_data_path(self):
        return os.path.join(self.get_path(), 'app-data')

    def get_config_path(self):
        path = os.path.join(self.get_data_path(), self.CONFIG_NAME)
        if not os.path.exists(path):
            return os.path.join(self.get_path(), self.CONFIG_NAME)
        return path

    def get_path(self):
        """
        Get the directory path of an app.
        """
        return os.path.join(settings.APP_DIR, self.app)

    def app_exists(self):
        """
        Check if an app exists.
        """
        return os.path.exists(self.get_path())


class AppConfigManager(object):
    def __init__(self, app_manager):
        if not isinstance(app_manager, AppManager):
            raise Exception('AppConfigManager requires an AppManager instance.')

        app_manager.expect_exists()

        self.app = app_manager
        self.path = self.app.get_config_path()

        if not os.path.exists(self.path):
            raise Exception('App "{}" does not have a config file.'.format(self.app))

        self.config = self.get_config()

    def get_config(self):
        """
        Get an app config as a Python dictionary.
        """
        config = open(self.path, 'r')
        return json.loads(config.read())

    def save(self):
        """
        Save a Python dictionary to an app's config
        """
        config = open(self.path, 'w').write(json.dumps(self.config))
        return config

    def set(self, key, value, auto_save=False):
        """
        Programatically set a config value.
        """
        self.config[key] = value
        if auto_save:
            self.save()
