from os import path
from typing import Callable

from providers import CallgraphConfiguration

_provider_factory = None
_provider_configuration = None


def initialize_callgraph(provider_factory: Callable, configuration: CallgraphConfiguration):
    global _provider_factory
    global _provider_configuration
    _provider_factory = provider_factory
    _provider_configuration = configuration


def generate_call_graph(func):
    """Generates Call Graph for the called function"""
    def wrapper(s, *args, **kwargs):
        if _provider_configuration.enabled:
            caller_func = func.__name__
            if len(args) > 1:
                caller_func += "_" + "_".join(args[1:])
            with _provider_factory(_provider_configuration, caller_func) as p:
                return func(s, *args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper
