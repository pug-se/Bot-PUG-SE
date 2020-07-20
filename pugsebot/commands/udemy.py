"""Defines Udemy's command."""

from utils.command_base import CommandBase
from utils.request import get_html_soup
from utils.time import UM_DIA_EM_SEGUNDOS
from utils.logging import command_logger

CACHE_EXPIRES = UM_DIA_EM_SEGUNDOS

class Udemy(CommandBase):
    def __init__(self):
        super().__init__(
            name='udemy',
            help_text='Coleta os cupons da Udemy',
            reply_function_name='reply_text',
            schedule_interval=UM_DIA_EM_SEGUNDOS,
            expire=CACHE_EXPIRES,
        )

    def function(self, update=None, context=None):
        """Collects 100% off Udemy coupons."""

        text = ''
        try:
            url = 'https://couponscorpion.com/'
            soup = get_html_soup(url)
            title_list = []
            url_list = []
            for h3 in soup.findAll('h3'):
                link = h3.find('a')
                if link:
                    title_list.append(link.text.strip())
                    url_list.append(link.get('href').strip())

            text = "Esses foram os cupons da Udemy que encontrei:\n\n"

            index = 1
            for title, url in zip(title_list, url_list):
                text += f'{index}) <a href="{url}">{title}</a>\n'
                index += 1
        except Exception as error:
            command_logger.info(f'Error at {self.name}')
            command_logger.error(error)

        return text
