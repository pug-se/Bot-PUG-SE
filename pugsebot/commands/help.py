import os

from utils.command_base import CommandBase
from utils.module import get_commands_by_path

MESSAGE_HEADER = 'Comandos aceitos:'
TEMPLATE_MESSAGE = '\n/{}: {}'

def get_commands_path():
    return os.path.dirname(os.path.abspath(__file__))

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
        command_list = get_commands_by_path(get_commands_path())
        for command in command_list:
            text += TEMPLATE_MESSAGE.format(command.name, command.help_text)
        return text
