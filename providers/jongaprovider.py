import errno
from os import path, makedirs

import jonga

from providers import CallgraphProviderBase, CallgraphConfiguration


def get_new_jonga_instance(configuration: CallgraphConfiguration, caller_name: str = None):
    return JongaProvider(configuration=configuration, caller_name=caller_name)


class JongaProvider(CallgraphProviderBase):
    def __init__(self, configuration: CallgraphConfiguration, caller_name: str = None):
        super().__init__(configuration, caller_name)
        includes_filter = caller_name
        if configuration.includes is not None and len(configuration.includes) > 0:
            includes_filter = "|".join(configuration.includes)
        self._provider = jonga.CallTracer(grpflt=includes_filter)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._provider is not None:
            self._provider.stop()
            self._provider.graph(path.join(self.get_path(), f"{self._caller_name}.{self.get_format()}"))

    def get_path(self):
        return self._configuration.path

    def get_format(self):
        return self._configuration.format

    def start(self):
        '''Starts Capturing Trace'''
        return self._provider.start()

    def stop(self):
        '''Stop Capture Trace'''
        return self._provider.stop()

    def create_path_if_not_exists(self):
        try:
            makedirs(self.get_path())
        except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(self.get_path()):
                pass
            else:
                raise

