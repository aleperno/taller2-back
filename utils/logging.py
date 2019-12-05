from api.admin_resources import app


class MyLogger(object):
    @classmethod
    def info(cls, *args, **kwargs):
        app.logger.info(*args, **kwargs)

    @classmethod
    def warning(cls, *args, **kwargs):
        app.logger.warning(*args, **kwargs)

    @classmethod
    def error(cls, *args, **kwargs):
        app.logger.info(*args, **kwargs)

    @classmethod
    def debug(cls, *args, **kwargs):
        app.logger.debug(*args, **kwargs)