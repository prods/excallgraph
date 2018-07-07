import os
from unittest import TestCase

from excallgraph import generate_call_graph, set_call_graph_format, set_call_graph_path

def get_execution_path():
    root = os.path.dirname(os.path.realpath(__file__))
    if "SRC_ROOT" in os.environ:
        root = os.path.join(os.path.abspath(os.environ['SRC_ROOT']), "tests")
    return root

def get_call_graphs_path():
    return get_execution_path_child("calls")

def get_execution_path_child(child):
    return os.path.join(get_execution_path(), child)

def check_call_graph_file_exists(call_graph_file_name):
    return os.path.isfile(os.path.join(get_call_graphs_path(), call_graph_file_name))

class ExCallGraphTestScenarios(object):
    def __init__(self):
        set_call_graph_format("png")
        set_call_graph_path(get_call_graphs_path())

    @generate_call_graph
    def test_fibonancy(self, max):
        a, b = 0,1
        while b <= max:
            yield a
            a,b = b, a+b

class ExCallGraphTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scenarios = ExCallGraphTestScenarios()

    def test_simple_call_graph_generation(self):
        result = self._scenarios.test_fibonancy(10000)
        self.assertTrue(check_call_graph_file_exists("test_simple_call_graph_generation"))
