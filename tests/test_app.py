from modules.apps import AppConfigManager, AppManager
from core import settings
import unittest
import os
import shutil


class AppManagerTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.manager = AppManager(app='composer-app')

        os.mkdir('/tmp/composer')
        settings.APP_DIR = '/tmp/composer/apps'
        os.mkdir(settings.APP_DIR)

    def test_create(self):
        apps_before_create = os.listdir(settings.APP_DIR)
        self.assertEqual(len(apps_before_create), 0)

        self.manager.create()
        apps_after_create = os.listdir(settings.APP_DIR)
        self.assertEqual(len(apps_after_create), 1)

        app_contents = os.listdir(os.path.join(settings.APP_DIR, 'composer-app'))
        self.assertTrue('compose.json' in app_contents)

        with self.assertRaises(Exception):
            self.manager.create()

    def test_delete(self):
        self.manager.create()

        apps_before_delete = os.listdir(settings.APP_DIR)
        self.assertEqual(len(apps_before_delete), 1)

        self.manager.delete()

        apps_after_delete = os.listdir(settings.APP_DIR)
        self.assertEqual(len(apps_after_delete), 0)

        with self.assertRaises(Exception):
            self.manager.delete()

    def test_app_expect_methods(self):
        with self.assertRaises(Exception):
            self.manager.expect_exists()

        self.manager.create()

        with self.assertRaises(Exception):
            self.manager.expect_not_exists()

    def tearDown(self):
        super().tearDown()
        shutil.rmtree('/tmp/composer')
