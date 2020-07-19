"""Defines help command."""

from utils.command_base import CommandBase
from utils.command_modules import get_commands

MESSAGE_HEADER = 'Comandos aceitos:'
TEMPLATE_MESSAGE = '\n/{}: {}'

class Help(CommandBase):
    def __init__(self):
        super().__init__(
            name='help',
            help_text='Mostra os comandos aceitos pelo Bot',
            reply_function_name='reply_text',
            schedule_interval=None,
        )

    def function(self, update=None, context=None):
        text = MESSAGE_HEADER
        command_list = get_commands()
        for command in command_list:
            text += TEMPLATE_MESSAGE.format(command.name, command.help_text)
        return text
