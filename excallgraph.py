from os import path
from typing import Callable
import inspect
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
    def wrapper(*args, **kwargs):
        if _provider_configuration.enabled:
            caller_func = func.__name__
            if len(args) > 1:
                caller_func += "_" + "_".join(args[1:])
            with _provider_factory(_provider_configuration, caller_func) as p:
                fn_parameters = [p for p in inspect.signature(func).parameters if p != 'self']
                if "_callgraph_" in fn_parameters:
                    if kwargs is None:
                        kwargs = {}
                    kwargs["_callgraph_"] = p
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper
