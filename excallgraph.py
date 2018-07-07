import errno
import os
from os import path

from pycallgraph import PyCallGraph, Config, GlobbingFilter
from pycallgraph.output import GraphvizOutput

_CALL_GRAPHS_FORMAT="png"
_CALL_GRAPHS_GENERATE = True
_CALL_GRAPHS_PATH_EXISTS = False

_CALL_GRAPH_CONFIG = Config()
_CALL_GRAPH_CONFIG.trace_filter = GlobbingFilter(exclude=[
    'pycallgraph.*'
])

def set_call_graph_format(format):
    """Set the Call graph export format."""
    global _CALL_GRAPHS_FORMAT
    if format not in ["png", "svg"]:
        raise Exception(f"{format} is not supported.")
    _CALL_GRAPHS_FORMAT = format

def set_call_graph_path(call_graph_path):
    global _CALL_GRAPHS_PATH
    _CALL_GRAPHS_PATH = call_graph_path
    if not os.path.isdir(call_graph_path):
        _create_call_graph_path()

def disable_call_graph_generation():
    global _CALL_GRAPHS_GENERATE
    _CALL_GRAPHS_GENERATE = False

def enable_call_graph_generation():
    global _CALL_GRAPHS_GENERATE
    _CALL_GRAPHS_GENERATE = True

def _create_call_graph_path():
    """Create Call Graph Path if it does not exists"""
    global _CALL_GRAPHS_PATH_EXISTS
    if not _CALL_GRAPHS_PATH_EXISTS:
        # Create Call diagrams folder
        try:
            os.makedirs(_CALL_GRAPHS_PATH)
        except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(_CALL_GRAPHS_PATH):
                pass
            else:
                raise
    _CALL_GRAPHS_PATH_EXISTS = True

def call_graph_ignore(*args):
    """Adds Module or classes to ignored list"""
    global _CALL_GRAPH_CONFIG
    for exclude in args:
        if exclude not in _CALL_GRAPH_CONFIG.trace_filter.exclude:
            _CALL_GRAPH_CONFIG.trace_filter.exclude.append(exclude)

def generate_call_graph(func):
    """Generates Call Graph for the called function"""
    def wrapper(s, *args, **kwargs):
        if _CALL_GRAPHS_GENERATE:
            caller_func = func.__name__
            if len(args) > 1:
                caller_func += "_" + "_".join(args[1:])
            if not _CALL_GRAPHS_PATH_EXISTS:
                _create_call_graph_path()
            with PyCallGraph(output=GraphvizOutput(output_file=path.join(_CALL_GRAPHS_PATH, f"{caller_func}.{_CALL_GRAPHS_FORMAT}"),
                                                   output_format=_CALL_GRAPHS_FORMAT), config=_CALL_GRAPH_CONFIG):
                return func(s, *args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper