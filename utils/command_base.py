"""Define utilites creating new commands."""

import abc

from .database import Cache, CommandInfo
from .schedule import Schedule


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
