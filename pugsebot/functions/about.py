from utils import bot_reply

REPLY_MESSAGE = (
    'Este bot foi feito pela comunidade de Python PUG-SE para levar '
    + 'informações importantes sobre a linguagem Python e eventos da '
    + 'comunidade.\nPara saber quais as funcionalidades do bot digite /help '
    + '\nPara saber mais ou contribuir com o projeto: '
    + 'https://github.com/pug-se/Bot-PUG-SE'
)

def reply(reply_message):
    return bot_reply(reply_message, REPLY_MESSAGE)
