from utils.command_base import CommandBase

import os
_path = os.path.dirname(os.path.abspath(__file__))
_modules = os.listdir(_path)

_modules = [
    mod for mod in _modules if '.py' in mod and mod != "__init__.py"
]
_modules = [mod.replace('.py', '') for mod in _modules]

# import commands
_modules_aux = _modules
_modules = []
for _module in _modules_aux:
    _modules.append(
        __import__(
            'commands.' + _module,
            fromlist=[_module]))

# create command instances
command_list = []

for _module in _modules:
    for _attr_str in dir(_module):
        _attr = getattr(_module, _attr_str)
        if not isinstance(_attr, type) \
            or _attr == CommandBase: continue
        if issubclass(_attr, CommandBase):
            command_list.append(_attr())
