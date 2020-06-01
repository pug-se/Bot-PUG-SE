from utils import Command

class Say(Command):
    def __init__(self):
        name = 'say'
        help = 'Broadcast de mensagens'
        reply_function_name = 'send_text'
        super().__init__(
            name, help, reply_function_name,
        )

    def function(self, update=None, context=None):
        text = ''
        if update:
            text = update.message.text.replace('/say', '')
        return {'text': text}
        
    def schedule(self):
        return False



