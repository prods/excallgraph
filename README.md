## Extended Call Graph Generator (ExCallGraph)

*Excallgraph* is an abstraction layer over call graph generation libraries like [pycallgraph](https://pycallgraph.readthedocs.io/en/master/) and [jonga](https://github.com/bwohlberg/jonga). Its premise is to make call graph generation libraries interchangeable under a standard API that should be as simple as possible.

### Installation
```bash
pip install excallgraph
```

### Usage
The example below makes use of the `pycallgraph` provider.

```python
import os
import re
from unittest import TestCase

from excallgraph import generate_call_graph, initialize_callgraph
from providers import CallgraphConfiguration
from providers.pycallgraphprovider import get_new_pygraphviz_instance

class ExCallGraphTestScenarios(object):
    def __init__(self):
        call_graphs_path = os.path.dirname(os.path.realpath(__file__))
        if "SRC_ROOT" in os.environ:
            call_graphs_path = os.path.join(os.path.abspath(os.environ['SRC_ROOT']), "tests", "calls")
    
        config = CallgraphConfiguration()
        config.format = "png"
        config.path = call_graphs_path
        config.enabled = True
        config.excludes = ['json']
        initialize_callgraph(get_new_pygraphviz_instance, config)


    @generate_call_graph
    def test_regex_finditer(self):
        return [m.start() for m in re.finditer('test', 'test test test test')]
```

### API

CallgraphConfiguration (*Class*)
----
An instance of this class is required in order to store the required configuration for the call graph generation. Inertly, each instantiated provider will transform it into its own specific configuration settings.

#####format
Expected call graph image/vector format. Specific format support is controlled by the underlying provider and only one format per instance is supported at the moment.
Example: `png`, `jpeg`, `svg`, etc...
```python
config.format = "png"
```


#####path
Path where the call graphs will be saved. Defaults to the path of the executing python script.
```python
config.path = "/home/me/projects/testproject/calls"
```


#####includes

List of packages, modules or classes to include in graph call traces. Not required for most providers. It supports basic regex depending on the selected provider.

```python
config.includes = ['re.*', 'orders.*']
```


#####excludes

List of packages, modules or classes to exclude from the call graph traces. It supports basic regex depending on the selected provider.

```python
config.excludes = [ 're.*', 'json' ]
```


#####enabled
Controls if call graphs will be generated or not. Defaults to `True`.

```python
config.enabled = True
```


get_new_*_instance
----
This factory function creates an instance of a specific call graph generation provider library. These libraries and factory functions can be found under the `providers` package.
At the moment only `pycallgraph` and `jonga` are supported.

| Library |Provider module         | Factory Function  |
|---------|------------------------|-------------------|
| [pycallgraph](https://pycallgraph.readthedocs.io/en/master/) |  [providers.pycallgraphprovider](https://github.com/prods/excallgraph/blob/master/providers/pycallgraphprovider.py) | [get_new_pygraphviz_instance](https://github.com/prods/excallgraph/blob/fbde766b956741b3c4232f655eb5381912b797d0/providers/pycallgraphprovider.py#L10) |
| [jonga](https://github.com/bwohlberg/jonga) |  [providers.jongaprovider](https://github.com/prods/excallgraph/blob/master/providers/jongaprovider.py) | [get_new_jonga_instance](https://github.com/prods/excallgraph/blob/fbde766b956741b3c4232f655eb5381912b797d0/providers/jongaprovider.py#L9) |


initialize_callgraph(*factory_function*, *configuration*)
----
This function initializes the call graph provider using the specified configuration instance.

```python
initialize_callgraph(get_new_pygraphviz_instance, config)
```

generate_call_graph (*Decorator*)
----
This decorator controls which function will be traced for call graph generation. 

```python
@generate_call_graph
def test_regex_finditer(self):
    return [m.start() for m in re.finditer('test', 'test test test test')]
```

Call graph will only be generated if the configuration `enabled` property is set to `True`.

####TODO
1. Bug fixes
2. Support more call graph generation libraries as needed or requested.