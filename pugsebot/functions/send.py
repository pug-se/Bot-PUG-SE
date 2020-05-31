def reply(send_message):
    def reply_send(update, context):
        text = update.message.text.replace('/send', '')
        send_message(text)
    return reply_send
