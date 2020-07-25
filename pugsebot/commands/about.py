"""Define about command."""

from ..utils.command_base import CommandBase

REPLY_MESSAGE = (
    'Este bot foi feito pela comunidade de Python PUG-SE para levar '
    'informações importantes sobre a linguagem Python e eventos da '
    'comunidade.\nPara saber quais as funcionalidades do bot digite /help '
    '\nPara saber mais ou contribuir com o projeto: '
    'https://github.com/pug-se/Bot-PUG-SE'
)

class About(CommandBase):
    """Configure about command."""

    def __init__(self):
        """Pass arguments to CommandBase init."""
        super().__init__(
            name='about',
            help_text='Informações sobre o bot',
            reply_function_name='reply_text',
            schedule_interval=None,
        )

    def function(self, update=None, context=None):
        """Return a string describing the bot."""
        text = REPLY_MESSAGE
        return text
