from core.settings import DATA_DIR
from datetime import datetime
import os


LOG_DIR = os.path.join(DATA_DIR, 'log')


class Logger(object):
    def __init__(self, prefix='', log='log.txt'):
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)

        self.prefix = prefix
        self.log = open(os.path.join(LOG_DIR, log), 'a+')

    def write(self, tag, msg, silent, raise_exception=False):
        formatted_msg = '[{tag}] {prefix} {msg}\n'.format(
            prefix=self.prefix,
            tag=tag,
            msg=msg
        )
        self.log.write('[{}]{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), formatted_msg))

        if not silent and not raise_exception:
            print(formatted_msg)

        if raise_exception:
            raise SystemExit(formatted_msg)

    def info(self, msg, silent=False):
        self.write('INFO', msg, silent)

    def warn(self, msg, silent=False):
        self.write('WARN', msg, silent)

    def fail(self, msg, raise_exception=True, silent=False):
        self.write('FAIL', msg, silent, raise_exception)

