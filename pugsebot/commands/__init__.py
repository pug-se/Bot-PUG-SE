from utils.command_base import CommandBase

import os

def get_module_names():
    path = os.path.dirname(os.path.abspath(__file__))
    modules_names = []
    for module_filename in os.listdir(path):
        if module_filename != '__init__.py'\
                and '.py' in module_filename:
            modules_names.append(
                module_filename.replace('.py', ''))
    return modules_names

def get_modules(modules_names):
    modules = []
    for module_name in modules_names:
        modules.append(
            __import__(
                'commands.' + module_name,
                fromlist=[module_name]))
    return modules

def get_commands(modules):
    command_list = []
    for module in modules:
        for attr_str in dir(module):
            attr = getattr(module, attr_str)
            if not isinstance(attr, type) or attr == CommandBase:
                continue
            if issubclass(attr, CommandBase):
                command_list.append(attr())
    return command_list

_modules_names = get_module_names()
_modules = get_modules(_modules_names)

command_list = get_commands(_modules)
