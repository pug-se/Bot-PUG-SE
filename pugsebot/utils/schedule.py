"""Defines a wrapper for scheduling command execution."""

class Schedule():
    """Wrapper for scheduling messaging functions.
    
    Attributes:
    name:
        name of the function
    function:
        function/method to be executed
    format:
        format of the message to be sent. Default is "text"
    """
    
    def __init__(self, name, function, message_type, interval):
        self.name = name
        self.function = function
        if "photo" in message_type:
            self.format = 'photo'
        else:
            self.format = 'text'
        self.interval = interval
