import json
import re
from unittest import TestCase


from excallgraph import generate_call_graph, initialize_callgraph
from providers import CallgraphConfiguration
from providers.pycallgraphprovider import get_new_pygraphviz_instance
from tests import get_call_graphs_path, check_call_graph_file_exists


class ExCallGraphTestScenarios(object):
    def __init__(self):
        config = CallgraphConfiguration()
        config.format = "png"
        config.path = get_call_graphs_path()
        config.enabled = True
        initialize_callgraph(get_new_pygraphviz_instance, config)


    @generate_call_graph
    def test_simple_call_graph_generation_using_pycallgraph(self):
        return [m.start() for m in re.finditer('test', 'test test test test')]

    @generate_call_graph
    def test_simple_call_graph_generation1_using_pycallgraph(self):
        value = []
        for v in range(0, 100):
            value.append({
                "test1": [m.start() for m in re.finditer('test', 'test test test test')]
            })
        return json.dumps({
            "test": value
        })

    @generate_call_graph
    def test_simple_call_graph_generation2_using_pycallgraph(self):
        value = []
        for v in range(0, 100):
            value.append({
                "test1": [m.start() for m in re.finditer('test', 'test test test test')]
            })
        return json.dumps({
            "test": value
        })


# class ExCallGraphPyCallGraphTests(TestCase):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._scenarios = ExCallGraphTestScenarios()
#
#
#     def test_simple_call_graph_generation_using_pycallgraph(self):
#         self._scenarios.test_simple_call_graph_generation_using_pycallgraph()
#         self.assertTrue(check_call_graph_file_exists("test_simple_call_graph_generation_using_pycallgraph.png"))
#
#
#     def test_simple_call_graph_generation1_using_pycallgraph(self):
#         self._scenarios.test_simple_call_graph_generation1_using_pycallgraph()
#         self.assertTrue(check_call_graph_file_exists("test_simple_call_graph_generation1_using_pycallgraph.png"))
#
#
#     def test_simple_call_graph_generation2_using_pycallgraph(self):
#         self._scenarios.test_simple_call_graph_generation2_using_pycallgraph()
#         self.assertTrue(check_call_graph_file_exists("test_simple_call_graph_generation2_using_pycallgraph.png"))
