# rfpython: run python function

A simple tool to run (or debug) a python function inside a python script from the command line.

![](rf_python_usage.gif)

### Usage

``` 
rfpython python-file function-name
``` 

### Using VSCode Debugger:

``` 
rfpython python-file function-name --debugger
``` 

With a remote attach configuration:


```
    {
        "name": "Python: Remote Attach",
        "type": "python",
        "request": "attach",
        "port": 5678,
        "host": "localhost",
        "pathMappings": [
            {
                "localRoot": "${workspaceFolder}",
                "remoteRoot": "."
            }
        ]
    }
```

### Installation

rfpython is [available from the Python Package
Index](https://pypi.org/project/rfpython/), so simply do
```
pip install rfpython
```
to install.

### Testing

To run the rfpython unit tests, check out this repository and type
```
pytest
```

### License

rfpython is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
