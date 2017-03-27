from core import settings
from core.managers import BaseManager
import subprocess
import shutil
import os
import json
import sh


class AppManager(BaseManager):
    DATA_DIR = 'app-data'
    CONFIG_NAME = 'compose.json'

    def __init__(self, app):
        self.app = app
        super().__init__()

    def get_name(self):
        # Get app name
        return self.app

    def get_path(self):
        # Get app path
        return os.path.join(settings.APP_DIR, self.get_name())

    def get_data_path(self):
        # Get app data path
        return os.path.join(self.get_path(), self.DATA_DIR)

    def get_config_path(self):
        # Get config file - use repo config or fallback on local config
        repo_config = os.path.join(self.get_data_path(), self.CONFIG_NAME)
        return repo_config if os.path.exists(repo_config) else os.path.join(self.get_path(), self.CONFIG_NAME)

    def should_exist(self):
        # Expect that app exists
        if not os.path.exists(self.get_path()):
            self.logger.fail('Does not exist.')

    def should_not_exist(self):
        # Expect that app does not exist
        if os.path.exists(self.get_path()):
            self.logger.fail('Already exists.')

    def should_be_empty(self):
        # Expect app is empty
        if len(os.listdir(self.get_data_path())):
            self.logger.fail('App is not empty.')

    def should_not_be_empty(self):
        # Expect app is not empty
        if not len(os.listdir(self.get_data_path())):
            self.logger.fail('App is empty.')

    def create(self):
        # Create an app
        self.should_not_exist()

        os.mkdir(self.get_path())
        os.mkdir(self.get_data_path())

        config_path = self.get_config_path()
        if not os.path.exists(config_path):
            sh.touch(self.get_config_path())

        self.logger.info('Created successfully.')

    def delete(self):
        # Delete an app
        self.should_exist()

        sh.rm('-rf', self.get_path())

        self.logger.info('Deleted successfully.')

    def change_branch(self, branch):
        # Change Git branch
        self.should_exist()
        self.should_not_be_empty()

        try:
            sh.git('checkout', branch)
            self.logger.info('Switched to branch {}'.format(branch))
        except sh.ErrorReturnCode as e:
            self.logger.fail('Error with Git repository: \n\n{}'.format(e))

    def clone(self, repo, branch='master'):
        # Clone Git repo
        self.should_exist()
        self.should_be_empty()

        try:
            os.chdir(self.get_data_path())
            sh.git('clone', repo, '.')
            self.logger.info('Successfully cloned from repository.')
            self.change_branch(branch)
        except sh.ErrorReturnCode as e:
            self.logger.fail('Error with Git repository: \n\n{}'.format(e))

    def change_repo(self, *args):
        # Change Git repo
        self.should_exist()

        shutil.rmtree(self.get_data_path())
        os.mkdir(self.get_data_path())

        self.clone(*args)
