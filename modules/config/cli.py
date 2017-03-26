from modules.apps import AppManager, AppConfigManager


class Config(object):
    def _get_config_manager(self, app):
        """
        Get the app config manager.
        """
        app = AppManager(app)
        config = AppConfigManager(app)
        return config

    def set_hostname(self, app, hostname):
        """
        Set hostname to route to app (single or comma seperated).
        """
        config = self._get_config_manager(app)
        config.set('hostname', hostname)
        config.save()
        print('App "{}" hostname(s) successfully set to "{}"'.format(app, hostname))

    def set_port(self, app, port=0, use_random=False):
        """
        Set a fixed app port or use a random one.
        """
        config = self._get_config_manager(app)
        config.set('port', port if not use_random else 0)
        config.save()
        print('App "{}" set to use {}.'.format(
            app,
            'a random port' if use_random else 'port {}'.format(port)
        ))

    def __str__(self):
        return 'Config CLI'
