from utils import Command

class Say(Command):
    def __init__(self):
        super().__init__(
            name='say',
            help_text='Broadcast de mensagens',
            reply_function_name='send_text',
            schedule_interval=None,
        )

    def function(self, update=None, context=None):
        text = ''
        if update:
            text = update.message.text.replace(
                '/say ', ''
            ).strip()
        return text
