import inspect
import threading
from typing import Callable
from providers import CallgraphConfiguration

_provider_factory = {}
_provider_configuration = {}


def initialize_callgraph(provider_factory: Callable, configuration: CallgraphConfiguration):
    global _provider_factory
    global _provider_configuration
    with threading.Lock():
        mod = inspect.getmodule(inspect.stack()[1][0])
        _provider_factory[mod] = provider_factory
        _provider_configuration[mod] = configuration


def generate_call_graph(func):
    """Generates Call Graph for the called function"""
    def wrapper(*args, **kwargs):
        # Get Calling Module
        mod = inspect.getmodule(inspect.stack()[1][0])
        if _provider_configuration[mod].enabled:
            caller_func = func.__name__
            if len(args) > 1:
                caller_func += "_" + "_".join(args[1:])
            # Get Factory and Configuration
            factory = _provider_factory[mod]
            config = _provider_configuration[mod]
            # Generate Call Graph
            with factory(config, caller_func) as p:
                p.start()
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper
