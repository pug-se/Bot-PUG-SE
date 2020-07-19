import os

from utils.command_base import CommandBase

PATH_MODULES = {}

command_list = None

def get_commands():
    global command_list
    if command_list is None:
        modules = get_modules_by_path(get_commands_path())
        command_list = get_commands_by_modules(modules)
    return command_list

def get_commands_path():
    root_directory = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    commands_path = os.path.join(root_directory, 'commands')
    return commands_path

def get_commands_by_modules(modules):
    command_list = []
    for module in modules:
        for attr_str in dir(module):
            attr = getattr(module, attr_str)
            if not isinstance(attr, type) or attr == CommandBase:
                continue
            if issubclass(attr, CommandBase):
                command_list.append(attr())
    return command_list

def get_modules_by_path(path):
    if path not in PATH_MODULES:
        modules_names = get_modules_names(path)
        package_name = get_package_name(path)
        PATH_MODULES[path] = get_modules_by_names(modules_names, package_name)
    return PATH_MODULES[path]

def get_modules_by_names(modules_names, package_name):
    modules = []
    for module_name in modules_names:
        modules.append(
            __import__(
                '{}.{}'.format(package_name, module_name),
                fromlist=[module_name],
            )
        )
    return modules

def get_modules_names(path):
    modules_names = []
    for module_filename in os.listdir(path):
        if '__' not in module_filename:
            modules_names.append(module_filename.replace('.py', ''))
    return modules_names

def get_package_name(path):
    package_name = None
    package_path = path

    while os.path.exists(os.path.join(package_path, '__init__.py')):
        current_package_name = os.path.basename(package_path)
        package_path = os.path.dirname(package_path)

        if package_name is None:
            package_name = current_package_name
        else:
            package_name = '{}.{}'.format(current_package_name, package_name)

    if package_name is None:
        raise ValueError('You must set a "path" that is a python package.')

    return package_name
