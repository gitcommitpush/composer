import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
APP_DIR = os.path.join(DATA_DIR, 'apps')

BASE_DOMAIN = 'example.com'
NGINX_CONFIG_LOCATION = os.path.join(BASE_DIR, 'data')  # Temporary
