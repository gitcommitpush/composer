from core import settings
from core.managers import BaseManager
import shutil
import os
import json
import subprocess


class AppManager(BaseManager):
    DATA_DIR = 'app-data'
    CONFIG_NAME = 'compose.json'
    PROXY_CONFIG_EXTENSION = '.conf'
    DEFAULT_PROXY_CONFIG_TEMPLATE = '''
server {{
    listen 80;
    server_name {hostname};

    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_pass_request_headers on;
    }}
}}
'''

    def __init__(self, app):
        self.app_name = app
        self.app = self  # Should always be an AppManager instance
        self.config = self._get_config()
        super().__init__()

    def get_name(self):
        # Get app name
        return self.app_name

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

    def get_proxy_config_path(self):
        # Get proxy config location
        return os.path.join(settings.PROXY_CONFIG_LOCATION, self.get_name() + self.PROXY_CONFIG_EXTENSION)

    def get_proxy_template(self):
        # Get proxy template to use for proxy config file
        try:
            template = open(self.config.get('proxy_config_template', 'r')).read()
        except:
            template = self.DEFAULT_PROXY_CONFIG_TEMPLATE

        return template


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

        try:
            subprocess.check_output(['touch', self.get_config_path()], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            self.logger.fail('Could not create config file', extra=error.output)

        self.logger.info('Created successfully.')

    def delete(self):
        # Delete an app
        self.should_exist()

        try:
            subprocess.check_output(['rm', '-r', self.get_path()], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            self.logger.fail('Could not delete app', extra=error.output)

        self.logger.info('Deleted successfully.')

    def change_branch(self, branch):
        # Change Git branch
        self.should_exist()
        self.should_not_be_empty()

        try:
            subprocess.check_output(['git', 'checkout', branch], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            self.logger.fail('Error with Git repository', extra=error.output)

        self.logger.info('Switched to branch {}'.format(branch))

    def fetch(self, repo, branch='master'):
        # Clone Git repo
        self.should_exist()
        self.should_be_empty()

        try:
            os.chdir(self.get_data_path())
            subprocess.check_output(['git', 'clone', repo, '.'], stderr=subprocess.STDOUT)
            self.change_branch(branch)
        except subprocess.CalledProcessError as error:
            self.logger.fail('Error with Git repository', extra=error.output)

        self.logger.info('Successfully cloned from repository.')

    def change_repo(self, *args):
        # Change Git repo
        self.should_exist()

        shutil.rmtree(self.get_data_path())
        os.mkdir(self.get_data_path())

        self.fetch(*args)

    def _get_config(self):
        # Get config from app
        config = open(self.app.get_config_path(), 'r').read()
        return json.loads(config if len(config) else '{}')

    def save_config(self):
        # Save config dict to app config file
        open(self.app.get_config_path(), 'w').write(json.dumps(self.config))
        self.logger.info('Configuration saved.')
