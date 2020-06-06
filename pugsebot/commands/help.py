from utils import Command

REPLY_MESSAGE = (
    "/help - Exibe essa mensagem.\n" \
    "/about - Sobre o bot e como contribuir.\n" \
    "/links - Mostrar links úteis sobre Python e da PUG-SE.\n" \
    "/memes - Mostra memes de programação.\n" \
    "/news - Informa notícias sobre Python.\n"\
    "/projects - Mostra os projetos do PUGSE no GitHub.\n"\
    "/say - Broadcast de mensagens.\n"\
    "/udemy - Informa cupons da Udemy.\n"
)

class Help(Command):
    def __init__(self):
        name = 'help'
        help = 'Mostrar funcionalidades do bot.'
        reply_function_name = 'reply_text'
        schedule_interval = None
        super().__init__(
            name, help, reply_function_name,
            schedule_interval,
        )

    def function(self, update=None, context=None):
        text = REPLY_MESSAGE
        return text