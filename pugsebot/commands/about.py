from utils import Command

REPLY_MESSAGE = (
    'Este bot foi feito pela comunidade de Python PUG-SE para levar '\
    'informações importantes sobre a linguagem Python e eventos da '\
    'comunidade.\nPara saber quais as funcionalidades do bot digite /help '\
    '\nPara saber mais ou contribuir com o projeto: '\
    'https://github.com/pug-se/Bot-PUG-SE'
)

class About(Command):
    def __init__(self):
        super().__init__(
            name='about',
            help_text='Informações sobre o bot',
            reply_function_name='reply_text',
            schedule_interval=None,
        )

    def function(self, update=None, context=None):
        text = REPLY_MESSAGE
        return text
