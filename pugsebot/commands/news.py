import logging

from utils import Command, get_html_soup, UM_DIA_EM_SEGUNDOS

logger = logging.getLogger('News')

class News(Command):
    def __init__(self):
        name = 'news'
        help = 'Coleta notícias sobre Python'
        reply_function_name = 'reply_text'
        super().__init__(
            name, help, reply_function_name,
        )

    def schedule(self):
        '''
        def send_news():
            bot.send_message(get_python_news())
        bot.schedule_manager.add_schedule(
            send_news, UM_DIA_EM_SEGUNDOS * 7,
        )
        '''
        return False

    def function(self, update=None, context=None):
        text = ''
        try:
            url = 'https://www.python.org/blogs/'
            soup = get_html_soup(url)

            h3 = soup.find('h3', {'class': 'event-title'})
            link = h3.find('a')
            title = link.text.strip()
            url = link.get('href').strip()
            text = 'A notícia mais quente sobre Python:\n'
            text += f'<a href="{url}">{title}</a>'
        except Exception as error:
            logger.error(error)

        return {'update': update, 'text':text}