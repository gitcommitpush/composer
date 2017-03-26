from core import settings
import configparser
import subprocess
import shutil
import os


class AppManager(object):
    CONFIG_NAME = 'app.ini'

    def __init__(self, app, expect_exists=False):
        self.app = app

    def get_config(self):
        path = os.path.join(self.get_path(), self.CONFIG_NAME)
        if not os.path.exists(path):
            raise Exception('App "{}" does not have a config file.'.format(self.app))

        parser = configparser.ConfigParser()
        return parser.read(os.path.join(self.get_path(), self.CONFIG_NAME))

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

        open(os.path.join(self.get_path(), self.CONFIG_NAME), 'w+').close()  # Create empty config file

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
