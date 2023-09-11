# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Pete Ezzo

import importlib
import urllib


class ModuleLoader:
    """
    Retrieve a remote python file and load it as a module

    Usage:

        main = ModuleLoader('http://localhost:8080/main.py', 'main')

    """
    def __init__(self, uri: str, name: str):
        data = urllib.request.urlopen(uri).read()
        codeobj = compile(data, uri, 'exec')
        module = importlib.util.module_from_spec(name)
        exec (codeobj, module.__dict__)
        return module
