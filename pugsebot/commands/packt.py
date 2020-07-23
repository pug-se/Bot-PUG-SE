"""Define packt command."""

import datetime

from utils.command_base import CommandBase
from utils.time import UM_DIA_EM_SEGUNDOS
from utils.request import get_json

class Packt(CommandBase):
    """Configure packt command."""

    def __init__(self):
        """Pass arguments to CommandBase init."""
        super().__init__(
            name='packt',
            help_text='Livro gratúito do Packt Learning',
            reply_function_name='reply_text',
            schedule_interval=UM_DIA_EM_SEGUNDOS,
            expire=UM_DIA_EM_SEGUNDOS,
        )

    def function(self, update=None, context=None):
        """Return a free book from Packt Learning."""
        date1 = datetime.datetime.now()
        date2 = date1 + datetime.timedelta(days=1)
        date1 = date1.strftime('%Y-%m-%d')
        date2 = date2.strftime('%Y-%m-%d')
        url = (
            'https://services.packtpub.com/free-learning-v1/'
            f'offers?dateFrom={date1}&dateTo={date2}'
        )
        response_json = get_json(url)
        book_id = response_json['data'][0]['productId']

        url = (
            'https://static.packt-cdn.com/products/'
            f'{book_id}/summary'
        )
        response_json = get_json(url)

        title = response_json['title']
        summary = response_json['oneLiner']

        return (
            'Livro gratuito da Packt Learning hoje:\n'
            '<a href="https://www.packtpub.com/free-learning">'
            f'{title}</a>\n{summary}')
