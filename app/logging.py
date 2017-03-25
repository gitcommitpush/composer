

class Logger(object):
    @staticmethod
    def header(text):
        lines = '-'*30
        print('{lines}\n{text}\n{lines}'.format(text=text, lines=lines))

    @staticmethod
    def info(text):
        """
        May be more useful in future
        """
        print(text)
