import errno
import os
import sys


class CallgraphConfiguration(object):
    def __init__(self):
        self.format = None
        self.path = os.path.dirname(sys.argv[0])
        self.includes = None
        self.excludes = None
        self.enabled = True


class CallgraphProviderBase(object):
    def __init__(self, configuration: CallgraphConfiguration, caller_name: str = None):
        self._configuration = configuration
        self._path = configuration.path
        self._caller_name = caller_name
        self._create_path_if_not_exists()

    def __enter__(self):
        raise NotImplemented()

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplemented()

    def get_path(self):
        return self._configuration.path

    def get_format(self):
        return self._configuration.format

    def is_enabled(self):
        return self._configuration.enabled

    def _create_path_if_not_exists(self):
        try:
            os.makedirs(self.get_path())
        except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(self.get_path()):
                pass
            else:
                raise