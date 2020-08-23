"""Define book command."""

import datetime

from ..utils.command import CommandBase
from ..utils.time import UM_DIA_EM_SEGUNDOS
from ..utils.request import get_json


class Book(CommandBase):
    """Configure book command."""

    def __init__(self):
        """Pass arguments to CommandBase init."""
        super().__init__(
            name="book",
            help_text="Livro gratuito do Packt Learning",
            reply_function_name="reply_text",
            schedule_interval=UM_DIA_EM_SEGUNDOS,
            expire=UM_DIA_EM_SEGUNDOS,
        )

    def function(self, update=None, context=None):
        """Return a free book from Packt Learning."""
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(days=1)
        start_date_formated = start_date.strftime("%Y-%m-%d")
        end_date_formated = end_date.strftime("%Y-%m-%d")
        promotion_url = (
            "https://services.packtpub.com/free-learning-v1/"
            f"offers?dateFrom={start_date_formated}&dateTo={end_date_formated}"
        )
        promotion_response_json = get_json(promotion_url)
        book_id = promotion_response_json["data"][0]["productId"]

        book_url = (
            "https://static.packt-cdn.com/products/" f"{book_id}/summary"
        )
        book_response_json = get_json(book_url)

        title = book_response_json["title"]
        summary = book_response_json["oneLiner"]

        return (
            "Livro gratuito da Packt Learning hoje:\n"
            '<a href="https://www.packtpub.com/free-learning">'
            f"{title}</a>\n{summary}"
        )
