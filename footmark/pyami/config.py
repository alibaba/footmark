#
import os

try:
    os.path.expanduser('~')
    expanduser = os.path.expanduser
except (AttributeError, ImportError):
    # This is probably running on App Engine.
    expanduser = (lambda x: x)
try:
    import simplejson as json
except ImportError:
    import json

# By default we use two locations for the footmark configurations,
# /etc/footmark/ and ~/.footmark (which works on Windows and Unix).
FootmarkConfigPath = '/etc/footmark/'
FootmarkConfigLocations = [FootmarkConfigPath]
UserConfigPath = os.path.join(expanduser('~'), '.footmark/')
FootmarkConfigLocations.append(UserConfigPath)
FootmarkLoggingConfig = ''
logging_config = '''
[loggers]
keys=root

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=form01

[logger_root]
level=NOTSET
handlers=consoleHandler,fileHandler

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=form01
args=()

[handler_fileHandler]
class=handlers.TimedRotatingFileHandler
level=DEBUG
formatter=form01
args=('footmark.log','D',1,7)

[formatter_form01]
format=%(asctime)s [%(levelname)s] %(filename)s, %(funcName)s[%(lineno)d]: %(message)s
'''

# Default logging configurations.
# By default we use location /var/footmark/ for the footmark logs.
LoggingDict = '/var/log/footmark/'
DefaultLoggingConfig = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] %(filename)s, %(funcName)s[%(lineno)d]: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'level': 'DEBUG',
            'filename': LoggingDict + 'footmark.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 7
        }
    },
    "loggers": {
        'footmark': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}


class Config(object):
    def __init__(self):
        pass

    def init_config(self):
        import platform
        sysstr = platform.system()
        if sysstr == "Linux":
            if not os.path.exists(FootmarkConfigLocations[0]):
                os.makedirs(FootmarkConfigLocations[0])
                FootmarkLoggingConfig = FootmarkConfigLocations[0] + 'logging.conf'
        else:
            os.makedirs(FootmarkConfigLocations[1])
            FootmarkLoggingConfig = FootmarkConfigLocations[1] + 'logging.conf'
        self.add_logging_config(FootmarkLoggingConfig)

        if not os.path.exists(LoggingDict):
            os.makedirs(LoggingDict)

    def add_logging_config(self, config_file):
        file_pb = open(config_file, 'wb')
        file_pb.write(logging_config)
        file_pb.close()
