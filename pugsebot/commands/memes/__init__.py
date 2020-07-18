import random
import os

from utils.command_base import CommandBase
from utils.time import UM_DIA_EM_SEGUNDOS
from utils.module import get_modules_by_path

CACHE_EXPIRES = 1800

MEMES_MODULES = get_modules_by_path(os.path.dirname(os.path.abspath(__file__)))
MEMES_IMAGES_FUNCTIONS = [
    meme_module.get_meme_url_image for meme_module in MEMES_MODULES
]

class Memes(CommandBase):
    def __init__(self):
        super().__init__(
            name='memes',
            help_text='Coleta memes de programação',
            reply_function_name='reply_photo',
            schedule_interval=UM_DIA_EM_SEGUNDOS * 2,
            expire=CACHE_EXPIRES,
        )

    def function(self, update=None, context=None):
        random_image_function = random.choice(MEMES_IMAGES_FUNCTIONS)
        return random_image_function()
