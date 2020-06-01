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
        name = 'about'
        help = 'Informações sobre o bot'
        reply_function_name = 'reply_text'
        super().__init__(
            name, help, reply_function_name,
        )

    def schedule(self):
        return False

    def function(self, update=None, context=None):
        text = REPLY_MESSAGE
        return {'update': update, 'text':text}