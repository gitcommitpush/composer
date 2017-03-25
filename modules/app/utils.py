import os
from app import settings
from app.logging import Logger


def get_path(app):
    return os.path.join(settings.COMPOSER_DATA_DIR, app)


def app_exists(app, raise_exception=False):
    path = get_path(app)
    if not os.path.exists(path):
        if raise_exception:
            raise Exception('App "{}" does not exist.'.format(app))
        return False
    else:
        return True
