"""Utilities for importing commands and creating new commands."""

import os

import abc

from .database import Cache, CommandInfo
from .schedule import Schedule


PATH_MODULES = {}

command_list = None


class CommandBase:
    """Base class that needs to be inherited."""

    def __init__(
        self,
        name,
        help_text,
        reply_function_name,
        schedule_interval,
        expire=None,
    ):
        """Set attributes from child classes."""
        self.name = name
        self.help_text = help_text
        self.reply_function_name = reply_function_name
        self.interval = schedule_interval
        self.expire = expire

    def set_info(self, info_key, info):
        """Set new info on the database."""
        return CommandInfo.set_value(self.name, info_key, info)

    def get_info(self, info_key):
        """Get info on the database."""
        command_info = CommandInfo.get_value(self.name, info_key)
        if command_info:
            return command_info.info
        return None

    def remove_info(self, info_key):
        """Remove info on the database."""
        return CommandInfo.remove_value(self.name, info_key)

    @abc.abstractmethod
    def function(self, update=None, context=None):
        """Return a message and needs to be overridden."""
        raise NotImplementedError

    def get_result(self, update=None, context=None):
        """Search and update cache before running the function."""
        if self.expire:
            cached_item = Cache.get_value(self.name)
            if cached_item is None:
                text = self.function(update, context)
                cached_item = Cache.set_value(self.name, text, self.expire,)
            result = cached_item.result
        else:
            result = self.function(update, context)
        return result

    def do_command(self, update=None, context=None):
        """Define a wrapper for get_result."""
        return {
            "update": update,
            "response": self.get_result(update, context),
        }

    def get_schedule(self):
        """Return a utils.Schedule."""
        if self.interval:
            return Schedule(
                self.name + "_function",
                self.get_result,
                self.reply_function_name,
                self.interval,
            )
        return None


def get_commands():
    """Get a list of commands."""
    global command_list
    if command_list is None:
        modules = get_modules_by_path(get_commands_path())
        command_list = get_commands_by_modules(modules)
    return command_list


def get_commands_path():
    """Get directory path of the commands package."""
    root_directory = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    commands_path = os.path.join(root_directory, "commands")
    return commands_path


def get_commands_by_modules(modules):
    """Get CommandBase child classes defined on each command module."""
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
    """Get command modules defined in a directory path."""
    if path not in PATH_MODULES:
        modules_names = get_modules_names(path)
        package_name = get_package_name(path)
        PATH_MODULES[path] = get_modules_by_names(modules_names, package_name)
    return PATH_MODULES[path]


def get_modules_by_names(modules_names, package_name):
    """Import command modules by name."""
    modules = []
    for module_name in modules_names:
        modules.append(
            __import__(
                "{}.{}".format(package_name, module_name),
                fromlist=[module_name],
            )
        )
    return modules


def get_modules_names(path):
    """Get all commmand modules names."""
    modules_names = []
    for module_filename in os.listdir(path):
        if "__" not in module_filename:
            modules_names.append(module_filename.replace(".py", ""))
    return modules_names


def get_package_name(path):
    """Get a package name."""
    package_name = None
    package_path = path

    while os.path.exists(os.path.join(package_path, "__init__.py")):
        current_package_name = os.path.basename(package_path)
        package_path = os.path.dirname(package_path)

        if package_name is None:
            package_name = current_package_name
        else:
            package_name = "{}.{}".format(current_package_name, package_name)

    if package_name is None:
        raise ValueError('You must set a "path" that is a python package.')

    return package_name
