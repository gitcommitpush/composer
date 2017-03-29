from core.managers import BaseManager
from core import settings
from modules.apps.managers import AppConfigManager, AppManager
import os
import sh


NGINX_PROXY_TEMPLATE = '''
server {{
    listen 80;
    server_name {hostname};

    location / {{
        proxy_pass http://localhost:{port};
    }}
}}
'''


class RouterManager(BaseManager):
    def __init__(self, config_manager):
        if not isinstance(config_manager, AppConfigManager):
            raise TypeError('Config manager should be an instance of AppConfigManager.')

        self.config = config_manager.config
        self.app = config_manager.app

        super().__init__()

    def get_hostname(self):
        return self.config.get('hostname', '{}.{}'.format(self.app.get_name(), settings.BASE_DOMAIN))

    def define_route(self, port):
        content = NGINX_PROXY_TEMPLATE.format(
            hostname=self.get_hostname(),
            port=port
        )

        with open(os.path.join(settings.NGINX_CONFIG_LOCATION, '{}.conf'.format(self.app.get_name())), 'w+') as f:
            f.write(content)
            f.close()

        sh.service('nginx', 'restart')
