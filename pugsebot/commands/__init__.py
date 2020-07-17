import os

from utils.module import get_commands_from_path

command_list = get_commands_from_path(
    os.path.dirname(os.path.abspath(__file__))
)
