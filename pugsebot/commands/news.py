"""Define news command."""

from ..utils.command import CommandBase
from ..utils.request import get_html_soup
from ..utils.time import UM_DIA_EM_SEGUNDOS
from ..utils.logging import command_logger

CACHE_EXPIRES = UM_DIA_EM_SEGUNDOS * 7


class News(CommandBase):
    """Configure news command."""

    def __init__(self):
        """Pass arguments to CommandBase init."""
        super().__init__(
            name="news",
            help_text="Coleta notícias sobre Python",
            reply_function_name="reply_text",
            schedule_interval=UM_DIA_EM_SEGUNDOS * 7,
            expire=CACHE_EXPIRES,
        )

    def function(self, update=None, context=None):
        """Return news about Python."""
        text = ""
        try:
            url = "https://www.python.org/blogs/"
            soup = get_html_soup(url)
            h3 = soup.find("h3", {"class": "event-title"})
            link = h3.find("a")
            title = link.text.strip()
            url = link.get("href").strip()
            text = "A notícia mais quente sobre Python:\n"
            text += f'<a href="{url}">{title}</a>'
        except Exception as error:
            command_logger.info(f"Error at {self.name}")
            command_logger.error(error)
        return text
