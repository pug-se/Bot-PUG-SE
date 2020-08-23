"""Define memes command."""

import random
import os

from utils.command import CommandBase, get_modules_by_path
from utils.time import UM_DIA_EM_SEGUNDOS

CACHE_EXPIRES = 1800

MEMES_MODULES = get_modules_by_path(os.path.dirname(os.path.abspath(__file__)))
MEMES_IMAGES_FUNCTIONS = [
    meme_module.get_meme_url_image for meme_module in MEMES_MODULES
]


class Memes(CommandBase):
    """Configures meme command."""

    def __init__(self):
        """Pass arguments to CommandBase init."""
        super().__init__(
            name="memes",
            help_text="Coleta memes de programação",
            reply_function_name="reply_photo",
            schedule_interval=UM_DIA_EM_SEGUNDOS * 2,
            expire=CACHE_EXPIRES,
        )

    def function(self, update=None, context=None):
        """Collect a random meme image."""
        random_image_function = random.choice(MEMES_IMAGES_FUNCTIONS)
        return random_image_function()
