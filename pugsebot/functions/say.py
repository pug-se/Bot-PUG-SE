def reply(send_text):
    def reply_send(update=None, context=None):
        if update:
            text = update.message.text.replace('/say', '')
            if text:
                send_text(text)
        return update
    return reply_send
