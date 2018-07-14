import errno
from os import path, makedirs

from pycallgraph import PyCallGraph, Config, GlobbingFilter
from pycallgraph.output import GraphvizOutput

from providers import CallgraphProviderBase, CallgraphConfiguration


def get_new_pygraphviz_instance(configuration: CallgraphConfiguration, caller_name: str = None):
    return PyCallgraphProvider(configuration=configuration, caller_name=caller_name)


class PyCallgraphProvider(CallgraphProviderBase):
    def __init__(self, configuration: CallgraphConfiguration, caller_name: str = None):
        super().__init__(configuration, caller_name)
        self._config = Config()
        self._config.trace_filter = GlobbingFilter(exclude=[
            'pycallgraph.*'
            'excallgraph.*'
        ])
        if self._configuration.excludes is not None:
            self._config.trace_filter.exclude += self._configuration.excludes
        if self._configuration.includes is not None:
            self._config.trace_filter.include = self._configuration.includes

    def __enter__(self):
        self._provider = PyCallGraph(
            output=GraphvizOutput(output_file=path.join(self._path, f"{self._caller_name}.{self._configuration.format}"),
                                  output_format=self._configuration.format), config=self._config)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._provider is not None:
            return self._provider.__exit__(exc_type, exc_val, exc_tb)

    def start(self):
        '''Starts Capturing Trace'''
        return self._provider.start()

    def stop(self):
        '''Stop Capture Trace'''
        return self._provider.stop()

    def get_path(self):
        return self._configuration.path

    def get_format(self):
        return self._configuration.format

    def create_path_if_not_exists(self):
        try:
            makedirs(self.get_path())
        except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(self.get_path()):
                pass
            else:
                raise

