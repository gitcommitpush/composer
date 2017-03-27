from core.logging import Logger


class BaseManager(object):
    app = None

    def __init__(self):
        self.logger = Logger(prefix='{}:'.format(self.app) if self.app else '')
