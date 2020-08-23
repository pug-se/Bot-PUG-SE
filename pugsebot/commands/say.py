"""Define say command."""
from ..utils.command import CommandBase


class Say(CommandBase):
    """Configure say command."""

    def __init__(self):
        """Pass arguments to CommandBase init."""
        super().__init__(
            name="say",
            help_text="Broadcast de mensagens",
            reply_function_name="send_text",
            schedule_interval=None,
        )

    def function(self, update=None, context=None):
        """Forward a message to group at utils.environment.TARGET_CHAT_ID."""
        text = ""
        if update:
            text = update.message.text.replace("/say ", "").strip()
        return text
