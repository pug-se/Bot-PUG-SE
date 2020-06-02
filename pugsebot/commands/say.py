from utils import Command

class Say(Command):
    def __init__(self):
        name = 'say'
        help = 'Broadcast de mensagens'
        reply_function_name = 'send_text'
        schedule_interval = None
        super().__init__(
            name, help, reply_function_name,
            schedule_interval,
        )

    def function(self, update=None, context=None):
        text = ''
        if update:
            text = update.message.text.replace(
                '/say ', ''
            ).strip()
        return text