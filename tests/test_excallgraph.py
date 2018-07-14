import os
import json
from unittest import TestCase


from excallgraph import generate_call_graph, initialize_callgraph
from providers import CallgraphConfiguration
from providers.pycallgraphprovider import get_new_pygraphviz_instance
#from providers.jongaprovider import get_new_jonga_instance


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
        config = CallgraphConfiguration()
        config.format = "png"
        config.path = get_call_graphs_path()
        config.enabled = True
        #config.excludes = ['json']
        initialize_callgraph(get_new_pygraphviz_instance, config)
        #initialize_callgraph(get_new_jonga_instance, config)

    def test_fibonancy(self, max):
        a, b = 0,1
        print(max)
        while b <= max:
            yield a
            a,b = b, a+b


    @generate_call_graph
    def test_simple_call_graph_generation(self):
        return self.test_fibonancy(10000)

    @generate_call_graph
    def test_simple_call_graph_generation1(self):
        value = []
        for v in range(0, 100000):
            value.append({
                "test1": v
            })
        return json.dumps({
            "test": value
        })

    @generate_call_graph
    def test_simple_call_graph_generation2(self):
        value = []
        for v in range(0, 100000):
            value.append({
                "test1": v
            })
        return json.dumps({
            "test": value
        })


class ExCallGraphTests(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scenarios = ExCallGraphTestScenarios()


    def test_simple_call_graph_generation(self):
        self._scenarios.test_simple_call_graph_generation()
        self.assertTrue(check_call_graph_file_exists("test_simple_call_graph_generation.png"))


    def test_simple_call_graph_generation1(self):
        self._scenarios.test_simple_call_graph_generation1()
        self.assertTrue(check_call_graph_file_exists("test_simple_call_graph_generation1.png"))


    def test_simple_call_graph_generation2(self):
        self._scenarios.test_simple_call_graph_generation2()
        self.assertTrue(check_call_graph_file_exists("test_simple_call_graph_generation2.png"))
