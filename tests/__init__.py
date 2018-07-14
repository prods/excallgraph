import os


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
