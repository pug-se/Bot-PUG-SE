class Schedule():
    def __init__(self, name, function, message_type, interval):
        self.name = name
        self.function = function
        if "photo" in message_type:
            self.format = 'photo'
        else:
            self.format = 'text'
        self.interval = interval
